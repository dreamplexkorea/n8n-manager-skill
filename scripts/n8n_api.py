#!/usr/bin/env python3
"""
n8n API Helper — 워크플로우 관리 유틸리티

사용법:
    python n8n_api.py list                          # 워크플로우 목록
    python n8n_api.py get <workflow_id>              # 워크플로우 상세 조회
    python n8n_api.py create <json_file>             # 워크플로우 생성
    python n8n_api.py update <workflow_id> <json>     # 워크플로우 수정
    python n8n_api.py delete <workflow_id>            # 워크플로우 삭제
    python n8n_api.py activate <workflow_id>          # 워크플로우 활성화
    python n8n_api.py deactivate <workflow_id>        # 워크플로우 비활성화
    python n8n_api.py executions [workflow_id]        # 실행 이력
    python n8n_api.py tags                            # 태그 목록
    python n8n_api.py export <workflow_id> [file]     # 워크플로우 JSON 내보내기

환경변수:
    N8N_BASE_URL  — n8n 서버 URL (기본: http://222.233.66.50:3003)
    N8N_API_KEY   — API 키
"""

import json
import os
import sys
import urllib.request
import urllib.error

# --- 설정 ---
DEFAULT_BASE_URL = "http://222.233.66.50:3003"
DEFAULT_API_KEY = ""  # 보안을 위해 환경변수 사용 권장

def get_config():
    base_url = os.environ.get("N8N_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    api_key = os.environ.get("N8N_API_KEY", DEFAULT_API_KEY)
    if not api_key:
        print("오류: N8N_API_KEY 환경변수를 설정해주세요.")
        print("  Windows: $env:N8N_API_KEY = 'your-api-key'")
        print("  Linux/Mac: export N8N_API_KEY='your-api-key'")
        sys.exit(1)
    return base_url, api_key

def api_request(method, endpoint, data=None):
    """n8n API 요청을 보냅니다."""
    base_url, api_key = get_config()
    url = f"{base_url}/api/v1{endpoint}"
    headers = {
        "X-N8N-API-KEY": api_key,
        "Content-Type": "application/json",
    }

    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"API 오류 ({e.code}): {error_body}")
        sys.exit(1)

# --- 명령어 ---

def cmd_list():
    """워크플로우 목록 조회"""
    result = api_request("GET", "/workflows")
    workflows = result.get("data", [])
    print(f"\n총 {len(workflows)}개 워크플로우:\n")
    print(f"{'ID':<20} {'활성':<6} {'이름'}")
    print("-" * 60)
    for wf in workflows:
        active = "✅" if wf.get("active") else "❌"
        print(f"{wf['id']:<20} {active:<6} {wf['name']}")

def cmd_get(workflow_id):
    """워크플로우 상세 조회"""
    result = api_request("GET", f"/workflows/{workflow_id}")
    print(json.dumps(result, indent=2, ensure_ascii=False))

def cmd_create(json_file_or_data):
    """워크플로우 생성"""
    if os.path.isfile(json_file_or_data):
        with open(json_file_or_data, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.loads(json_file_or_data)

    result = api_request("POST", "/workflows", data)
    wf = result.get("data", result)
    print(f"✅ 워크플로우 생성 완료!")
    print(f"   ID: {wf.get('id')}")
    print(f"   이름: {wf.get('name')}")
    base_url, _ = get_config()
    print(f"   URL: {base_url}/workflow/{wf.get('id')}")

def cmd_update(workflow_id, json_file_or_data):
    """워크플로우 수정"""
    if os.path.isfile(json_file_or_data):
        with open(json_file_or_data, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = json.loads(json_file_or_data)

    result = api_request("PUT", f"/workflows/{workflow_id}", data)
    print(f"✅ 워크플로우 수정 완료: {workflow_id}")

def cmd_delete(workflow_id):
    """워크플로우 삭제"""
    api_request("DELETE", f"/workflows/{workflow_id}")
    print(f"✅ 워크플로우 삭제 완료: {workflow_id}")

def cmd_activate(workflow_id):
    """워크플로우 활성화"""
    result = api_request("POST", f"/workflows/{workflow_id}/activate")
    print(f"✅ 워크플로우 활성화 완료: {workflow_id}")

def cmd_deactivate(workflow_id):
    """워크플로우 비활성화"""
    result = api_request("POST", f"/workflows/{workflow_id}/deactivate")
    print(f"✅ 워크플로우 비활성화 완료: {workflow_id}")

def cmd_executions(workflow_id=None):
    """실행 이력 조회"""
    endpoint = "/executions"
    if workflow_id:
        endpoint += f"?workflowId={workflow_id}"
    result = api_request("GET", endpoint)
    execs = result.get("data", [])
    print(f"\n총 {len(execs)}개 실행 이력:\n")
    print(f"{'ID':<12} {'상태':<12} {'워크플로우':<20} {'시작시간'}")
    print("-" * 70)
    for ex in execs[:20]:
        status = ex.get("status", "unknown")
        wf_name = ex.get("workflowData", {}).get("name", "N/A")[:18]
        started = ex.get("startedAt", "N/A")[:19]
        print(f"{ex['id']:<12} {status:<12} {wf_name:<20} {started}")

def cmd_tags():
    """태그 목록 조회"""
    result = api_request("GET", "/tags")
    tags = result.get("data", [])
    print(f"\n총 {len(tags)}개 태그:\n")
    for tag in tags:
        print(f"  [{tag['id']}] {tag['name']}")

def cmd_export(workflow_id, output_file=None):
    """워크플로우를 JSON 파일로 내보내기"""
    result = api_request("GET", f"/workflows/{workflow_id}")
    if output_file is None:
        name = result.get("name", workflow_id).replace(" ", "_")
        output_file = f"{name}.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"✅ 워크플로우 내보내기 완료: {output_file}")

# --- 진입점 ---

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1].lower()
    args = sys.argv[2:]

    commands = {
        "list": lambda: cmd_list(),
        "get": lambda: cmd_get(args[0]) if args else print("사용법: n8n_api.py get <workflow_id>"),
        "create": lambda: cmd_create(args[0]) if args else print("사용법: n8n_api.py create <json_file>"),
        "update": lambda: cmd_update(args[0], args[1]) if len(args) >= 2 else print("사용법: n8n_api.py update <id> <json>"),
        "delete": lambda: cmd_delete(args[0]) if args else print("사용법: n8n_api.py delete <workflow_id>"),
        "activate": lambda: cmd_activate(args[0]) if args else print("사용법: n8n_api.py activate <workflow_id>"),
        "deactivate": lambda: cmd_deactivate(args[0]) if args else print("사용법: n8n_api.py deactivate <workflow_id>"),
        "executions": lambda: cmd_executions(args[0] if args else None),
        "tags": lambda: cmd_tags(),
        "export": lambda: cmd_export(args[0], args[1] if len(args) > 1 else None) if args else print("사용법: n8n_api.py export <workflow_id>"),
    }

    if cmd in commands:
        commands[cmd]()
    else:
        print(f"알 수 없는 명령어: {cmd}")
        print(f"사용 가능: {', '.join(commands.keys())}")

if __name__ == "__main__":
    main()
