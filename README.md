# n8n Manager Skill

Claude Cowork용 n8n 워크플로우 자동화 관리 스킬입니다.

## 기능

- **워크플로우 관리** — n8n API를 통해 워크플로우 생성/수정/삭제/실행
- **서버 배포** — Docker Compose 템플릿으로 새 n8n 서버 원클릭 배포
- **팀 공유** — .skill 파일로 누구나 설치 가능

## 설치

1. `n8n-manager.skill` 파일을 다운로드
2. Claude Desktop > Cowork에서 스킬 추가
3. 또는 파일을 더블클릭하여 설치

## 사용 예시

- "n8n에 웹훅 워크플로우 만들어줘"
- "워크플로우 목록 보여줘"
- "새 서버에 n8n 배포해줘"
- "스케줄 워크플로우 만들어서 매시간 API 호출해줘"

## 구성 파일

| 파일 | 설명 |
|------|------|
| `SKILL.md` | 스킬 본체 (트리거 조건, 사용법) |
| `references/api-credentials.json` | n8n API 접속 정보 |
| `references/docker-compose-template.yml` | Docker Compose 배포 템플릿 |
| `references/n8n-api-reference.md` | n8n API 상세 레퍼런스 |
| `scripts/n8n_api.py` | Python CLI 헬퍼 스크립트 |

## 설정

`references/api-credentials.json`에서 자신의 n8n 서버 정보를 입력하세요:

```json
{
  "default": {
    "base_url": "http://your-server:port",
    "api_key": "your-api-key"
  }
}
```

## 라이선스

MIT
