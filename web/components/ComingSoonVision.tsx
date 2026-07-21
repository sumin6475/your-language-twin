import { ComingSoonPill, SectionLabel } from "@/components/ui";

const dashedCard = {
  background: "var(--surface-card)",
  border: "1px dashed var(--border)",
  borderRadius: "var(--radius-lg)",
  padding: 22,
} as const;

const flowPill = {
  fontFamily: "var(--font-display)",
  fontSize: 13,
  fontWeight: 500,
  color: "var(--ink)",
  background: "var(--bg-subtle)",
  border: "1px solid var(--border)",
  borderRadius: 999,
  padding: "8px 14px",
} as const;

const day1 = [
  ["Sentence length", "short"],
  ["Questions you ask", "rarely"],
  ["Your own opinions", "sometimes"],
];
const day14 = [
  ["Sentence length", "a little longer"],
  ["Questions you ask", "more often"],
  ["Your own opinions", "clearly"],
];

export function ComingSoonVision() {
  return (
    <>
      <div style={{ marginTop: 56 }}>
        <div style={{ textAlign: "center", marginBottom: 8 }}>
          <SectionLabel style={{ marginBottom: 10 }}>Where this goes next</SectionLabel>
          <h2 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 24, margin: 0, textWrap: "pretty" }}>
            Finding your match is step one of a loop.
          </h2>
          <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-tertiary)", margin: "12px auto 0", maxWidth: "46ch", textWrap: "pretty" }}>
            The parts below are the vision. They are not in this demo yet.{" "}
            <a className="dc-inline-link" href="/about">
              See the whole idea &rarr;
            </a>
          </p>
        </div>

        <div style={{ display: "flex", flexDirection: "column", gap: 20, marginTop: 28 }}>
          {/* Personal Language Memory */}
          <div style={dashedCard}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 6 }}>
              <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 17, color: "var(--ink)" }}>Personal Language Memory</div>
              <ComingSoonPill />
            </div>
            <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "0 0 16px", maxWidth: "60ch" }}>
              With your permission we can save a profile of how you talk, never your audio, and show what grew between two recordings.
            </p>
            <div style={{ opacity: 0.6, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
              {[
                ["Day 1", day1],
                ["Day 14", day14],
              ].map(([label, rows]) => (
                <div key={label as string} style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: 16 }}>
                  <SectionLabel style={{ fontSize: 11, letterSpacing: "0.08em", marginBottom: 12 }}>{label as string}</SectionLabel>
                  <div style={{ display: "flex", flexDirection: "column", gap: 10, fontSize: 13, color: "var(--ink-secondary)" }}>
                    {(rows as string[][]).map(([field, value]) => (
                      <div key={field}>
                        {field}: <span style={{ color: "var(--ink)" }}>{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Practice loop */}
          <div style={dashedCard}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 6 }}>
              <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 17, color: "var(--ink)" }}>A practice loop, built around your match.</div>
              <ComingSoonPill />
            </div>
            <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "0 0 16px", maxWidth: "60ch" }}>
              Once you know who talks like you, the next step is copying them on purpose, then seeing what improved, then getting a fresh match.
            </p>
            <div style={{ opacity: 0.6, display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
              {["Understand you", "Find your match", "Practice with them", "See what grew"].map((label, index, arr) => (
                <span key={label} style={{ display: "contents" }}>
                  <span style={flowPill}>{label}</span>
                  {index < arr.length - 1 ? <span style={{ color: "var(--ink-tertiary)" }}>&rarr;</span> : null}
                </span>
              ))}
              <span style={{ color: "var(--ink-tertiary)" }}>&#8617;</span>
              <span style={{ fontFamily: "var(--font-display)", fontSize: 13, fontWeight: 500, color: "var(--ink-tertiary)" }}>then a fresh match</span>
            </div>
          </div>

          {/* Creator network */}
          <div style={dashedCard}>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 6 }}>
              <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 17, color: "var(--ink)" }}>A new way for real creators to be found.</div>
              <ComingSoonPill />
            </div>
            <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "0 0 16px", maxWidth: "60ch" }}>
              The role models are real English vloggers, and that pool keeps growing. When a learner matches a creator, that creator gets found by exactly the person who wants to learn from them. For a small vlogger, that is a new way to be discovered, not through ads, but through the way they talk.
            </p>
            <div style={{ opacity: 0.6, display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
              {["Learners", "matched by how they talk", "Creators (vloggers) get found"].map((label, index, arr) => (
                <span key={label} style={{ display: "contents" }}>
                  <span style={flowPill}>{label}</span>
                  {index < arr.length - 1 ? <span style={{ color: "var(--ink-tertiary)" }}>&rarr;</span> : null}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>

      {/* For creators — animated trail border */}
      <div className="dc-trail-card" style={{ background: "var(--surface-card)", border: "1px solid var(--border)", borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-card)", padding: 24, marginTop: 40 }}>
        <div className="dc-trail-mask">
          <div className="dc-trail" />
        </div>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 10 }}>
          <SectionLabel>For creators</SectionLabel>
          <ComingSoonPill />
        </div>
        <p style={{ fontSize: 15, lineHeight: 1.6, color: "var(--ink-secondary)", margin: 0, textWrap: "pretty" }}>
          Do you make videos in English? Learners who talk like you are looking for someone to copy. Soon you will be able to opt in and get found. Coming soon.
        </p>
      </div>
    </>
  );
}
