---
title: 03. 인증 구성 (Entra ID + .env)
duration_minutes: 15
last_updated: 2026-08-12
---

# 03. 인증 구성

## 개요 · 학습 목표

이 워크샵은 API Key 대신 **Microsoft Entra ID(keyless) 인증**을 사용합니다. `az login`으로 로그인하면 노트북의 `DefaultAzureCredential`이 자동으로 자격 증명을 찾아 사용합니다.

> **왜 API Key가 아닌가?** 최신 SDK(azure-ai-projects 2.x)는 API Key 인증을 지원하지 않으며, Microsoft는 [keyless 인증](https://learn.microsoft.com/azure/developer/ai/keyless-connections)을 권장합니다. 키 유출 위험이 없고 RBAC로 권한을 세밀하게 제어할 수 있습니다.

## 1. Azure 로그인

터미널에서 로그인합니다 (Codespaces에서는 `--use-device-code` 사용):

```bash
az login --use-device-code
# 구독이 여러 개면 실습용 구독을 선택
az account set --subscription "<subscription-name-or-id>"
```

## 2. 권한 확인

Foundry 프로젝트에 대해 본인 계정에 **Azure AI User**(또는 상위) 역할이 필요합니다. 프로젝트를 직접 만들었다면 보통 자동으로 부여되어 있습니다. 권한 오류가 나면 포털의 **Operate > Admin**에서 역할을 확인하세요.

## 3. .env 파일 구성

1. 예시 파일을 복사합니다:

    ```bash
    cp .env.example .env
    ```

2. [Foundry 포털](https://ai.azure.com)에서 프로젝트 **Overview**를 열고 **프로젝트 엔드포인트**를 복사해 붙여넣습니다:

    ```bash
    PROJECT_ENDPOINT="https://<resource>.services.ai.azure.com/api/projects/<project-name>"
    ```

3. [02장](../02-foundry-project/README.md)에서 배포한 모델의 **배포 이름**을 확인해 업데이트합니다:

    ```bash
    MODEL_NAME="gpt-5-mini"
    TEXT_EMBEDDING_MODEL="text-embedding-3-small"
    ```

`SEARCH_*` 변수 3개는 [04장](../04-chat-completion/README.md)에서 Azure AI Search를 만든 뒤에 채웁니다.

## 검증

```bash
python - <<'EOF'
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()
project = AIProjectClient(
    endpoint=os.environ["PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential(),
)
print("✅ 연결 성공! 배포 목록:")
for d in project.deployments.list():
    print(" -", d.name)
EOF
```

배포한 모델 이름들이 출력되면 인증 구성이 완료된 것입니다.

## 트러블슈팅

- `DefaultAzureCredential failed`: `az login`이 되어 있는지, 올바른 테넌트/구독인지 확인 (`az account show`)
- `401/403`: 프로젝트에 대한 Azure AI User 역할 여부 확인. 역할 부여 후 반영까지 몇 분 걸릴 수 있음
- 엔드포인트 형식 오류: `/api/projects/<project-name>`까지 포함된 전체 URL인지 확인

## 다음 단계

→ [04. Chat Completion](../04-chat-completion/README.md)
