import { Arrow, Avatar, Badge, Check } from "@/components/ui";
import { ExpandableQuote } from "@/components/ExpandableQuote";
import type { Match } from "@/lib/matches";

const quoteCard = {
  flex: 1,
  minWidth: 170,
  background: "var(--surface-card)",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-sm)",
  padding: "11px 13px",
} as const;

const microLabel = {
  fontFamily: "var(--font-display)",
  fontSize: 10,
  fontWeight: 500,
  letterSpacing: "0.08em",
  textTransform: "uppercase",
  color: "var(--ink-tertiary)",
  marginBottom: 5,
} as const;

export function MatchCard({ match, judgeSkipped = false, analysisComplete, raised = false }: { match: Match; judgeSkipped?: boolean; analysisComplete?: boolean; raised?: boolean }) {
  const evidenceCount = match.evidence.length;
  const evidenceVerified = evidenceCount > 0 && !judgeSkipped && analysisComplete !== false;
  const resemblanceVariant = match.resemblance === "strong" ? "matchStrong" : match.resemblance === "clear" ? "matchClear" : "matchPartial";
  return (
    <article
      style={{
        background: "var(--surface-card)",
        border: "1px solid var(--border)",
        borderRadius: "var(--radius-lg)",
        boxShadow: raised ? "var(--shadow-raised)" : "var(--shadow-card)",
        padding: 24,
        display: "flex",
        flexDirection: "column",
        gap: 18,
      }}
    >
      <div style={{ display: "flex", gap: 16 }}>
        <Avatar name={match.name} size={52} />
        <div style={{ minWidth: 0, flex: 1, display: "flex", flexDirection: "column", gap: 8 }}>
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12 }}>
            <span style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 18, lineHeight: 1.2, color: "var(--ink)" }}>{match.name}</span>
            <Badge variant={resemblanceVariant}>{match.resemblance} resemblance</Badge>
          </div>
          <div style={{ fontSize: 13, color: "var(--ink-tertiary)" }}>{match.role}</div>
          <p style={{ fontSize: 15, lineHeight: 1.6, color: "var(--ink-secondary)", margin: 0, textWrap: "pretty" }}>{match.why}</p>
        </div>
      </div>

      {match.trait_chips.length ? (
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {match.trait_chips.map((chip) => (
            <span key={chip} style={{ fontSize: 12, color: "var(--ink-secondary)", background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: 999, padding: "5px 11px" }}>
              {chip}
            </span>
          ))}
        </div>
      ) : null}

      {evidenceCount ? (
        <div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: 16, display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 10, flexWrap: "wrap" }}>
            <div style={{ fontFamily: "var(--font-display)", fontSize: 11, fontWeight: 500, letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--ink-tertiary)" }}>Why these two line up</div>
            {evidenceVerified ? (
              <span style={{ display: "inline-flex", alignItems: "center", gap: 5, fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 11, padding: "4px 9px", borderRadius: 999, background: "var(--blue-tint)", color: "var(--blue-deep)" }}>
                <Check size={11} strokeWidth={3} />
                Evidence verified
              </span>
            ) : (
              <span style={{ display: "inline-flex", alignItems: "center", fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 11, letterSpacing: "0.06em", textTransform: "uppercase", padding: "4px 10px", borderRadius: 999, background: "var(--bg-subtle)", color: "var(--ink-tertiary)", border: "1px dashed var(--border)" }}>
                {judgeSkipped ? "Confidence check unavailable" : "Evidence not verified"}
              </span>
            )}
          </div>
          {match.evidence.map((item, index) => (
            <div key={`${item.trait_id}-${index}`} style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              <div style={{ display: "flex", alignItems: "flex-start", gap: 10, flexWrap: "wrap" }}>
                <div style={quoteCard}>
                  <div style={microLabel}>You said</div>
                  <ExpandableQuote text={item.you_quote.text} />
                </div>
                <Arrow />
                <div style={quoteCard}>
                  <div style={microLabel}>{match.name} does</div>
                  <div style={{ fontSize: 13, lineHeight: 1.5, color: "var(--ink)" }}>{item.creator_descriptor}</div>
                </div>
                <span style={{ alignSelf: "center", display: "inline-flex", alignItems: "center", gap: 5, fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 12, padding: "6px 10px", borderRadius: 999, background: evidenceVerified ? "var(--blue-tint)" : "var(--bg-subtle)", color: evidenceVerified ? "var(--blue-deep)" : "var(--ink-secondary)", border: evidenceVerified ? undefined : "1px solid var(--border)" }}>
                  {evidenceVerified ? <Check size={11} strokeWidth={3} /> : null}
                  {evidenceVerified ? "Match" : "Reported overlap"}
                </span>
              </div>
              {item.match_reason ? <p style={{ margin: 0, fontSize: 13, lineHeight: 1.5, color: "var(--ink-secondary)" }}>{item.match_reason}</p> : null}
            </div>
          ))}
        </div>
      ) : (
        <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: 0 }}>We found a possible match in sentence structure, but the detailed evidence did not complete this time.</p>
      )}

      <a className="dc-btn dc-btn-secondary" href={match.video_url} rel="noreferrer" target="_blank" style={{ alignSelf: "flex-start", padding: "9px 16px", fontSize: 14 }}>
        Visit their channel
      </a>
    </article>
  );
}
