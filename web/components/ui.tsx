import Link from "next/link";
import type { CSSProperties, ReactNode } from "react";

/* Header ------------------------------------------------------------------ */
export function Header({
  variant = "marketing",
  active,
}: {
  variant?: "marketing" | "app";
  active?: "about";
}) {
  return (
    <header className="lrm-header">
      <Link className="lrm-brand" href="/">
        <span className="lrm-brand-mark" />
        <span>Language Role Model</span>
      </Link>
      <nav className="lrm-nav">
        <a className="dc-navlink" data-active={active === "about"} href="/about">
          About
        </a>
        <a className="dc-navlink" href="/#how-it-works">
          How it works
        </a>
        {variant === "marketing" ? (
          <Link className="dc-btn dc-btn-primary" href="/app" style={{ padding: "10px 16px", fontSize: 13 }}>
            Try it, no account
          </Link>
        ) : null}
      </nav>
    </header>
  );
}

/* Badge (Claude Design DS) ------------------------------------------------ */
const badgeVariants: Record<string, CSSProperties> = {
  match: { background: "var(--blue-tint)", color: "var(--blue-deep)" },
  neutral: { background: "var(--bg-subtle)", color: "var(--ink-secondary)", border: "1px solid var(--border)" },
  solid: { background: "var(--blue-deep)", color: "var(--text-on-blue)" },
};

export function Badge({
  children,
  variant = "match",
  style,
}: {
  children: ReactNode;
  variant?: "match" | "neutral" | "solid";
  style?: CSSProperties;
}) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        fontFamily: "var(--font-display)",
        fontWeight: 500,
        fontSize: 13,
        lineHeight: 1,
        padding: "6px 10px",
        borderRadius: "var(--radius-sm)",
        whiteSpace: "nowrap",
        ...badgeVariants[variant],
        ...style,
      }}
    >
      {children}
    </span>
  );
}

/* Pills ------------------------------------------------------------------- */
export function LivePill({ style }: { style?: CSSProperties }) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        gap: 6,
        fontFamily: "var(--font-display)",
        fontWeight: 500,
        fontSize: 11,
        letterSpacing: "0.06em",
        textTransform: "uppercase",
        whiteSpace: "nowrap",
        padding: "4px 10px",
        borderRadius: 999,
        background: "var(--blue-tint)",
        color: "var(--blue-deep)",
        ...style,
      }}
    >
      <span style={{ width: 6, height: 6, borderRadius: "50%", background: "var(--blue-deep)" }} />
      Live
    </span>
  );
}

export function ComingSoonPill({ style }: { style?: CSSProperties }) {
  return (
    <span
      style={{
        display: "inline-flex",
        alignItems: "center",
        fontFamily: "var(--font-display)",
        fontWeight: 500,
        fontSize: 11,
        letterSpacing: "0.06em",
        textTransform: "uppercase",
        whiteSpace: "nowrap",
        padding: "4px 10px",
        borderRadius: 999,
        background: "var(--bg-subtle)",
        color: "var(--ink-tertiary)",
        border: "1px dashed var(--border)",
        flexShrink: 0,
        ...style,
      }}
    >
      Coming soon
    </span>
  );
}

export function SectionLabel({ children, style }: { children: ReactNode; style?: CSSProperties }) {
  return (
    <div
      style={{
        fontFamily: "var(--font-display)",
        fontSize: 12,
        fontWeight: 500,
        letterSpacing: "0.1em",
        textTransform: "uppercase",
        color: "var(--ink-tertiary)",
        ...style,
      }}
    >
      {children}
    </div>
  );
}

/* Avatar ------------------------------------------------------------------ */
export function Avatar({ name, size = 52, style }: { name: string; size?: number; style?: CSSProperties }) {
  const initials = name
    .split(" ")
    .map((word) => word[0])
    .filter(Boolean)
    .slice(0, 2)
    .join("")
    .toUpperCase();
  return (
    <div
      aria-hidden="true"
      style={{
        width: size,
        height: size,
        flexShrink: 0,
        borderRadius: "var(--radius-md)",
        background: "var(--avatar-gradient)",
        color: "var(--text-on-blue)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        fontFamily: "var(--font-display)",
        fontWeight: 600,
        fontSize: size * 0.36,
        ...style,
      }}
    >
      {initials}
    </div>
  );
}

/* Icons ------------------------------------------------------------------- */
export function Check({ size = 15, stroke = "var(--blue-deep)", strokeWidth = 2.5, style }: { size?: number; stroke?: string; strokeWidth?: number; style?: CSSProperties }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" style={style} aria-hidden="true">
      <polyline points="20 6 9 17 4 12" />
    </svg>
  );
}

export function ArrowGlyph({ size = 16, stroke = "var(--blue-deep)", strokeWidth = 2.2 }: { size?: number; stroke?: string; strokeWidth?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="4" y1="12" x2="20" y2="12" />
      <polyline points="13 5 20 12 13 19" />
    </svg>
  );
}

export function ShieldCheck({ size = 21, stroke = "#fff", strokeWidth = 2.4 }: { size?: number; stroke?: string; strokeWidth?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={stroke} strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M9 12l2 2 4-4" />
      <path d="M12 3l7 4v5c0 4-3 7-7 8-4-1-7-4-7-8V7z" />
    </svg>
  );
}

/* Legacy arrow used by evidence chains */
export function Arrow() {
  return (
    <span aria-hidden="true" style={{ alignSelf: "center", color: "var(--blue-deep)", fontSize: 16, fontWeight: 600 }}>
      &rarr;
    </span>
  );
}
