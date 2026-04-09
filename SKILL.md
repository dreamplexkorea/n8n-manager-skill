---
name: n8n-manager
description: n8n 워크플로우 자동화 플랫폼의 종합 관리 스킬. 온라인 n8n 인스턴스에 API로 접속하여 워크플로우를 생성·수정·삭제·실행하고, 새 서버를 Docker Compose로 배포합니다. 다음과 같은 경우 반드시 이 스킬을 사용하세요 — "n8n 워크플로우 만들어줘", "n8n에 자동화 추가해줘", "워크플로우 목록 보여줘", "n8n 서버 세팅해줘", "n8n 배포", "워크플로우 실행", "n8n API", "자동화 파이프라인", "webhook 만들어줘", "n8n 노드 설정" 등. n8n, workflow, 자동화, automation, webhook 등의 키워드가 나오면 이 스킬을 사용하세요.
---

# n8n Manager Skill

n8n 워크플로우 자동화 플랫폼을 관리하는 스킬입니다. 크게 두 가지 기능을 제공합니다:

1. **워크플로우 관리** — 온라인 n8n 인스턴스에 API로 접속하여 워크플로우 CRUD 및 실행
2. **서버 배포** — Docker Compose를 사용한 새 n8n 서버 설치 및 구성

---

## 사전 준비: 접속 정보 확인

이 스킬을 사용하기 전에 n8n 접속 정보가 필요합니다.

### 기본 접속 정보 (소유자 서버)

| 항목 | 값 |
|------|-----|
| URL | `http://222.233.66.50:3003` |
| API Key | `references/api-credentials.json`에 저장 |
| 소유자 | 강욱곤 (kangukkon1@gmail.com) |

사용자가 다른 n8n 인스턴스를 사용하고 싶다면, URL과 API 키를 물어보세요.

---

## 파트 1: 워크플로우 관리

### API 호출 방법

n8n API 호출은 반드시 **사용자의 로컬 환경**에서 실행해야 합니다 (샌드박스 네트워크 제한 때문).

**PowerShell (Windows-MCP)을 사용할 수 있는 경우:**
```powershell
$apiKey = "<API_KEY>"
$baseUrl = "http://222.233.66.50:3003"
$headers = @{"X-N8N-API-KEY"=$apiKey}

# 워크플로우 목록
Invoke-RestMethod -Uri "$baseUrl/api/v1/workflows" -Headers $headers

# 워크플로우 생성
$body = @{...} | ConvertTo-Json -Depth 20
Invoke-RestMethod -Uri "$baseUrl/api/v1/workflows" -Method Post -Headers $headers -Body $body -ContentType "application/json"
```

**PowerShell이 없는 경우:**
사용자에게 curl 명령어나 Python 스크립트를 생성해서 제공하세요.

### 워크플로우 생성 가이드

n8n 워크플로우를 만들 때는 다음 구조를 따릅니다:

```json
{
  "name": "워크플로우 이름",
  "nodes": [
    {
      "parameters": {},
      "id": "고유ID",
      "name": "노드이름",
      "type": "n8n-nodes-base.노드타입",
      "typeVersion": 1,
      "position": [x, y]
    }
  ],
  "connections": {
    "소스노드이름": {
      "main": [[{"node": "대상노드이름", "type": "main", "index": 0}]]
    }
  },
  "settings": {
    "executionOrder": "v1"
  }
}
```

### 주요 API 엔드포인트

| 작업 | 메서드 | 엔드포인트 |
|------|--------|------------|
| 워크플로우 목록 | GET | `/api/v1/workflows` |
| 워크플로우 조회 | GET | `/api/v1/workflows/{id}` |
| 워크플로우 생성 | POST | `/api/v1/workflows` |
| 워크플로우 수정 | PUT | `/api/v1/workflows/{id}` |
| 워크플로우 삭제 | DELETE | `/api/v1/workflows/{id}` |
| 워크플로우 활성화 | POST | `/api/v1/workflows/{id}/activate` |
| 워크플로우 비활성화 | POST | `/api/v1/workflows/{id}/deactivate` |
| 실행 목록 | GET | `/api/v1/executions` |
| 실행 조회 | GET | `/api/v1/executions/{id}` |
| 태그 목록 | GET | `/api/v1/tags` |

