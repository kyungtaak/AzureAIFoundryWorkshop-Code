---
title: 05. Foundry Agent Service 기초
duration_minutes: 40
last_updated: 2026-08-12
---

# 05. Foundry Agent Service 기초

## 개요 · 학습 목표

**Microsoft Foundry Agent Service**로 건강·피트니스 어드바이저 에이전트를 만들고 대화합니다.

- `PromptAgentDefinition`으로 에이전트 정의·버전 생성
- **Conversations + Responses API**로 대화 관리 (구 Assistants 방식의 thread/run을 대체)
- 에이전트 정리(삭제)

| 노트북 | 내용 |
|--------|------|
| [01-agent-basics.ipynb](01-agent-basics.ipynb) | 에이전트 생성 → 대화 → 정리 전체 흐름 |

> **변경 참고**: 이전 버전 워크샵의 `create_agent` / `threads` / `runs` 패턴(Assistants API 기반)은 2026-08-26 서비스 종료(sunset)되어 최신 패턴으로 전면 교체되었습니다. 자세한 내용은 [CHANGELOG](../CHANGELOG.md)와 [공식 마이그레이션 문서](https://learn.microsoft.com/azure/foundry/agents/how-to/migrate)를 참고하세요.

## 사전 요구사항

- [03. 인증 구성](../03-authentication/README.md) 완료 (`az login` + `.env`의 `PROJECT_ENDPOINT`, `MODEL_NAME`)
- gpt-5-mini 모델 배포 ([02장](../02-foundry-project/README.md))

## 검증

노트북 마지막의 정리 셀까지 실행 후, Foundry 포털 **Build > Agents**에서 에이전트가 삭제되었는지 확인하면 완료입니다.

## 정리 (Clean-up)

- 노트북의 정리 셀이 에이전트를 삭제합니다. 남아 있다면 포털 **Build > Agents**에서 수동 삭제하세요.
- 워크샵 전체를 마쳤다면 리소스 그룹을 삭제해 과금을 방지하세요.
