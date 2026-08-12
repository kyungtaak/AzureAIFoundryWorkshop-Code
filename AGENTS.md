# AGENTS.md — AI 코딩 에이전트 작업 지시문

이 문서는 GitHub Copilot(및 다른 AI 에이전트)이 이 리포지토리를 점검·유지보수할 때의 기준 지시문이다.
**모든 작업 전에 이 문서와 CHANGELOG.md를 먼저 읽는다.**

## 리포지토리 성격

- Microsoft Foundry 입문 핸즈온 워크샵 (한국어, 건강·피트니스 예제)
- [Azure/ai-foundry-workshop](https://github.com/Azure/ai-foundry-workshop) 기반 한국어 워크샵의 포크를 현행화한 것
- **팀 워크샵 콘텐츠 표준의 첫 파일럿 적용 리포** — 여기서 검증된 규약이 팀 표준 템플릿의 기반이 된다

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

```bash
pip install -r requirements.txt nbformat pyyaml

# 1) 노트북 유효성 + 코드 문법
python - <<'EOF'
import nbformat, glob, ast, sys
ok = True
for f in glob.glob('**/*.ipynb', recursive=True):
    nb = nbformat.read(f, as_version=4)
    nbformat.validate(nb)
    for c in nb.cells:
        if c.cell_type == 'code' and c.get('outputs'):
            ok = False; print(f"❌ {f}: 출력이 클리어되지 않은 셀 존재")
        if c.cell_type == 'code':
            try: ast.parse(c.source)
            except SyntaxError as e: ok = False; print(f"❌ {f}: {e}")
    print(f"✅ {f}")
sys.exit(0 if ok else 1)
EOF

# 2) frontmatter 파싱 + 상대 링크 생존 확인
python - <<'EOF'
import re, os, glob, yaml, sys
errors = []
for f in glob.glob('**/README.md', recursive=True) + ['README.md', 'CHANGELOG.md']:
    if not os.path.exists(f): continue
    text = open(f, encoding='utf-8').read()
    if text.startswith('---'):
        try: yaml.safe_load(text.split('---')[1])
        except Exception as e: errors.append(f"{f}: frontmatter 오류 {e}")
    for m in re.finditer(r'\]\((?!http|#)([^)]+)\)', text):
        t = os.path.normpath(os.path.join(os.path.dirname(f), m.group(1).split('#')[0]))
        if t and not os.path.exists(t): errors.append(f"{f}: 깨진 링크 → {m.group(1)}")
print("\n".join(errors) or "✅ frontmatter·링크 정상")
sys.exit(1 if errors else 0)
EOF

# 3) 임포트 스모크 테스트 (API 호출 없음)
python -c "import azure.ai.projects, openai, azure.identity, azure.search.documents; from azure.ai.projects.models import PromptAgentDefinition; print('✅ SDK imports OK')"
```

## 남은 작업 (백로그)

1. **[1순위] E2E 실행 검증** — Azure 구독으로 01→05장 전체를 실제 실행. 오류 수정 후 루트 README frontmatter의 `validated_on` 기입. 코드는 SDK 2.4.0 API 표면 검사까지만 검증된 상태(실 리소스 미검증)이므로, 특히 다음을 주의 깊게 확인:
   - `03-basic-rag.ipynb`의 azure-search-documents 12.0 동작 (11.x 대비 breaking change 가능)
   - `01-agent-basics.ipynb`의 conversations items 나열 부분(응답 객체 구조가 SDK 버전에 따라 다를 수 있음)
2. 신규 Foundry 포털 스크린샷 재캡처 (02·03장의 핵심 단계만 최소한으로, alt-text 필수)
3. E2E 검증 통과 후 팀 카탈로그(workshop-viewer-poc)의 `data/external.yml`에 entry 등록

## DO NOT

- DO NOT: 하네스(위 3개 검증) 실패 상태로 커밋
- DO NOT: retired SDK 패턴(azure-ai-inference, API Key, threads/runs) 재도입
- DO NOT: E2E 실행 없이 `validated_on` 기입
- DO NOT: frontmatter·LICENSE·CHANGELOG 삭제 또는 약화
- DO NOT: main에 직접 커밋 (브랜치 → PR 검토 후 머지)