### 자주 사용하는 노드 타입

#### 트리거 노드 (워크플로우 시작점)
- `n8n-nodes-base.manualTrigger` — 수동 실행
- `n8n-nodes-base.webhook` — 웹훅 트리거
- `n8n-nodes-base.scheduleTrigger` — 스케줄(Cron) 트리거
- `n8n-nodes-base.emailTrigger` — 이메일 트리거

#### 일반 노드
- `n8n-nodes-base.httpRequest` — HTTP 요청
- `n8n-nodes-base.code` — JavaScript/Python 코드 실행
- `n8n-nodes-base.if` — 조건 분기
- `n8n-nodes-base.switch` — 다중 분기
- `n8n-nodes-base.set` — 데이터 설정
- `n8n-nodes-base.merge` — 데이터 병합
- `n8n-nodes-base.splitInBatches` — 배치 처리
- `n8n-nodes-base.noOp` — 아무 동작 없음 (연결용)

#### 외부 서비스 노드
- `n8n-nodes-base.slack` — Slack 메시지
- `n8n-nodes-base.gmail` — Gmail
- `n8n-nodes-base.googleSheets` — Google Sheets
- `n8n-nodes-base.notion` — Notion
- `n8n-nodes-base.openAi` — OpenAI
- `n8n-nodes-base.telegram` — Telegram

### 워크플로우 생성 시 주의사항

1. **모든 워크플로우에는 반드시 트리거 노드가 1개 이상** 있어야 합니다.
2. **노드 ID는 UUID 형식**을 사용합니다 (예: `"id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"`).
3. **노드 위치(position)**는 `[x, y]` 좌표이며, 노드 간 간격은 보통 250px입니다.
4. **connections에서 소스 노드 이름은 정확히 일치**해야 합니다.
5. 워크플로우 생성 후 **활성화(activate)**해야 트리거가 동작합니다.

### 워크플로우 생성 절차

1. 사용자에게 원하는 자동화 내용을 파악
2. 필요한 노드 구성을 설계
3. JSON 워크플로우를 작성
4. `POST /api/v1/workflows`로 생성
5. 필요시 `POST /api/v1/workflows/{id}/activate`로 활성화
6. 사용자에게 결과 URL 제공: `http://222.233.66.50:3003/workflow/{id}`

---

## 파트 2: 서버 배포

새 컴퓨터에 n8n을 배포하려면 `references/docker-compose-template.yml`을 참조하세요.

### 필요 조건
- Docker 및 Docker Compose 설치
- 최소 2GB RAM, 10GB 디스크
- 포트 1개 개방 (기본 5678, 커스텀 가능)

### 배포 절차

1. 배포 대상 환경 확인 (OS, Docker 버전, 공인 IP 등)
2. `references/docker-compose-template.yml` 기반으로 docker-compose.yml 생성
3. 사용자 환경에 맞게 변수 수정:
   - `WEBHOOK_URL` — 외부 접근 URL
   - `N8N_BASIC_AUTH_USER/PASSWORD` — 로그인 정보
   - `N8N_ENCRYPTION_KEY` — 암호화 키 (신규 생성)
   - 포트 매핑
4. `docker-compose up -d`로 실행
5. 초기 설정 안내

### 보안 권장사항
- 기본 비밀번호 변경 필수
- HTTPS 설정 권장 (Nginx reverse proxy + Let's Encrypt)
- 방화벽에서 n8n 포트만 허용
- API 키는 필요한 scope만 부여

---

## 참조 파일

| 파일 | 용도 |
|------|------|
| `references/api-credentials.json` | API 접속 정보 |
| `references/docker-compose-template.yml` | Docker Compose 배포 템플릿 |
| `references/n8n-api-reference.md` | n8n API 상세 레퍼런스 |
| `scripts/n8n_api.py` | Python API 헬퍼 스크립트 |
