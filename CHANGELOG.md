# CHANGELOG

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

### 표준화 (팀 워크샵 콘텐츠 규약 적용)

- 폴더·파일 kebab-case 영문 + 번호 접두어 (`1. 사전 준비/` → `01-setup/`)
- 루트 README frontmatter(메타데이터) + 각 장 README 축약 frontmatter 추가
- `.devcontainer` + "Open in Codespaces" 뱃지 (Codespaces 기본, 로컬 Dev Container 보조)
- `requirements.txt` 버전 고정 (재현성)
- LICENSE(MIT) + LICENSE-DOCS(CC BY-SA 4.0) 추가
- 장 문서 템플릿 적용: 개요/학습 목표 → 사전 요구사항 → 단계 → 검증 → 다음 단계
- 구(클래식) 포털 스크린샷 제거 → 텍스트 절차로 대체 (신규 포털 스크린샷은 실행 검증 시 재캡처 권장)

### 미검증 항목 (validated_on 미기입 사유)

- 실제 Azure 구독으로 E2E 실행 검증은 수행되지 않음. 코드·절차는 2026-08-12 기준 공식 문서와 SDK 2.4.0 API 표면 검사로 확인됨.
- 첫 E2E 실행 후 루트 README frontmatter의 `validated_on`을 기입할 것.
- Korea Central 리전의 gpt-5-mini 배포 타입(Global Standard 권장)은 배포 시점에 포털에서 확인 필요.
