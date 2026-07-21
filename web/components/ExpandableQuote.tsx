"use client";

import { useLayoutEffect, useRef, useState } from "react";

export function ExpandableQuote({ text }: { text: string }) {
  const [expanded, setExpanded] = useState(false);
  const [clampable, setClampable] = useState(false);
  const quoteRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    const quote = quoteRef.current;
    if (quote) setClampable(quote.scrollHeight > quote.clientHeight + 1);
  }, [text]);

  const clampStyle = expanded
    ? {}
    : {
        display: "-webkit-box",
        WebkitLineClamp: 1,
        WebkitBoxOrient: "vertical" as const,
        overflow: "hidden",
      };

  return (
    <div>
      <div ref={quoteRef} style={{ fontSize: 13, lineHeight: 1.5, color: "var(--ink)", ...clampStyle }}>
        &ldquo;{text}&rdquo;
      </div>
      {clampable || expanded ? (
        <button
          aria-expanded={expanded}
          onClick={() => setExpanded((isExpanded) => !isExpanded)}
          style={{ marginTop: 4, padding: 0, background: "none", border: "none", cursor: "pointer", fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 12, color: "var(--blue-deep)" }}
          type="button"
        >
          {expanded ? "Show less" : "Show more"}
        </button>
      ) : null}
    </div>
  );
}
