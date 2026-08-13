---
title: 02. Microsoft Foundry 프로젝트 구성
duration_minutes: 20
last_updated: 2026-08-12
---

# 02. Microsoft Foundry 프로젝트 구성

## 개요 · 학습 목표

[Microsoft Foundry 포털](https://ai.azure.com)에서 프로젝트를 만들고, 실습에 사용할 chat 모델(**gpt-5-mini**)과 임베딩 모델(**text-embedding-3-small**)을 배포합니다.

> **참고**: 2025년 말 "Azure AI Foundry"가 **Microsoft Foundry**로 리브랜드되면서 포털 화면이 개편되었습니다. 이 문서는 **신규 포털** 기준입니다. 화면이 다르면 포털 상단 배너에서 "New Foundry" 토글을 확인하세요. SaaS 특성상 메뉴 위치는 이후에도 바뀔 수 있습니다.

## 프로젝트 생성

1. [Microsoft Foundry 포털](https://ai.azure.com)에 로그인합니다.
2. **Create new**(새로 만들기)를 클릭해 새 프로젝트를 만듭니다.
3. 프로젝트 이름에 `<alias>-<date>`를 입력합니다. (예: `jayden-0812`)
4. Region은 `Korea Central`(또는 사용 가능한 인근 리전)을 선택하고 **Create**를 클릭합니다.
5. 리소스 생성에는 약 2분이 소요됩니다. 권한 안내(Fix me 등)가 표시되면 클릭해 사용자 권한을 할당합니다.
6. 프로젝트 **Overview** 화면에서 **프로젝트 엔드포인트**를 확인해 둡니다 — [03. 인증 구성](../03-authentication/README.md)에서 사용합니다.
   - 형식: `https://<resource>.services.ai.azure.com/api/projects/<project-name>`

## Chat 모델 배포 (gpt-5-mini)

1. 프로젝트 왼쪽 메뉴에서 **Build > Models**로 이동합니다. (구 포털의 "Models + endpoints"에 해당)
2. **Deploy model > Deploy base model**을 선택합니다.
3. 모델 리스트에서 `gpt-5-mini`를 선택하고 **Confirm**을 클릭합니다.
   - 배포 타입은 **Global Standard**를 권장합니다 (리전 제약 완화).
4. 배포 이름(기본값 `gpt-5-mini`)을 확인하고 **Deploy**를 클릭합니다.

> **참고**: 이전 버전 워크샵에서 사용하던 `gpt-4o`는 Deprecated 상태로 신규 배포가 제한됩니다. gpt-5 계열(gpt-5-mini, gpt-5.1 등)을 사용하세요.

## 임베딩 모델 배포 (text-embedding-3-small)

1. 같은 방법으로 **Build > Models > Deploy model**을 클릭합니다.
2. 모델 리스트에서 `text-embedding-3-small`을 선택하고 **Confirm** → **Deploy**를 클릭합니다.

## 검증

- **Build > Models**에 두 배포(`gpt-5-mini`, `text-embedding-3-small`)가 **Succeeded** 상태로 표시되면 완료입니다.
- 각 **배포 이름**을 메모하세요 — `.env`의 `MODEL_NAME`, `TEXT_EMBEDDING_MODEL` 값이 됩니다.

## 트러블슈팅

- **모델이 리스트에 없음**: 선택한 리전에서 미지원일 수 있습니다. 배포 타입을 Global Standard로 바꾸거나 [리전별 가용성](https://learn.microsoft.com/azure/foundry/foundry-models/concepts/models-sold-directly-by-azure-region-availability)을 확인하세요.
- **권한 오류**: 구독에서 Foundry 리소스 생성 권한(Contributor 이상)과 프로젝트 사용자 역할이 있는지 확인하세요.

## 다음 단계

→ [03. 인증 구성](../03-authentication/README.md)
