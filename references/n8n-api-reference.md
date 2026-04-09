# n8n API 상세 레퍼런스

## 인증

모든 API 요청에 `X-N8N-API-KEY` 헤더가 필요합니다.

```
X-N8N-API-KEY: <your-api-key>
```

## 워크플로우 API

### GET /api/v1/workflows
워크플로우 목록을 가져옵니다.

쿼리 파라미터:
- `limit` (number) — 결과 수 제한 (기본 10, 최대 250)
- `cursor` (string) — 페이지네이션 커서
- `tags` (string) — 태그 이름으로 필터링
- `name` (string) — 이름으로 필터링
- `active` (boolean) — 활성 상태로 필터링

응답:
```json
{
  "data": [
    {
      "id": "string",
      "name": "string",
      "active": true,
      "createdAt": "2026-01-01T00:00:00.000Z",
      "updatedAt": "2026-01-01T00:00:00.000Z",
      "tags": []
    }
  ],
  "nextCursor": "string"
}
```

### GET /api/v1/workflows/{id}
워크플로우 상세 정보를 가져옵니다. 노드, 연결, 설정 포함.

### POST /api/v1/workflows
새 워크플로우를 생성합니다.

요청 본문:
```json
{
  "name": "My Workflow",
  "nodes": [...],
  "connections": {...},
  "settings": {
    "executionOrder": "v1"
  }
}
```

### PUT /api/v1/workflows/{id}
기존 워크플로우를 수정합니다. 전체 워크플로우 JSON을 전송해야 합니다.

### DELETE /api/v1/workflows/{id}
워크플로우를 삭제합니다.

### POST /api/v1/workflows/{id}/activate
워크플로우를 활성화합니다. 트리거 노드가 있어야 합니다.

### POST /api/v1/workflows/{id}/deactivate
워크플로우를 비활성화합니다.

## 실행(Execution) API

### GET /api/v1/executions
실행 이력을 가져옵니다.

쿼리 파라미터:
- `workflowId` (string) — 특정 워크플로우의 실행만 조회
- `status` (string) — `success`, `error`, `waiting` 등으로 필터
- `limit` (number) — 결과 수 제한

### GET /api/v1/executions/{id}
특정 실행의 상세 정보를 가져옵니다. 각 노드의 입출력 데이터 포함.

### DELETE /api/v1/executions/{id}
실행 이력을 삭제합니다.

## 태그 API

### GET /api/v1/tags
태그 목록을 가져옵니다.

### POST /api/v1/tags
새 태그를 생성합니다.

```json
{"name": "태그이름"}
```

## 워크플로우 노드 구조 예제

### 기본 Webhook → Code 워크플로우

```json
{
  "name": "Webhook Example",
  "nodes": [
    {
      "parameters": {
        "httpMethod": "POST",
        "path": "my-webhook"
      },
      "id": "node-001",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [250, 300],
      "webhookId": "unique-webhook-id"
    },
    {
      "parameters": {
        "jsCode": "// 입력 데이터 처리\nconst items = $input.all();\nreturn items.map(item => ({\n  json: {\n    received: item.json,\n    processedAt: new Date().toISOString()\n  }\n}));"
      },
      "id": "node-002",
      "name": "Process Data",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [500, 300]
    }
  ],
  "connections": {
    "Webhook": {
      "main": [[{"node": "Process Data", "type": "main", "index": 0}]]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

### Schedule → HTTP Request 워크플로우

```json
{
  "name": "Scheduled API Call",
  "nodes": [
    {
      "parameters": {
        "rule": {
          "interval": [{"field": "hours", "hoursInterval": 1}]
        }
      },
      "id": "node-001",
      "name": "Schedule Trigger",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1.2,
      "position": [250, 300]
    },
    {
      "parameters": {
        "url": "https://api.example.com/data",
        "method": "GET",
        "options": {}
      },
      "id": "node-002",
      "name": "HTTP Request",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4.2,
      "position": [500, 300]
    }
  ],
  "connections": {
    "Schedule Trigger": {
      "main": [[{"node": "HTTP Request", "type": "main", "index": 0}]]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

### Manual Trigger → IF 분기 워크플로우

```json
{
  "name": "Conditional Example",
  "nodes": [
    {
      "parameters": {},
      "id": "node-001",
      "name": "Manual Trigger",
      "type": "n8n-nodes-base.manualTrigger",
      "typeVersion": 1,
      "position": [250, 300]
    },
    {
      "parameters": {
        "conditions": {
          "options": {
            "caseSensitive": true,
            "leftValue": "",
            "typeValidation": "strict"
          },
          "conditions": [
            {
              "id": "cond-001",
              "leftValue": "={{ $json.status }}",
              "rightValue": "active",
              "operator": {
                "type": "string",
                "operation": "equals"
              }
            }
          ],
          "combinator": "and"
        },
        "options": {}
      },
      "id": "node-002",
      "name": "IF",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [500, 300]
    },
    {
      "parameters": {
        "jsCode": "return [{json: {result: 'Active path'}}];"
      },
      "id": "node-003",
      "name": "Active Handler",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [750, 200]
    },
    {
      "parameters": {
        "jsCode": "return [{json: {result: 'Inactive path'}}];"
      },
      "id": "node-004",
      "name": "Inactive Handler",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [750, 400]
    }
  ],
  "connections": {
    "Manual Trigger": {
      "main": [[{"node": "IF", "type": "main", "index": 0}]]
    },
    "IF": {
      "main": [
        [{"node": "Active Handler", "type": "main", "index": 0}],
        [{"node": "Inactive Handler", "type": "main", "index": 0}]
      ]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

## REST API를 통한 로그인 (세션 기반)

API 키 없이 세션 쿠키로 접근할 때:

```
POST /rest/login
Content-Type: application/json

{"emailOrLdapLoginId": "user@email.com", "password": "password"}
```

응답 헤더의 `Set-Cookie: n8n-auth=...` 값을 이후 요청에 사용합니다.

## 에러 코드

| 코드 | 의미 |
|------|------|
| 401 | 인증 실패 — API 키 확인 |
| 404 | 리소스 없음 — ID 확인 |
| 400 | 잘못된 요청 — 요청 본문 확인 |
| 500 | 서버 내부 오류 |
