# Plan-Stage Architecture Prompts — demo-scoped

*2026-07-20. Copy-paste prompts for the plan stage: design the multi-agent architecture cleanly,
without over-engineering it into a production concurrency system. Paste one prompt at a time, review
the output against the checklist under it, then paste the next. Pairs with
`2026-07-20-strategy-ai-role-model-engine.md` (the strategy) and `2026-07-20-session-context-primer.md`
(the background). Load both of those into the plan session first; these prompts assume they are in
context.*

---

## How to use this file

1. Open the plan session with the **primer + strategy doc** loaded.
2. Paste **Prompt 1**, read the output, run the review checklist under it.
3. Paste **Prompt 2**, review. Paste **Prompt 3**, review. Optionally paste **Prompt 4** to
   consolidate.
4. The goal is a **framework-neutral, demo-scoped spec** Codex can build in the remaining time, not a
   production architecture.

## Shared constraints (these are baked into every prompt below)

- **Goal is a demo that runs well in one day.** Not a production concurrency system.
- **Single user, single request, fan-out then join.** There is no concurrent multi-writer state at
  demo scale, so **do not design queues, an event bus, or locks.**
- **No new framework.** Plain FastAPI + Python. Framework-neutral spec (no LangGraph / CrewAI).
- **Build only two things for real:** (1) the agent pipeline + reasoning visualization, (2) the
  evidence-based Why Panel. Memory, the full loop, and the network are **shown as vision** (mockup,
  diagram, one seeded "Day 2" comparison), not fully built.
- **Minimize GPT-5.6 calls.** Show six agent *roles* but collapse them into **2 to 3 real calls**
  (parallel or staged). Keep the **Confidence Judge as a genuine separate pass** (it is the visible
  differentiator).
- **Do not break the privacy spine.** Raw audio deleted immediately, nothing derived persists by
  default, memory is an **opt-in toggle + seeded demo** only. Never quietly break "Audio deleted,
  nothing stored."
- **Every deliverable marks a real-vs-mock cut line** for the demo.

---

## Prompt 1 — System architecture and state separation (demo-scoped)

```
우리는 지금 "AI Role Model Engine"(첨부된 전략 문서 참고)의 멀티 에이전트 아키텍처를
플랜 단계에서 설계하려고 합니다. 최우선 목표는 "하루 안에 잘 도는 데모"이고,
프로덕션용 동시성 시스템을 만드는 것이 아닙니다.

전제(반드시 지킬 것):
- 단일 사용자, 단일 요청, fan-out 후 join 구조. 동시 다중 writer 상태가 없으므로
  메시지 큐 / 이벤트 버스 / 락(lock)을 설계하지 마세요.
- 새 프레임워크(LangGraph, CrewAI 등) 도입 금지. 순수 FastAPI + Python 기준의
  프레임워크 중립 설계로.
- 실제로 빌드하는 건 2개뿐: (1) 에이전트 파이프라인 + 추론 시각화,
  (2) 증거 기반 Why Panel. 메모리/루프/네트워크는 "비전 시연"(목업/다이어그램/
  seeded Day2)이지 완전 구현이 아님.
- 프라이버시: 원본 오디오 즉시 삭제, 파생물 기본 미보존, 메모리는 opt-in + seeded 데모.

다음을 정교하게 설계해 주세요:
1. 메인 오케스트레이터(Supervisor)의 역할과 제어 흐름. 단, 라우팅은 LLM 판단이 아니라
   반드시 "결정적(deterministic)"이어야 합니다. 왜 결정적이어야 하는지도 한 줄로.
2. 분리할 워커(Worker) 에이전트 리스트 (전략 문서의 6개 역할 기반) + 각 워커의
   Single Responsibility. 6개 역할을 실제 GPT 콜 2~3개로 어떻게 묶을지(병렬/staged)도 표시.
3. 글로벌 상태 vs 로컬 상태 구분. 단, "데모 스케일에서는 공유 가변 상태가 거의 없다"는
   점을 명시하고, 유일하게 지속되는 상태(opt-in 스타일 메모리) 하나만 식별해 주세요.
4. 에이전트 간 데이터 전달 방식. 동기 fan-out 후 join으로 충분함을 전제로,
   어디를 병렬화하면 지연이 줄어드는지만 표시하세요. (큐/이벤트버스 설계 금지)
5. 이 설계에서 데모에 "실제로 도는 부분" vs "목업/seeded로 보여줄 부분"의 컷라인.

출력은 간결하고 구현 지향적으로.
```

**Review checklist for Prompt 1's output:**
- Supervisor is **deterministic** (not an LLM deciding the route).
- Six roles are mapped to **2 to 3 real calls**, Confidence Judge kept separate.
- It explicitly says there is **almost no shared mutable state**; only the opt-in memory persists.
- **No queue / event bus / lock** was introduced.
- A clear **real-vs-mock cut line** is present.

---

## Prompt 2 — Agent contract specs (per worker)

