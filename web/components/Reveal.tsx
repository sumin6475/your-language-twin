"use client";

import { useEffect, useRef, type ReactNode } from "react";

/**
 * RevealScope mirrors the Claude Design pages' reveal script: any descendant
 * carrying `data-reveal` ("rise" | "pop") starts at opacity 0 and animates in
 * when it scrolls into view, honoring an optional `data-delay`.
 */
export function RevealScope({ children, className, style }: { children: ReactNode; className?: string; style?: React.CSSProperties }) {
  const ref = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    const root = ref.current;
    if (!root) return;
    const els = Array.from(root.querySelectorAll<HTMLElement>("[data-reveal]"));

    const prefersReduced =
      typeof window !== "undefined" && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (prefersReduced) {
      els.forEach((el) => {
        el.style.opacity = "1";
      });
      return;
    }

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          const el = entry.target as HTMLElement;
          const anim = el.getAttribute("data-reveal") === "pop" ? "lrm-pop" : "lrm-rise";
          el.style.animation = `${anim} 500ms ease forwards`;
          el.style.animationDelay = el.getAttribute("data-delay") || "0s";
          observer.unobserve(el);
        });
      },
      { threshold: 0.12 }
    );
    els.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
  }, []);

  return (
    <div ref={ref} className={className} style={style}>
      {children}
    </div>
  );
}
