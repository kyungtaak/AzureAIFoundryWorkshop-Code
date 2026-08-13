# AGENTS.md — AI 코딩 에이전트 작업 지시문

이 문서는 GitHub Copilot(및 다른 AI 에이전트)이 이 리포지토리를 점검·유지보수할 때의 기준 지시문이다.
**모든 작업 전에 이 문서와 CHANGELOG.md를 먼저 읽는다.**

> 수강생은 이 문서가 아니라 [README.md](README.md)부터 보면 된다. 여기서부터는 유지보수자용 내용이다.

## 리포지토리 성격

- Microsoft Foundry 입문 핸즈온 워크샵 (한국어, 건강·피트니스 예제)
- [Azure/ai-foundry-workshop](https://github.com/Azure/ai-foundry-workshop) 기반 한국어 워크샵의 포크를 현행화한 것

## 수행된 표준화 작업 (2026-08-12, modernize-standardize 브랜치)

상세 내역과 근거 출처는 [CHANGELOG.md](CHANGELOG.md) 참고. 요약:

1. **콘텐츠 최신화**: `azure-ai-inference`(2026-05-30 retired) → `openai` SDK, API Key → Entra ID(`DefaultAzureCredential`), azure-ai-projects 2.4.0, Agent Service를 Assistants(threads/runs) → **Conversations + Responses API**로 마이그레이션, gpt-4o(Deprecated) → **gpt-5-mini**, 신규 Microsoft Foundry 포털 기준으로 문서 갱신
2. **구조 표준화**: 공백·한글 폴더명 → kebab-case + 번호 접두어(`01-setup` ~ `05-agent-service`), 노트북 파일명 `01-*.ipynb` 형식
3. **메타데이터**: 루트 README에 frontmatter 전체 스키마, 각 장 README에 축약 frontmatter(title/duration_minutes/last_updated)
4. **실행 환경**: `.devcontainer` + "Open in Codespaces" 뱃지, `requirements.txt` 버전 고정
5. **거버넌스**: LICENSE(MIT, 코드) + LICENSE-DOCS(CC BY-SA 4.0, 문서), CHANGELOG
6. **문서 템플릿**: 각 장 = 개요/학습 목표 → 사전 요구사항 → 단계 → 검증 → (정리) → 트러블슈팅 → 다음 단계
7. 구(클래식) 포털 스크린샷 9장 제거 (신규 포털 기준 텍스트 절차로 대체)

## 지켜야 할 표준 규약 (수정 작업 시 유지)

- **frontmatter**: 루트 README의 필드 셋 유지. `last_updated`는 내용 수정 시 갱신, `validated_on`은 **실제 E2E 실행 검증을 한 사람만** 기입
- **명명**: 새 파일·폴더는 kebab-case 영문 + 번호 접두어. 공백·한글 경로 금지
- **노트북**: 출력(outputs)은 클리어 상태로 커밋. 설명 md 셀은 한국어, 코드·식별자는 영어. 각 노트북 첫 코드 셀은 `.env` 로드 + 클라이언트 초기화
- **SDK 원칙**: `azure-ai-inference`·API Key 인증·Assistants API(threads/runs) 패턴을 **재도입하지 않는다** (모두 retired/sunset). 모델은 retirement 일정 확인 후 GA 상태만 사용
- **언어 정책**: 문서·노트북 설명 한국어 + 기술 용어 영문 병기

## 검증 하네스 (변경 후 반드시 실행)

`.github/scripts/verify.py` 하나로 3종 검사를 실행한다. Windows·macOS·Linux 동일하게 동작한다.

```bash
pip install -r requirements.txt nbformat pyyaml
python .github/scripts/verify.py            # 전체
python .github/scripts/verify.py --only docs  # 일부만 (notebooks | docs | imports)
```

검사 내용:

1. **notebooks** — 모든 `.ipynb`의 nbformat 스키마 유효성, 코드 셀 문법(`ast.parse`), 출력(outputs) 클리어 여부
2. **docs** — 모든 `.md`의 frontmatter YAML 파싱, 상대 링크 대상 파일 존재 여부
3. **imports** — `azure-ai-projects` / `openai` / `azure-identity` / `azure-search-documents` 임포트와 `PromptAgentDefinition`, `openai` 클라이언트의 `chat`·`embeddings`·`responses`·`conversations` 속성 존재 확인 (실제 API 호출 없음)

실패가 하나라도 있으면 exit code 1을 반환한다.

## 남은 작업 (백로그)

1. 신규 Foundry 포털 스크린샷 재캡처 (02·03장의 핵심 단계만 최소한으로, alt-text 필수)

## E2E 실행 검증 (2026-08-12 완료)

04·05장 노트북 4개를 실제 Azure 리소스로 끝까지 실행해 통과했다. 재실행 절차:

1. `az login` 후 `.env` 구성 (`.env.example` 참고)
2. `pip install nbconvert ipykernel` 및 커널 등록
3. `python -m nbconvert --to notebook --execute --output-dir <임시폴더> <노트북>` — 출력을 임시 폴더로 보내 리포의 노트북은 클리어 상태로 유지한다

검증 중 확인된 API 제약 (수정 시 되돌리지 말 것):

- **임베딩은 리소스 범위 엔드포인트를 써야 한다.** `project.get_openai_client()`의 프로젝트 범위 base_url `{PROJECT_ENDPOINT}/openai/v1` 에는 `/embeddings` 라우트가 없어 404가 난다. 04장 02·03 노트북은 `base_url`을 `https://<resource>.services.ai.azure.com/openai/v1` 로 오버라이드한 `embedding_client`를 별도로 만들어 쓴다. chat·responses·conversations는 프로젝트 범위 그대로 동작한다.

## DO NOT

- DO NOT: 하네스(위 3개 검증) 실패 상태로 커밋
- DO NOT: retired SDK 패턴(azure-ai-inference, API Key, threads/runs) 재도입
- DO NOT: E2E 실행 없이 `validated_on` 기입
- DO NOT: frontmatter·LICENSE·CHANGELOG 삭제 또는 약화
- DO NOT: main에 직접 커밋 (브랜치 → PR 검토 후 머지)