```
앞서 정의한 에이전트들에 대해 각각의 "계약 명세(Agent Contract)"를 작성해 주세요.
목적은 역할 중첩과 애매한 인터페이스로 인한 충돌을 설계 단계에서 차단하는 것입니다.

각 에이전트마다 다음을 포함하세요:
1. 이름 + 한 줄 미션.
2. Input Schema — JSON 구조와 짧은 예시 포함.
3. Output Schema — JSON 구조와 짧은 예시 포함. (특히 Why 관련 에이전트는 전략 문서의
   "증거 체인: You quote -> Creator descriptor -> Match" 구조를 반영)
4. 사용 가능한 도구 / 접근 범위. 대부분의 에이전트는 "LLM only" 또는 "transcript only"임을
   명시하고, DB(스타일 메모리) 접근은 opt-in 메모리 담당 워커로만 한정하세요.
5. 전제 조건(pre-conditions) + 성공/실패 판정 기준.
6. 실패/타임아웃 시: 오케스트레이터에 반환할 에러 코드 + fallback 동작 + "재시도 상한"
   (무한 재시도 금지).

추가로:
- 각 에이전트 옆에 "이건 진짜 별도 GPT 콜인가, 아니면 staged 단일 콜의 일부인가"를 표시하고,
  실제 콜 수가 2~3개로 유지되는지 확인해 주세요. Confidence Judge는 별도 콜 유지.
- 전제(단일 요청, 큐/락 없음, 순수 FastAPI, 데모 우선, 프라이버시 opt-in)는 그대로 유지.
```

**Review checklist for Prompt 2's output:**
- Every agent has a **strict Input/Output JSON schema with an example**.
- The Why agents output the **evidence-chain** shape (learner quote to creator descriptor to match).
- Tool/DB access is **narrow**: only the memory worker touches persistence, and only on opt-in.
- Each agent has an **error code + fallback + retry cap**.
- Real-call count stays at **2 to 3**; Confidence Judge is a separate pass.

---

## Prompt 3 — Red-team stress test (our real risks, not imaginary ones)

```
지금까지의 아키텍처 + 워커 스펙을 기준으로, 실제 데모 가동 시의 위험을 비판적으로
시뮬레이션해 주세요. 단, 과녁은 "우리 데모의 진짜 리스크"입니다. 데모 스케일에서
발생하지 않는 DB 락 / 동시성 race condition은 다루지 말고(억지로 만들지 말 것),
아래 3가지에 집중하세요:

1. 지연(Latency) 병목: 어떤 GPT 콜 또는 외부 API(예: Groq 번역)가 전체 흐름을 느리게
   만드는가? 병렬화 / staged 통합 / 캐싱으로 개선안을 제시하고, 목표는 총 처리 시간을
   대략 30~40초 이내로 유지하는 것.
2. 순환 / 무한 루프: Confidence Judge가 근거 부족으로 Evidence Generator에 재작성을
   반복 요청하는 루프에 빠질 위험이 있는가? "최대 재시도 1~2회 + 그래도 부족하면
   통과가 아니라 중립 fallback으로 종료" 같은 안전장치를 수치로 제시.
3. 부분 실패(Graceful Degradation): 6개 역할 중 하나가 실패/타임아웃해도
   top-3 카드 + 최소한의 Why가 렌더되도록 하는 fallback 경로를 제시.

각 위험마다: (a) 어디서 터지는지, (b) 개선책, (c) 구체적 안전장치(타임아웃 값, 재시도
상한, fallback 카피)까지 명시하세요.
```

**Review checklist for Prompt 3's output:**
- It targets **latency, the critique loop, and partial failure** — not DB locks.
- The critique loop has a **hard retry cap** and a "fallback instead of pass" rule.
- Partial failure still renders **three cards + a minimal Why**.
- Every mitigation has a **concrete number** (timeout, retry cap) or fallback copy.

---

## Prompt 4 (optional) — Consolidate into a build-ready spec

```
지금까지 확정된 내용을 개발자(Codex)가 즉시 구현할 수 있는 스펙 문서로 정리해 주세요.
포함할 것:
1. 메인 파이프라인을 Mermaid 다이어그램으로(워커 fan-out 후 join + Confidence Judge 패스).
2. 상태 원칙: 워커는 상태를 직접 수정하지 않고 "변경분(state delta)"만 반환, 실제 상태
   반영은 오케스트레이터 한 곳에서만. (데모에선 사실상 요청 스코프 객체 하나)
3. 실제 GPT 콜 목록(2~3개)과 각 콜에 들어가는 에이전트 역할 매핑.
4. real vs mock 컷라인 표: 데모에서 실제 도는 것 / 목업 / seeded.
5. 두 히어로 화면의 데이터 계약: (a) 추론 시각화(에이전트 파이프라인이 보이는),
   (b) 증거 체인 Why Panel.
6. "Codex + GPT-5.6를 이렇게 썼다"는 README용 한 줄 스토리.

순수 FastAPI + Python 기준. 새 프레임워크/큐/락 도입 금지.
```

**Review checklist for Prompt 4's output:**
- A **Mermaid** diagram of the pipeline exists.
- The **state-delta** rule is stated (orchestrator is the only writer).
- The **real-vs-mock cut line** and the **two hero-screen data contracts** are explicit.
- Everything stays **plain FastAPI**, no new framework.

---

## Design principles kept (demo-scoped versions)

- **Async only where it is cheap and it removes latency** (parallel fan-out of independent agents).
  No message queue, no event bus.
- **State-delta / single writer:** agents return changes; the orchestrator applies them. At demo
  scale this is one request-scoped object, which removes any race by construction.
- **Mermaid diagram** of the main workflow to spot tangled dependencies at a glance.
- **Confidence Judge is the one genuinely separate reasoning pass** — the visible "reasoning process"
  that the judging rewards.

## Exit criteria (what the plan stage must produce before building)

1. A deterministic Supervisor + a worker list mapped to **2 to 3 real GPT calls**.
2. An **agent contract** (I/O schema + tools + fallback + retry cap) for each worker.
3. A red-team result covering **latency, critique loop, partial failure**, each with a concrete
   safeguard.
4. A **real-vs-mock cut line** and **two hero-screen data contracts**.
5. A one-line README story of how Codex + GPT-5.6 were used.

Anything beyond this (queues, locks, accounts, a live memory history, LangGraph) is out of scope for
the one-day demo and should be recorded as "future," not built.
