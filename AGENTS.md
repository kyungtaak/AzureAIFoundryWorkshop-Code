# AGENTS.md — AI 코딩 에이전트 작업 지시문

이 문서는 GitHub Copilot(및 다른 AI 에이전트)이 이 리포지토리를 점검·유지보수할 때의 기준 지시문이다.
**모든 작업 전에 이 문서와 CHANGELOG.md를 먼저 읽는다.**

> 수강생은 이 문서가 아니라 [README.md](README.md)부터 보면 된다. 여기서부터는 유지보수자용 내용이다.

## 리포지토리 성격

- Microsoft Foundry 입문 핸즈온 워크샵 (한국어, 건강·피트니스 예제)
- [Azure/ai-foundry-workshop](https://github.com/Azure/ai-foundry-workshop) 기반 한국어 워크샵의 포크를 현행화한 것

이 문서는 아래 네 개 섹션으로 구성한다. ① 리포 규칙 → ② 콘텐츠·노트북 스타일 가이드 → ③ 검증 하네스 → ④ 백로그·DO NOT

---

## 1. 리포 규칙

- **시크릿 커밋 금지**: API 키·엔드포인트·토큰·구독 ID를 파일에 남기지 않는다. 설정 값은 `.env`(gitignore 대상)와 `.env.example`(플레이스홀더만)로 분리한다.
- **수정 금지 파일**: `LICENSE`(MIT, 코드)와 `LICENSE-DOCS`(CC BY-SA 4.0, 문서)는 변경·삭제하지 않는다. `CHANGELOG.md`는 항목 추가만 하고 기존 이력을 고쳐 쓰지 않는다.
- **노트북 출력 클리어 커밋**: 모든 `.ipynb`는 outputs가 비어 있는 상태로 커밋한다. 실행 검증이 필요하면 `nbconvert --execute`의 출력을 리포 밖 임시 폴더로 보낸다.
- **대용량 바이너리 금지**: 이미지·데이터셋·모델 파일 등 대용량 바이너리를 커밋하지 않는다. 스크린샷은 꼭 필요한 단계만 최소 용량으로 추가하고 alt-text를 붙인다.
- **명명 규칙**: 새 파일·폴더는 kebab-case 영문 + 번호 접두어(`01-setup` ~ `05-agent-service`, 노트북은 `01-*.ipynb`). 공백·한글 경로를 쓰지 않는다.
- **브랜치·커밋**: `main`에 직접 커밋하지 않는다. 작업 브랜치에서 커밋하고 PR로 검토받는다.
- **frontmatter**: 루트 README의 필드 셋을 유지한다. `last_updated`는 내용 수정 시 갱신하고, `validated_on`은 실제 E2E 실행 검증을 한 사람만 기입한다.
- **SDK 원칙**: `azure-ai-inference`·API Key 인증·Assistants API(threads/runs) 패턴은 모두 retired 또는 sunset이므로 재도입하지 않는다. 모델은 retirement 일정을 확인해 GA 상태만 사용한다.

### 표준화 이력 요약 (2026-08-12, modernize-standardize 브랜치)

상세 내역과 근거 출처는 [CHANGELOG.md](CHANGELOG.md) 참고. 요약:

1. **콘텐츠 최신화**: `azure-ai-inference`(2026-05-30 retired) → `openai` SDK, API Key → Entra ID(`DefaultAzureCredential`), azure-ai-projects 2.4.0, Agent Service를 Assistants(threads/runs) → **Conversations + Responses API**로 마이그레이션, gpt-4o(Deprecated) → **gpt-5-mini**, 신규 Microsoft Foundry 포털 기준으로 문서 갱신
2. **구조 표준화**: 공백·한글 폴더명 → kebab-case + 번호 접두어(`01-setup` ~ `05-agent-service`), 노트북 파일명 `01-*.ipynb` 형식
3. **메타데이터**: 루트 README에 frontmatter 전체 스키마, 각 장 README에 축약 frontmatter(title/duration_minutes/last_updated)
4. **실행 환경**: `.devcontainer` + "Open in Codespaces" 뱃지, `requirements.txt` 버전 고정
5. **거버넌스**: LICENSE(MIT, 코드) + LICENSE-DOCS(CC BY-SA 4.0, 문서), CHANGELOG
6. **문서 템플릿**: 각 장 = 개요/학습 목표 → 사전 요구사항 → 단계 → 검증 → (정리) → 트러블슈팅 → 다음 단계
7. 구(클래식) 포털 스크린샷 9장 제거 (신규 포털 기준 텍스트 절차로 대체)

---

## 2. 콘텐츠·노트북 스타일 가이드

### 2.1 노트북 셀 구조 템플릿

모든 실습 노트북(`**/*.ipynb`)은 아래 구조를 따른다.

**첫 셀 (markdown)** — 제목 + 시나리오 도입 + 미션 목록

- `#` 하나짜리 제목으로 시작한다.
- 시나리오 도입 문단으로 **왜 배우는지**를 먼저 설명한다. 기능 나열이 아니라 수강생이 처한 상황을 그린다.
- `**🎯 미션**` 목록을 1~3개 항목으로 적는다. 각 항목은 이 노트북에서 실제로 만들어 내는 결과물과 일치해야 한다.
- 사전 준비와 주의 문구(건강 관련 안내 등)는 미션 목록 뒤에 인용문(`>`)으로 둔다.

```markdown
# 노트북 제목

시나리오 도입 문단. 수강생이 어떤 상황에 있고 이 노트북이 무엇을 해결하는지 설명한다.

**🎯 미션**

1. 첫 번째로 만들 것
2. 두 번째로 만들 것

> **사전 준비**: ...
```

**본문** — `## 1.` `## 2.` 형태로 번호를 매긴 단계 헤딩을 유지한다. 하위 단계가 필요하면 `### 5.1` 처럼 번호를 이어 쓴다.

**마지막 셀 (markdown)** — 미션 완료 정리

- `## ✅ 미션 완료` 헤딩으로 시작한다.
- `**무엇을 만들었나:**` 아래에 `✓` 목록을 적는다. 항목은 첫 셀의 미션과 하나씩 대응시킨다.
- 마지막에 다음 노트북 또는 다음 장으로 가는 링크를 둔다.

```markdown
## ✅ 미션 완료

**무엇을 만들었나:**

- ✓ 첫 번째 미션의 결과물
- ✓ 두 번째 미션의 결과물

다음 노트북에서는 ... → [02-embeddings.ipynb](02-embeddings.ipynb)
```

**문체 규칙**

- 산문 설명에서 세미콜론(`;`)과 엠 대시(`—`)를 쓰지 않는다. 문장을 나눈다.
- 일반 대시(`-`)는 목록 기호로만 쓴다.
- 첫 코드 셀은 `.env` 로드와 클라이언트 초기화로 시작한다.

### 2.2 언어 정책

- 설명 markdown 셀과 문서는 **한국어**로 쓰고, 기술 용어는 영문을 병기한다 (예: 의미적 유사도(semantic similarity)).
- 코드·식별자·변수명·파일명은 **영어**로 쓴다.
- 코드 주석은 한국어를 허용하되, 코드가 스스로 드러내지 못하는 내용만 한 줄로 적는다.

### 2.3 랩 README 페어링 규약

각 장 폴더는 `README.md` 하나를 두고 그 장의 노트북과 짝을 이룬다. README 구성은 다음 순서를 지킨다.

1. **frontmatter** — `title`, `duration_minutes`, `last_updated` (루트 README는 전체 스키마 유지)
2. **개요 · 학습 목표**
3. **노트북 목차 표** — 노트북 파일 링크 / 내용 / 소요 시간 열
4. **사전 요구사항** (해당 장에 필요한 경우)
5. **단계별 절차** (포털 작업 등 노트북 밖 작업이 있는 경우)
6. **검증** — 무엇이 되면 성공인지
7. **정리 (Clean-up)** — 과금이 발생하는 리소스가 있는 경우 필수
8. **트러블슈팅** (필요한 경우)
9. **다음 단계** — 다음 장 README 링크

---

## 3. 검증 하네스

`.github/scripts/verify.py` 하나로 모든 검사를 실행한다. Windows·macOS·Linux에서 동일하게 동작한다. 검증 절차를 다른 문서나 워크플로에 다시 적지 않고 이 스크립트를 참조한다.

```bash
pip install -r requirements.txt nbformat pyyaml
python .github/scripts/verify.py              # 전체
python .github/scripts/verify.py --only docs  # 일부만 (notebooks | structure | docs | imports)
```

검사 내용:

1. **notebooks** — 모든 `.ipynb`의 nbformat 스키마 유효성, 코드 셀 문법(`ast.parse`), 출력(outputs) 클리어 여부
2. **structure** — 첫 셀이 markdown이면서 `🎯` 미션 목록을 포함하는지, 마지막 셀이 markdown이면서 `✅ 미션 완료`를 포함하는지 (2.1 셀 구조 템플릿 준수 여부)
3. **docs** — 모든 `.md`의 frontmatter YAML 파싱, 상대 링크 대상 파일 존재 여부
4. **imports** — `azure-ai-projects` / `openai` / `azure-identity` / `azure-search-documents` 임포트와 `PromptAgentDefinition`, `openai` 클라이언트의 `chat`·`embeddings`·`responses`·`conversations` 속성 존재 확인 (실제 API 호출 없음)

실패가 하나라도 있으면 exit code 1을 반환한다.

### E2E 실행 검증 (2026-08-12 완료)

04·05장 노트북 4개를 실제 Azure 리소스로 끝까지 실행해 통과했다. 재실행 절차:

1. `az login` 후 `.env` 구성 (`.env.example` 참고)
2. `pip install nbconvert ipykernel` 및 커널 등록
3. `python -m nbconvert --to notebook --execute --output-dir <임시폴더> <노트북>` — 출력을 임시 폴더로 보내 리포의 노트북은 클리어 상태로 유지한다

검증 중 확인된 API 제약 (수정 시 되돌리지 말 것):

- **임베딩은 리소스 범위 엔드포인트를 써야 한다.** `project.get_openai_client()`의 프로젝트 범위 base_url `{PROJECT_ENDPOINT}/openai/v1` 에는 `/embeddings` 라우트가 없어 404가 난다. 04장 02·03 노트북은 `base_url`을 `https://<resource>.services.ai.azure.com/openai/v1` 로 오버라이드한 `embedding_client`를 별도로 만들어 쓴다. chat·responses·conversations는 프로젝트 범위 그대로 동작한다.

---

## 4. 백로그 · DO NOT

### 백로그

1. 신규 Foundry 포털 스크린샷 재캡처 (02·03장의 핵심 단계만 최소한으로, alt-text 필수)
2. 04·05장 노트북 E2E 재검증 후 루트 README의 `validated_on` 갱신

### DO NOT

- DO NOT: 하네스(`.github/scripts/verify.py`) 실패 상태로 커밋
- DO NOT: retired SDK 패턴(azure-ai-inference, API Key, threads/runs) 재도입
- DO NOT: E2E 실행 없이 `validated_on` 기입
- DO NOT: frontmatter·LICENSE·CHANGELOG 삭제 또는 약화
- DO NOT: main에 직접 커밋 (브랜치 → PR 검토 후 머지)
- DO NOT: 시크릿·대용량 바이너리 커밋
