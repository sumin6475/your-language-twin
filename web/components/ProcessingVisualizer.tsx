import { Check, LivePill, ShieldCheck } from "@/components/ui";

const agents: { title: string; copy: string; tag: string; delay: string }[] = [
  { title: "Turn your clip into text", copy: "We write down what you said and split it into sentences.", tag: "Transcript Agent", delay: "0.15s" },
  { title: "Look at the way you talk", copy: "How you open a point, connect ideas, and land it.", tag: "Thinking Style Agent", delay: "0.5s" },
  { title: "Find the creators who fit you", copy: "Line you up with creators we have looked at by hand.", tag: "Role Model Matching Agent", delay: "0.85s" },
  { title: "Pull out what lines up", copy: "The exact lines where you and a creator do the same thing.", tag: "Evidence Agent", delay: "1.2s" },
];

const judgeChecks: { text: string; delay: string }[] = [
  { text: '"You open with a question" found in your words', delay: "2.3s" },
  { text: '"You end on one plain lesson" found in your words', delay: "2.8s" },
  { text: '"You stack concrete examples" found in your words', delay: "3.3s" },
];

export function ProcessingVisualizer() {
  return (
    <div style={{ maxWidth: 660, margin: "0 auto", padding: "48px 24px 72px" }}>
      <div style={{ textAlign: "center", marginBottom: 36 }}>
        <div style={{ marginBottom: 16 }}>
          <LivePill />
        </div>
        <h1 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 28, lineHeight: 1.15, letterSpacing: "-0.015em", margin: 0, textWrap: "pretty" }}>
          Finding the creators who talk the way you do.
        </h1>
        <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-tertiary)", margin: "14px auto 0", maxWidth: "46ch", textWrap: "pretty" }}>
          This is not one guess. A short chain of steps looks at your clip, then a last step checks every reason against your own words.
        </p>
        <div className="dc-dots" style={{ marginTop: 22 }} role="status" aria-label="Processing">
          <span />
          <span />
          <span />
        </div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {agents.map((agent) => (
          <div
            key={agent.tag}
            style={{
              opacity: 0,
              animation: "lrm-rise 460ms ease forwards",
              animationDelay: agent.delay,
              display: "flex",
              alignItems: "center",
              gap: 14,
              background: "var(--surface-card)",
              border: "1px solid var(--border)",
              borderRadius: "var(--radius-md)",
              boxShadow: "var(--shadow-card)",
              padding: "14px 18px",
            }}
          >
            <span style={{ width: 24, height: 24, flexShrink: 0, borderRadius: "50%", background: "var(--blue-tint)", display: "flex", alignItems: "center", justifyContent: "center" }}>
              <Check size={13} strokeWidth={3} />
            </span>
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 15, color: "var(--ink)" }}>{agent.title}</div>
              <div style={{ fontSize: 13, color: "var(--ink-tertiary)" }}>{agent.copy}</div>
            </div>
            <span className="dc-agent-tag">{agent.tag}</span>
          </div>
        ))}

        {/* Confidence Judge */}
        <div style={{ opacity: 0, animation: "lrm-rise 500ms ease forwards", animationDelay: "1.7s", position: "relative", overflow: "hidden", background: "var(--surface-card)", border: "1.5px solid var(--blue-deep)", borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-raised)", padding: 22, marginTop: 6 }}>
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 6 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span style={{ width: 32, height: 32, flexShrink: 0, borderRadius: "var(--radius-md)", background: "var(--avatar-gradient)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <ShieldCheck size={17} />
              </span>
              <div>
                <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 17, color: "var(--ink)" }}>Confidence check</div>
                <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 4, flexWrap: "wrap" }}>
                  <span style={{ fontFamily: "ui-monospace,SFMono-Regular,Menlo,monospace", fontSize: 11, letterSpacing: "0.02em", color: "var(--blue-deep)", background: "var(--blue-tint)", borderRadius: 6, padding: "3px 8px", whiteSpace: "nowrap" }}>Confidence Judge</span>
                  <span style={{ fontSize: 12, color: "var(--ink-tertiary)", fontFamily: "var(--font-display)", fontWeight: 500 }}>the step that keeps us honest</span>
                </div>
              </div>
            </div>
            <LivePill />
          </div>
          <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "12px 0 16px" }}>
            A second pass reads every reason back against your own words. If a reason is not clearly in your clip, it is dropped.
          </p>
          <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
            {judgeChecks.map((item) => (
              <div key={item.text} style={{ opacity: 0, animation: "lrm-pop 320ms ease forwards", animationDelay: item.delay, display: "flex", alignItems: "center", gap: 10, background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-sm)", padding: "10px 12px" }}>
                <span style={{ width: 18, height: 18, flexShrink: 0, borderRadius: "50%", background: "var(--blue-deep)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                  <Check size={10} stroke="#fff" strokeWidth={3.5} />
                </span>
                <span style={{ fontSize: 13, color: "var(--ink-secondary)" }}>{item.text}</span>
              </div>
            ))}
          </div>
          <div style={{ opacity: 0, animation: "lrm-pop 360ms ease forwards", animationDelay: "3.8s", display: "flex", alignItems: "center", gap: 8, marginTop: 14, fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 14, color: "var(--blue-deep)" }}>
            <Check size={15} strokeWidth={2.5} />
            Every reason checked, three of three confirmed.
          </div>
        </div>

        <div style={{ opacity: 0, animation: "lrm-pop 400ms ease forwards", animationDelay: "4.5s", display: "flex", alignItems: "center", justifyContent: "center", gap: 10, marginTop: 16, fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 15, color: "var(--blue-deep)" }}>
          <span className="dc-spin" />
          Building your Language Twin...
        </div>
      </div>

      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, marginTop: 24, color: "var(--ink-tertiary)", fontSize: 13 }}>
        <Check size={14} strokeWidth={2.5} />
        Your clip is checked, then deleted. Nothing you said is stored.
      </div>
    </div>
  );
}
