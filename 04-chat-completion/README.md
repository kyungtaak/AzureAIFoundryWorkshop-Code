---
title: 04. Chat Completion · Embeddings · RAG
duration_minutes: 90
last_updated: 2026-08-12
---

# 04. Chat Completion · Embeddings · RAG

## 개요 · 학습 목표

`openai` SDK와 Foundry 프로젝트를 사용해 Chat Completions → Embeddings → 기본 RAG를 순서대로 실습합니다.

| 노트북 | 내용 | 소요 시간 |
|--------|------|-----------|
| [01-basic-chat-completion.ipynb](01-basic-chat-completion.ipynb) | Chat Completions 기본, 프롬프트 템플릿 | 25분 |
| [02-embeddings.ipynb](02-embeddings.ipynb) | 텍스트 임베딩 | 20분 |
| [03-basic-rag.ipynb](03-basic-rag.ipynb) | Azure AI Search 기반 벡터 검색 + RAG | 45분 |

노트북 01·02는 바로 실행할 수 있습니다. **노트북 03(RAG)을 시작하기 전에** 아래 Azure AI Search 구성을 완료하세요.

## Azure AI Search 구성 (노트북 03 사전 준비)

### AI Search 리소스 생성

1. [Azure Portal](https://portal.azure.com)에 접속해 상단 검색창에 `AI Search`를 입력합니다.
2. **+ 만들기**를 클릭하고 다음과 같이 구성합니다:
   - 리소스 그룹: Foundry 프로젝트와 **같은 리소스 그룹** (Foundry 포털의 프로젝트 Overview에서 확인 가능)
   - 서비스 이름: `<alias>-ai-search`
   - 위치: Korea Central (프로젝트와 동일 권장)
   - 가격 책정 계층: **Basic** (실습에는 충분 — Standard도 무방)
3. **검토 + 만들기 > 만들기**로 리소스를 생성합니다.

### .env 업데이트

생성된 AI Search 리소스의 **개요**에서 URL을, **설정 > 키**에서 관리자 키를 복사해 `.env`를 업데이트합니다:

```bash
SEARCH_ENDPOINT="https://<alias>-ai-search.search.windows.net"
SEARCH_API_KEY="<primary-admin-key>"
SEARCH_INDEX_NAME="healthtips-index"
```

> **참고**: 인덱스는 노트북 03이 코드로 직접 생성하므로 포털에서 미리 만들 필요가 없습니다. AI Search 접근에 관리자 키를 쓰는 것은 실습 편의를 위한 것으로, 운영 환경에서는 AI Search도 [Entra ID 인증](https://learn.microsoft.com/azure/search/search-security-rbac)을 권장합니다.

## 검증

세 노트북을 순서대로 실행해 각 노트북 마지막 셀까지 오류 없이 완료되면 성공입니다.

## 정리 (Clean-up)

RAG 실습 후 AI Search 리소스를 계속 쓰지 않는다면 Azure Portal에서 삭제하세요 (Basic 계층도 시간 과금됩니다).

## 다음 단계

→ [05. Agent Service](../05-agent-service/README.md)
