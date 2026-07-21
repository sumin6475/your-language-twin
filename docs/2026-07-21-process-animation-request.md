# 요청서 — Process 애니메이션 개선 (해커톤 데모용)

**대상 파일**
- `web/components/ProcessingVisualizer.tsx` (메인)
- `web/app/app/page.tsx` (라우팅/타이밍 조정)
- `web/app/globals.css` (체크 완료 애니메이션 추가)

**목표 한 줄**
각 스텝이 순서대로 "완료(스피너 → 체크)"되는 느낌을 주기. 애니메이션은 백엔드와 분리해 고정 타이머로 돌리고, **마지막 스텝만** 실제 백엔드 완료에 sync.

---

## 1. 지금 상태 (문제 진단)

- 스텝은 총 **5개**: 에이전트 카드 4개 (`agents` 배열) + `Confidence check` 카드 1개. 그 아래 "Building your Language Twin…"는 스텝이 아니라 푸터.
- 현재 애니메이션은 **CSS 뿐**: 카드가 `lrm-rise`로 시차를 두고 등장하는 게 전부. 상태(state)가 없음.
- **핵심 버그**: 모든 카드의 스피너가 `lrm-spin … infinite`라서 **영원히 돌기만 하고 완료로 안 바뀜**. → "각 단계가 안 돌아가는 것처럼", "느린 것처럼" 보이는 원인.
- `page.tsx`는 `MIN_PROCESSING_MS = 5200`만 보장하고, 백엔드 `/match` 응답이 그보다 오래 걸리면 화면은 그냥 다 돌고만 있음.

## 2. 원하는 동작 (해커톤 = "느낌"만)

지금은 **진짜 에이전트 진행에 묶지 말고** 타이머로 순차 완료 느낌만 준다. (진짜 스트리밍 sync는 나중에 = out of scope, 아래 5번 참고.)

## 3. 상세 스펙 (상태 머신)

**스텝 상태**: 각 스텝은 `pending` | `active`(스피너) | `done`(체크) 중 하나.

**진행 규칙**
- 마운트 시: 스텝 0 = `active`, 나머지 = `pending`.
- `STEP_INTERVAL_MS`(기본 2000ms)마다: 현재 `active` 스텝 → `done`, 다음 스텝 → `active`.
- 스텝 0~3 (에이전트 4개)는 **타이머로만** 순차 진행/완료.
- 스텝 4 (`Confidence check`)는 타이머로 `active`가 되지만 **자동 완료 안 함**. 실제 백엔드 결과가 준비될 때까지 `active`(스피너) 유지.

**마지막 스텝 sync (이 설계의 핵심)**
- 백엔드 응답 도착 **AND** 스텝 4가 `active` → 스텝 4를 `done`으로, 푸터 "Building your Language Twin…" 약 600ms 노출 후 결과 페이지로 이동.
- 백엔드가 스텝 4 도달 **전에** 끝나면 → 결과는 들고만 있고, 타이머가 스텝 4까지 따라온 뒤에 완료 처리 (너무 빨리 끝나 어색해지는 것 방지).
- 백엔드가 스텝 4 도달 시점에 **아직 안 끝났으면** → 스텝 4 스피너 유지 (이건 실제 검증 단계라 정직하게 기다려도 자연스러움). 선택: "still checking…" 같은 문구 살짝.

**타이밍 정리**
- 스텝 0~3은 약 8초 안에 순차 완료 (`STEP_INTERVAL_MS` = 2000 기준). 값은 상수 하나로 빼서 조정 가능하게 (예: 1800~2000).
- 실제 총 대기는 대부분 스텝 4(백엔드)가 결정. 즉 스텝퍼가 곧 최소 대기시간이 되므로 `MIN_PROCESSING_MS`는 제거하거나 스텝퍼 완료 조건으로 대체.

## 4. 시각 처리

- `active`: 지금 스피너 그대로.
- `done`: 스피너를 파란 원 배경 + 흰 체크로 교체. 살짝 pop 되면 진행감이 산다 (`lrm-pop` 재사용 가능). 완료된 카드 텍스트는 톤 다운(선택).
- `pending`: 카드는 보이되 스피너 대신 빈 회색 원(`--border`), 텍스트 흐리게. (또는 지금처럼 등장 시차만 유지해도 됨.)
- 접근성: `@media (prefers-reduced-motion)`에서 스피너/전환 없이 상태만 바뀌게 (globals.css에 이미 reduced-motion 블록 있음 — done 상태도 여기 반영).

## 5. 연결 방식 (권장안)

스텝퍼 로직을 `ProcessingVisualizer`가 소유하게 하고, `page.tsx`와 이렇게 연결:

- `page.tsx`: 백엔드 응답 오면 `backendReady` 상태 true. `ProcessingVisualizer`에 prop 두 개 전달 — `backendReady: boolean`, `onFinished: () => void`.
- `ProcessingVisualizer`: 내부에서 스텝퍼 타이머 돌리고, 스텝 4까지 `done` 되면(위 sync 규칙) `onFinished()` 호출.
- `page.tsx`: `onFinished`에서 `sessionStorage` 저장 + `router.push("/app/results")`.
- 기존 `MIN_PROCESSING_MS` 고정 대기는 삭제 (스텝퍼가 최소 시간 역할).
- 에러 케이스는 지금 로직 유지 (에러 메시지 그래이스풀 노출).

`useEffect`로 `setInterval` 돌리고 언마운트/`prefers-reduced-motion`에서 정리(clear)하는 것 잊지 말 것.

## 6. Out of scope (나중에)

- 실제 각 에이전트 완료 이벤트에 스텝을 묶는 진짜 스트리밍 sync. 지금은 "느낌"만.

## 7. Acceptance criteria (완료 기준)

- [ ] 스텝 0~3이 약 2초 간격으로 스피너 → 체크로 **순차 완료**된다.
- [ ] 스텝 4는 백엔드 응답 전까지 스피너 유지, 응답 오면 체크 후 결과 페이지로 이동.
- [ ] 백엔드가 스텝퍼보다 빨리 끝나도 애니가 갑자기 점프하지 않는다 (스텝 4까지 따라온 뒤 완료).
- [ ] 백엔드가 느려도 화면이 "멈춘 것"처럼 안 보인다 (앞 스텝들은 이미 체크 완료 상태).
- [ ] `prefers-reduced-motion`에서 깨지지 않는다.
- [ ] 콘솔 에러/타이머 누수 없음 (언마운트 시 clear).

---

**튜닝 상수**: `STEP_INTERVAL_MS` (기본 2000), 푸터 노출 딜레이 (기본 600).
