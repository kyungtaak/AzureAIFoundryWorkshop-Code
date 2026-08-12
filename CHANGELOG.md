# CHANGELOG

## 2026-08-12 — E2E 실행 검증 + 하네스 점검 수정

### E2E 실행 검증 (validated_on 기입)

실제 Azure 구독의 Foundry 프로젝트(`gpt-5-mini`, `text-embedding-3-small`)와 Azure AI Search로 04·05장 노트북 4개를 `nbconvert --execute`로 끝까지 실행해 통과를 확인했다. 루트 README frontmatter에 `validated_on: 2026-08-12` 기입.

- **임베딩 호출 경로 수정 (04장 02·03 노트북)** — `project.get_openai_client()`가 만드는 **프로젝트 범위** base_url `{endpoint}/openai/v1` 에는 `/embeddings` 라우트가 없어 **404**가 발생한다 (chat/responses/conversations는 정상). 임베딩은 **리소스 범위** `https://<resource>.services.ai.azure.com/openai/v1` 을 써야 한다. 두 노트북에 `embedding_client`(base_url 오버라이드)를 추가하고 임베딩 호출을 전부 여기로 옮김. 01장 노트북의 부정확한 주석도 함께 정정.
- 05장 Agent 노트북(`create_version` + `PromptAgentDefinition` + conversations/responses)은 수정 없이 통과. `get_openai_client(agent_name=...)`가 `allow_preview=True` 없이도 azure-ai-projects 2.4.0에서 동작함을 확인.
- 03장 인증 절차(`AIProjectClient` + `DefaultAzureCredential` + `deployments.list()`)도 실제 프로젝트에서 통과.
- 04장 RAG는 azure-search-documents 12.0.0으로 인덱스 생성·문서 업로드·`VectorizedQuery` 벡터 검색까지 정상 동작 (11.x 대비 breaking change 미발견).

### 하네스 점검 수정

- `requirements.txt`의 `openai==3.0.0` → **`openai==2.53.0`**. PyPI에 3.x 배포가 존재하지 않아(최신 2.53.0) 설치 자체가 실패하던 문제. 노트북이 쓰는 `responses` / `conversations(.items)` / `embeddings` / `chat` API 표면은 2.53.0에 모두 존재함을 확인.
- 검증 하네스를 **`.github/scripts/verify.py`** 로 분리. 기존 AGENTS.md의 bash heredoc은 Windows PowerShell에서 실행되지 않아 Windows·macOS·Linux 공통으로 동작하는 Python 스크립트로 대체. `--only notebooks|docs|imports` 로 부분 실행 가능. AGENTS.md의 하네스 섹션을 이 스크립트 호출로 갱신.
- docs 검사 범위를 `README.md` + `CHANGELOG.md` → 리포지토리의 **모든 `.md`** 로 확대 (AGENTS.md·LICENSE 문서 포함).
- 수강생이 볼 필요 없는 유지보수 도구는 `.github/` 아래로 모아 루트를 README·챕터 폴더 중심으로 유지. AGENTS.md는 [공식 규약](https://agents.md/)상 에이전트가 루트부터 상위 탐색으로 찾기 때문에 루트에 남긴다.

## 2026-08-12 — 표준화 + 최신화 (modernize-standardize 브랜치)

### 콘텐츠 최신화 (2025-07 작성분 → 2026-08 기준)

| 항목 | 변경 전 | 변경 후 | 근거 |
|---|---|---|---|
| SDK (chat/embeddings) | `azure-ai-inference` (ChatCompletionsClient, EmbeddingsClient) | `openai` 패키지 (`project.get_openai_client()`) | azure-ai-inference는 **2026-05-30 retired** — [마이그레이션 가이드](https://learn.microsoft.com/azure/foundry/how-to/model-inference-to-openai-migration) |
| 인증 | API Key (`AzureKeyCredential`) | **Entra ID** (`az login` + `DefaultAzureCredential`) | azure-ai-projects 2.x는 API Key 미지원, [keyless 권장](https://learn.microsoft.com/azure/developer/ai/keyless-connections) |
| azure-ai-projects | 1.x | **2.4.0** (breaking change) | [PyPI](https://pypi.org/project/azure-ai-projects/) |
| Agent Service API | `create_agent` / `threads` / `runs` (Assistants 기반) | `create_version` + `PromptAgentDefinition` + **conversations/responses** | Assistants API **2026-08-26 sunset** — [마이그레이션](https://learn.microsoft.com/azure/foundry/agents/how-to/migrate) |
| Chat 모델 | gpt-4o | **gpt-5-mini** | gpt-4o/4.1 전 버전 Deprecated(신규 배포 제한) — [retirement schedule](https://learn.microsoft.com/azure/foundry/openai/concepts/model-retirement-schedule) |
| 임베딩 모델 | text-embedding-3-small | 유지 (은퇴 2028-02-09) | 동일 문서 |
| azure-search-documents | 11.x | **12.0.0** (임포트 호환 확인) | [PyPI](https://pypi.org/project/azure-search-documents/) |
| 브랜드/포털 | "Azure AI Foundry", Models + endpoints 메뉴 | **"Microsoft Foundry"**, 신규 포털 **Build > Models** | [포털 마이그레이션 문서](https://learn.microsoft.com/azure/foundry/how-to/navigate-from-classic) |
| .env | ENDPOINT + API_KEY 중심 | PROJECT_ENDPOINT 중심 (키 제거) | 위 인증 변경에 따름 |

### 리포지토리 구조 정비

- 폴더·파일 kebab-case 영문 + 번호 접두어 (`1. 사전 준비/` → `01-setup/`)
- 루트 README frontmatter(메타데이터) + 각 장 README 축약 frontmatter 추가
- `.devcontainer` + "Open in Codespaces" 뱃지 (Codespaces 기본, 로컬 Dev Container 보조)
- `requirements.txt` 버전 고정 (재현성)
- LICENSE(MIT) + LICENSE-DOCS(CC BY-SA 4.0) 추가
- 장 문서 템플릿 적용: 개요/학습 목표 → 사전 요구사항 → 단계 → 검증 → 다음 단계
- 구(클래식) 포털 스크린샷 제거 → 텍스트 절차로 대체 (신규 포털 스크린샷은 실행 검증 시 재캡처 권장)

### 미검증 항목 (validated_on 미기입 사유)

> 이 시점의 상태이며, E2E 실행 검증은 같은 날 별도로 완료되었다 (위 "E2E 실행 검증" 항목 참고).

- 실제 Azure 구독으로 E2E 실행 검증은 수행되지 않음. 코드·절차는 2026-08-12 기준 공식 문서와 SDK 2.4.0 API 표면 검사로 확인됨.
- 첫 E2E 실행 후 루트 README frontmatter의 `validated_on`을 기입할 것.
- Korea Central 리전의 gpt-5-mini 배포 타입(Global Standard 권장)은 배포 시점에 포털에서 확인 필요.
