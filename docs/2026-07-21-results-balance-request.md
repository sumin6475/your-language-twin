# 요청서 — 결과 페이지 좌우 무게 균형 (해커톤 데모용)

**대상 파일**
- `web/components/MatchCard.tsx` (메인 수정)
- `web/components/ExpandableQuote.tsx` (신규 생성 — 클라이언트 컴포넌트)

**목표 한 줄**
"You said" 인용문을 **1줄로 clamp + 더보기(Show more)** 토글로 바꿔, 좌우 박스 높이를 맞추고 분석이 얕아 보이지 않게 한다. 오른쪽 고정 텍스트(`creator_descriptor`)와 나머지는 그대로.

---

## 1. 지금 상태 (문제 진단)

`MatchCard.tsx`의 evidence row 구조:
- 왼쪽 박스(`quoteCard`, `flex:1`): "You said" + `item.you_quote.text`
- `<Arrow />`
- 오른쪽 박스(`quoteCard`, `flex:1`): "{name} does" + `item.creator_descriptor` (**고정 텍스트, 짧음**)
- 오른쪽 끝 "Match" 칩
- 그 아래 `item.match_reason` 한 줄

row는 `alignItems: "stretch"`, 두 박스는 동일 `quoteCard` 스타일(`flex:1`).

**문제**: 실제 전사된 `you_quote.text`는 장황함 → 왼쪽 박스가 세로로 커짐 → `stretch` 때문에 오른쪽 고정-짧은 텍스트 박스도 같이 늘어나 **빈 공간 발생** → 좌우 불균형 + "분석이 간편해 보이는" 착시. (목업은 인용문이 짧아 이 문제가 안 보였던 것.)

## 2. 원하는 동작

- "You said" 인용문을 기본 **1줄만** 보이게 clamp, 넘치면 끝에 **"더보기"** 토글. 펼치면 전체, 다시 "접기".
- 짧아서 안 잘리는 인용문은 토글 없이 그대로.
- 오른쪽 `creator_descriptor`(화살표 뒤 고정 텍스트), "Match" 칩, `match_reason`은 **그대로 유지**.
- clamp 후엔 양쪽 박스가 1줄로 균형이 맞아야 함.

## 3. 상세 스펙

### 3-1. 신규 컴포넌트 `ExpandableQuote.tsx` (client)

`MatchCard`는 지금 server 컴포넌트(훅 없음)라, 토글 상태만 담는 작은 client 컴포넌트를 따로 만들어 그 자리에 끼운다. (카드 전체를 client로 바꾸지 말 것.)

```tsx
"use client";
import { useState, useRef, useLayoutEffect } from "react";

export function ExpandableQuote({ text }: { text: string }) {
  const [expanded, setExpanded] = useState(false);
  const [clampable, setClampable] = useState(false); // 넘칠 때만 토글 노출
  const ref = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const el = ref.current;
    if (el) setClampable(el.scrollHeight > el.clientHeight + 1);
  }, [text]);

  const clampStyle = expanded
    ? {}
    : { display: "-webkit-box", WebkitLineClamp: 1, WebkitBoxOrient: "vertical" as const, overflow: "hidden" };

  return (
    <div>
      <div ref={ref} style={{ fontSize: 13, lineHeight: 1.5, color: "var(--ink)", ...clampStyle }}>
        &ldquo;{text}&rdquo;
      </div>
      {(clampable || expanded) && (
        <button
          type="button"
          onClick={() => setExpanded((v) => !v)}
          style={{ marginTop: 4, padding: 0, background: "none", border: "none", cursor: "pointer",
                   fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 12, color: "var(--blue-deep)" }}
        >
          {expanded ? "접기" : "더보기"}
        </button>
      )}
    </div>
  );
}
```
- 라벨 문구는 UI 언어에 맞춰 조정 (영문이면 "Show more" / "Show less").
- clamp 판정은 `scrollHeight > clientHeight`로 (넘칠 때만 토글). 간단히 가려면 `text.length > 60`류 문자수 heuristic도 가능하나 ref 방식 권장.

### 3-2. `MatchCard.tsx` 수정

왼쪽 박스 안의 이 부분만 교체:
```tsx
// 기존
<div style={{ fontSize: 13, lineHeight: 1.5, color: "var(--ink)" }}>&ldquo;{item.you_quote.text}&rdquo;</div>
// 변경
<ExpandableQuote text={item.you_quote.text} />
```
(라벨 "You said"와 `quoteCard` 래퍼는 유지.)

### 3-3. 박스 정렬 보정

- evidence row의 `alignItems`를 `"stretch"` → **`"flex-start"`** 로 변경. 왼쪽이 펼쳐져도 오른쪽 고정-짧은 박스가 억지로 안 늘어나 균형 유지.
- (선택) 오른쪽이 너무 비어 보이면 `creator_descriptor`가 항상 1~2줄이라 그대로 두되, "Match" 칩 정렬만 `alignSelf: "center"` 유지.

## 4. 시각/톤

- 접힌 상태 기본. 인용문 1줄 + "더보기"가 파란 텍스트 링크로 (`--blue-deep`).
- 오른쪽 고정 텍스트, `match_reason`, "Match" 칩 스타일 변경 없음.
- 목업(두 번째 이미지)의 균형감 = 목표 레퍼런스.

## 5. Out of scope (건드리지 말 것)

- `creator_descriptor`(화살표 뒤 텍스트) 내용/스타일.
- `match_reason`, resemblance 뱃지, "Evidence verified", "Visit their channel" 등 나머지 카드 요소.
- 데이터 모델(`matches.ts`) 변경 불필요.

## 6. Acceptance criteria (완료 기준)

- [ ] 긴 "You said" 인용문이 기본 1줄로 잘리고 "더보기"가 뜬다.
- [ ] "더보기" 누르면 전체 문장, "접기"로 되돌아온다.
- [ ] 짧아서 안 잘리는 인용문엔 토글이 안 뜬다.
- [ ] clamp 상태에서 좌우 박스 높이가 맞고, 오른쪽에 빈 공간이 안 생긴다.
- [ ] `creator_descriptor` / `match_reason` / "Match" 칩은 변화 없음.
- [ ] `prefers-reduced-motion` 및 콘솔 에러 없음, MatchCard는 server 컴포넌트 유지(토글만 client 자식).

---

**튜닝 포인트**: 기본 clamp 줄 수(`WebkitLineClamp`, 기본 1 — 답답하면 2), 더보기/접기 라벨 언어.
