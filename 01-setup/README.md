---
title: 01. 실습 환경 구성
duration_minutes: 15
last_updated: 2026-08-12
---

# 01. 실습 환경 구성

## 개요 · 학습 목표

실습에 사용할 개발 환경을 준비합니다. **GitHub Codespaces(권장)** 또는 로컬 VS Code 중 하나를 선택하세요 — 두 방식 모두 같은 `.devcontainer` 정의를 사용하므로 결과 환경은 동일합니다.

## 방법 A — GitHub Codespaces (권장)

1. 이 리포지토리의 GitHub 페이지에서 **Code > Codespaces > Create codespace on main**을 클릭합니다. (또는 루트 README의 "Open in GitHub Codespaces" 뱃지 클릭)
2. 컨테이너가 준비되면 Python 3.12, Azure CLI, Jupyter 확장과 `requirements.txt`의 패키지가 자동 설치되어 있습니다.
3. 터미널에서 Azure에 로그인합니다 (이후 [03. 인증 구성](../03-authentication/README.md)에서 사용):

    ```bash
    az login --use-device-code
    ```

## 방법 B — 로컬 VS Code

<details>
<summary>로컬 환경 구성 절차 (펼치기)</summary>

**사전 설치**: [Python 3.11+](https://www.python.org/downloads/), [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), [Git](https://git-scm.com/downloads), [VS Code](https://code.visualstudio.com/)

1. 리포지토리를 복제하고 VS Code로 엽니다.

    ```bash
    git clone https://github.com/kyungtaak/AzureAIFoundryWorkshop-Code.git
    cd AzureAIFoundryWorkshop-Code
    code .
    ```

2. VS Code 확장 `Python`, `Jupyter`를 설치합니다.
3. 가상환경을 만들고 패키지를 설치합니다. ([uv](https://docs.astral.sh/uv/)를 쓰면 더 빠릅니다)

    ```bash
    # venv 사용 시
    python -m venv .venv
    source .venv/bin/activate   # Windows: .venv\Scripts\activate
    pip install -r requirements.txt

    # 또는 uv 사용 시
    uv venv && source .venv/bin/activate
    uv pip install -r requirements.txt
    ```

4. Azure CLI 로그인:

    ```bash
    az login
    ```

> Docker가 있다면 VS Code의 **Dev Containers: Reopen in Container** 명령으로 Codespaces와 동일한 컨테이너 환경을 로컬에서 쓸 수도 있습니다.

</details>

## 검증

터미널에서 아래가 모두 성공하면 준비 완료입니다:

```bash
python -c "import azure.ai.projects, openai, azure.identity; print('SDK OK')"
az account show --query name -o tsv
```

## 다음 단계

→ [02. Foundry 프로젝트 구성](../02-foundry-project/README.md)
