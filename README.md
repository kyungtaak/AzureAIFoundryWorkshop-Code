---
type: workshop
title: Microsoft Foundry Workshop (Code)
description: Microsoft Foundry에서 Python으로 Chat Completions·Embeddings·RAG·에이전트를 구축하는 입문 핸즈온 (건강·피트니스 예제)
level: beginner
authors: [Kyungtaak Noh]
contacts: ["@kyungtaak"]
duration_minutes: 180
tags: [foundry, azure-openai, rag, agent, ai-search]
language: ko
execution: [codespaces, local]
status: active
source: "localized: Azure/ai-foundry-workshop"
last_updated: 2026-08-20
validated_on: 2026-08-12
---

# Microsoft Foundry Workshop (Code)

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/kyungtaak/AzureAIFoundryWorkshop-Code)

## 개요

이 워크샵은 **Microsoft Foundry**(구 Azure AI Foundry)를 기반으로 지능형 애플리케이션과 AI 에이전트를 구축하는 실습 중심의 과정을 제공합니다.
건강 및 식단 조언과 관련된 재미있는 예제를 통해 다음을 학습합니다:

- Microsoft Foundry의 기본 개념 이해
- Entra ID 기반 인증 및 프로젝트 설정 구성
- AI 모델 배포 및 테스트 (Chat Completions · Embeddings)
- Azure AI Search를 활용한 기본 RAG 구현
- Foundry Agent Service로 AI 에이전트 구축 (건강 조언 에이전트 예제)

> **소요 시간**: 약 3시간 · **난이도**: 입문
> **중점**: 실습 과제, 대화형 노트북, 실용적인 예제

## 사전 준비 사항

- 활성화된 Azure 구독과 [Microsoft Foundry 포털](https://ai.azure.com) 접근 권한
- GitHub 계정 (Codespaces 사용 시 — 권장)
- 기본적인 Python 프로그래밍 지식
- 로컬 실행 시: Python 3.11+, [Azure CLI](https://learn.microsoft.com/cli/azure/install-azure-cli), Git, VS Code

## 실습 환경

**권장: GitHub Codespaces** — 상단 뱃지를 클릭하면 `.devcontainer` 정의로 Python·Azure CLI·Jupyter가 준비된 환경이 자동 구성됩니다. 로컬에서 진행하려면 같은 devcontainer를 VS Code Dev Containers로 열거나, [01-setup](01-setup/README.md)의 로컬 구성 절차를 따르세요.

## 워크샵 학습 경로

아래 순서대로 진행하세요.

### 1. 준비

| 단계 | 설명 | 소요 시간 |
|------|------|-----------|
| [01. 실습 환경 구성](01-setup/README.md) | Codespaces 또는 로컬 환경 구성 | 15분 |
| [02. Foundry 프로젝트 구성](02-foundry-project/README.md) | 프로젝트 생성, 모델 배포 (gpt-5-mini, text-embedding-3-small) | 20분 |
| [03. 인증 구성](03-authentication/README.md) | Entra ID(keyless) 인증과 .env 구성 | 15분 |

### 2. 주요 워크샵

| 주제 | 노트북 | 소요 시간 |
|------|--------|-----------|
| **Chat Completion & RAG** | [04. Chat Completion](04-chat-completion/README.md) — 기본 채팅 → 임베딩 → RAG 3개 노트북 | 90분 |
| **Agent Development** | [05. Agent Service](05-agent-service/README.md) — Foundry Agent Service 기초 | 40분 |

## 정리 (Clean-up)

실습 후 과금을 방지하려면 Azure Portal에서 사용한 리소스 그룹(Foundry 리소스, AI Search)을 삭제하세요. 에이전트 삭제는 [05. Agent Service](05-agent-service/README.md)의 정리 절차를 참고하세요.

## 변경 이력

2026-08 기준 최신 SDK·포털로 현행화되었습니다. 무엇이 왜 바뀌었는지는 [CHANGELOG.md](CHANGELOG.md)를 참고하세요.

## 라이선스 · 출처

- 코드: [MIT](LICENSE) · 문서: [CC BY-SA 4.0](LICENSE-DOCS)
- 이 워크샵은 [Azure/ai-foundry-workshop](https://github.com/Azure/ai-foundry-workshop)을 참고하여 재작성한 한국어 워크샵을 현행화한 것입니다.
