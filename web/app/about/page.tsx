import Link from "next/link";

import { RevealScope } from "@/components/Reveal";
import { ArrowGlyph, Badge, Check, ComingSoonPill, Header, LivePill, SectionLabel, ShieldCheck } from "@/components/ui";

const CONTACT_EMAIL = "takedown@languagerolemodel.app";

const agents: [string, string, string][] = [
  ["1", "Transcript Agent", "Writes down what you said and splits it into sentences."],
  ["2", "Thinking Style Agent", "Reads how you open a point, connect ideas, and land it."],
  ["3", "Role Model Matching Agent", "Finds the English speakers whose way of talking fits yours."],
  ["4", "Evidence Agent", "Pulls the exact lines where you and a creator do the same thing."],
];

const twinBars: [string, number][] = [
  ["Story driven", 82],
  ["Example first", 64],
  ["Question led", 48],
  ["Reflective", 71],
];

const cardBase = {
  background: "var(--surface-card)",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-lg)",
  boxShadow: "var(--shadow-card)",
} as const;

const dayRows = (opinions: string, length: string, questions: string) => [
  ["Sentence length", length],
  ["Questions you ask", questions],
  ["Your own opinions", opinions],
];

export default function AboutPage() {
  return (
    <main className="lrm-page">
      <Header active="about" />
      <RevealScope>
        {/* Beat 1: hook */}
        <section style={{ maxWidth: 880, margin: "0 auto", padding: "130px 24px 40px", textAlign: "center" }}>
          <p data-reveal="rise" style={{ opacity: 0, fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 17, color: "var(--ink-tertiary)", margin: "0 0 22px" }}>
            You have been told to copy a native speaker.
          </p>
          <h1 data-reveal="rise" data-delay="0.25s" style={{ opacity: 0, fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 52, lineHeight: 1.16, letterSpacing: "-0.02em", margin: 0, textWrap: "balance" }}>
            But copying a stranger who talks nothing like you feels like wearing a costume.
          </h1>
          <p data-reveal="rise" data-delay="0.7s" style={{ opacity: 0, fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 21, color: "var(--blue-deep)", margin: "34px 0 0" }}>
            So we start from how you already talk.
          </p>
        </section>

        {/* Beat 2: the shift */}
        <section style={{ maxWidth: 980, margin: "0 auto", padding: "96px 24px 24px" }}>
          <div data-reveal="rise" style={{ opacity: 0, display: "grid", gridTemplateColumns: "1fr 44px 1fr", alignItems: "stretch", gap: 0 }}>
            <div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-lg)", padding: "34px 30px", display: "flex", flexDirection: "column", justifyContent: "center" }}>
              <SectionLabel style={{ fontSize: 11, letterSpacing: "0.1em", marginBottom: 12 }}>The usual way</SectionLabel>
              <p style={{ fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 22, lineHeight: 1.4, color: "var(--ink-tertiary)", margin: 0, textWrap: "balance" }}>
                Most apps help you sound like a native speaker.
              </p>
            </div>
            <div style={{ display: "flex", alignItems: "center", justifyContent: "center" }}>
              <ArrowGlyph size={24} />
            </div>
            <div style={{ ...cardBase, boxShadow: "var(--shadow-raised)", padding: "34px 30px", display: "flex", flexDirection: "column", justifyContent: "center" }}>
              <SectionLabel style={{ fontSize: 11, letterSpacing: "0.1em", color: "var(--blue-deep)", marginBottom: 12 }}>Our way</SectionLabel>
              <p style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 22, lineHeight: 1.4, color: "var(--blue-deep)", margin: 0, textWrap: "balance" }}>
                We find the native speaker who already sounds like you.
              </p>
            </div>
          </div>
          <p data-reveal="rise" data-delay="0.2s" style={{ opacity: 0, fontSize: 16, lineHeight: 1.7, color: "var(--ink-secondary)", margin: "30px auto 0", maxWidth: "56ch", textAlign: "center", textWrap: "pretty" }}>
            The way you build a sentence, ask a question, or tell a story is similar in any language, and that is what we listen for.
          </p>
        </section>

        {/* Beat 3: the pipeline */}
        <section style={{ maxWidth: 680, margin: "0 auto", padding: "110px 24px 24px" }}>
          <div data-reveal="rise" style={{ opacity: 0, marginBottom: 36 }}>
            <div style={{ marginBottom: 16 }}>
              <LivePill />
            </div>
            <SectionLabel style={{ marginBottom: 10 }}>How the reasoning works</SectionLabel>
            <h2 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 28, margin: 0, textWrap: "pretty" }}>
              Not one guess. A short chain of steps, each doing one job.
            </h2>
          </div>

          <div style={{ display: "flex", flexDirection: "column" }}>
            {agents.map(([number, title, copy], index) => (
              <div key={number}>
                <div data-reveal="rise" data-delay={`${index * 0.15}s`} style={{ opacity: 0, display: "flex", alignItems: "center", gap: 16, background: "var(--surface-card)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", boxShadow: "var(--shadow-card)", padding: "18px 20px" }}>
                  <span style={{ width: 28, height: 28, flexShrink: 0, borderRadius: "50%", background: "var(--blue-tint)", color: "var(--blue-deep)", fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 13, display: "flex", alignItems: "center", justifyContent: "center" }}>
                    {number}
                  </span>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 16, color: "var(--ink)", marginBottom: 4 }}>{title}</div>
                    <div style={{ fontSize: 14, lineHeight: 1.5, color: "var(--ink-secondary)" }}>{copy}</div>
                  </div>
                  <span className="dc-agent-tag">Agent {number}</span>
                </div>
                <div data-reveal="rise" data-delay={`${index * 0.15 + 0.1}s`} style={{ opacity: 0, display: "flex", justifyContent: "center", padding: "2px 0" }}>
                  <span style={{ width: 2, height: 22, background: index === agents.length - 1 ? "var(--blue-deep)" : "var(--border)", display: "block" }} />
                </div>
              </div>
            ))}
            <div data-reveal="pop" data-delay="0.65s" style={{ opacity: 0, display: "flex", alignItems: "center", gap: 16, background: "var(--surface-card)", border: "1.5px solid var(--blue-deep)", borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-raised)", padding: "22px 24px" }}>
              <span style={{ width: 40, height: 40, flexShrink: 0, borderRadius: "var(--radius-md)", background: "var(--avatar-gradient)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <ShieldCheck />
              </span>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: "flex", alignItems: "baseline", gap: 10, flexWrap: "wrap", marginBottom: 4 }}>
                  <span style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 18, color: "var(--ink)" }}>Confidence Judge</span>
                  <span style={{ fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 12, color: "var(--blue-deep)" }}>the step that keeps us honest</span>
                </div>
                <div style={{ fontSize: 14, lineHeight: 1.5, color: "var(--ink-secondary)" }}>Reads every reason back against your own words, and drops anything it cannot find there.</div>
              </div>
              <LivePill />
            </div>
          </div>
        </section>

        {/* Beat 4: payoff */}
        <section style={{ maxWidth: 900, margin: "0 auto", padding: "130px 24px", textAlign: "center" }}>
          <div data-reveal="rise" style={{ opacity: 0 }}>
            <span style={{ display: "block", width: 56, height: 2, background: "var(--blue-deep)", margin: "0 auto 40px" }} />
            <p style={{ fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 30, lineHeight: 1.5, letterSpacing: "-0.01em", color: "var(--ink)", margin: 0, textWrap: "balance" }}>
              We are not matching people by topic or vocabulary. We build a reasoning based language profile, verify every behavioral claim against your own transcript, and only then search for creators whose communication patterns truly align.
            </p>
            <span style={{ display: "block", width: 56, height: 2, background: "var(--blue-deep)", margin: "40px auto 0" }} />
          </div>
        </section>

        {/* Good to know */}
        <section style={{ maxWidth: 820, margin: "0 auto", padding: "0 24px 130px" }}>
          <div data-reveal="rise" style={{ opacity: 0, textAlign: "center", marginBottom: 36 }}>
            <SectionLabel style={{ marginBottom: 10 }}>Good to know</SectionLabel>
            <h2 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 28, margin: 0, textWrap: "balance" }}>What this is, and what it is not.</h2>
          </div>
          <div data-reveal="rise" data-delay="0.1s" style={{ opacity: 0, display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 14, marginBottom: 20 }}>
            <div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: 20 }}>
              <SectionLabel style={{ fontSize: 11, letterSpacing: "0.08em", marginBottom: 10 }}>Accent scorers</SectionLabel>
              <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: 0, textWrap: "pretty" }}>Apps that score your accent tell you how native you sound.</p>
            </div>
            <div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: 20 }}>
              <SectionLabel style={{ fontSize: 11, letterSpacing: "0.08em", marginBottom: 10 }}>Soundalike tools</SectionLabel>
              <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: 0, textWrap: "pretty" }}>Soundalike tools tell you which famous voice you resemble.</p>
            </div>
            <div style={{ background: "var(--blue-tint)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: 20 }}>
              <SectionLabel style={{ fontSize: 11, letterSpacing: "0.08em", color: "var(--blue-deep)", marginBottom: 10 }}>Us</SectionLabel>
              <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink)", margin: 0, textWrap: "pretty" }}>We do neither. We look at how you build your thoughts, then point you to real people who talk a similar way, so copying them feels natural.</p>
            </div>
          </div>
          <div data-reveal="rise" data-delay="0.2s" style={{ ...cardBase, opacity: 0, padding: "24px 26px" }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 16 }}>
              <span style={{ width: 26, height: 26, flexShrink: 0, borderRadius: "50%", background: "var(--blue-tint)", display: "flex", alignItems: "center", justifyContent: "center" }}>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="var(--blue-deep)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
              </span>
              <span style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 16, color: "var(--ink)" }}>Getting the best match</span>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 12, fontSize: 14, lineHeight: 1.65, color: "var(--ink-secondary)" }}>
              <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                <Check size={15} style={{ flexShrink: 0, marginTop: 4 }} />
                <span style={{ textWrap: "pretty" }}>Talk the way you normally would, in your own language. Loose and unscripted is perfect.</span>
              </div>
              <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                <svg width="15" height="15" style={{ flexShrink: 0, marginTop: 4 }} viewBox="0 0 24 24" fill="none" stroke="var(--ink-tertiary)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="8" y1="12" x2="16" y2="12" />
                </svg>
                <span style={{ textWrap: "pretty" }}>A rehearsed script read out loud, or written English typed in, is a poor fit. A polished performance hides how you really talk, and how you really talk is the one thing we listen for.</span>
              </div>
              <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                <svg width="15" height="15" style={{ flexShrink: 0, marginTop: 4 }} viewBox="0 0 24 24" fill="none" stroke="var(--ink-tertiary)" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                  <circle cx="12" cy="12" r="10" />
                  <line x1="12" y1="16" x2="12" y2="12" />
                  <line x1="12" y1="8" x2="12.01" y2="8" />
                </svg>
                <span style={{ textWrap: "pretty" }}>This is a learning-fit suggestion, not a score on your voice or your English.</span>
              </div>
            </div>
          </div>
        </section>
      </RevealScope>

      {/* Beat 5: vision */}
      <section style={{ background: "var(--bg-subtle)", borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)", padding: "96px 0" }}>
        <RevealScope style={{ maxWidth: 1040, margin: "0 auto", padding: "0 24px" }}>
          <div data-reveal="rise" style={{ opacity: 0, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 20, marginBottom: 96 }}>
            <div style={{ ...cardBase, padding: 24 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
                <LivePill />
                <span style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 15, color: "var(--ink)" }}>In the demo today</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 11, fontSize: 14, color: "var(--ink-secondary)" }}>
                {["Record a clip in your own language", "The agent pipeline", "Evidence chains from your words", "The Confidence Judge", "Three real matches"].map((item) => (
                  <div key={item} style={{ display: "flex", gap: 9, alignItems: "flex-start" }}>
                    <Check size={15} style={{ flexShrink: 0, marginTop: 2 }} />
                    {item}
                  </div>
                ))}
              </div>
            </div>
            <div style={{ background: "var(--surface-card)", border: "1px dashed var(--border)", borderRadius: "var(--radius-lg)", padding: 24 }}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 16 }}>
                <ComingSoonPill />
                <span style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 15, color: "var(--ink)" }}>Where it is going</span>
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 11, fontSize: 14, color: "var(--ink-secondary)" }}>
                {["Personal Language Memory", "Your Language Twin", "The practice loop", "The creator network"].map((item) => (
                  <div key={item} style={{ display: "flex", gap: 9, alignItems: "flex-start" }}>
                    <span style={{ flexShrink: 0, marginTop: 7, width: 6, height: 6, borderRadius: "50%", background: "var(--ink-tertiary)" }} />
                    {item}
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div data-reveal="rise" style={{ opacity: 0, textAlign: "center", marginBottom: 44 }}>
            <SectionLabel style={{ marginBottom: 10 }}>The ideal app</SectionLabel>
            <h2 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 32, margin: 0, textWrap: "balance" }}>Where a Personal Language Twin takes this.</h2>
            <p style={{ fontSize: 15, lineHeight: 1.6, color: "var(--ink-tertiary)", margin: "12px auto 0", maxWidth: "48ch", textWrap: "pretty" }}>Everything below is the vision, mocked up, not built yet.</p>
          </div>

          <div style={{ display: "flex", flexDirection: "column", gap: 28 }}>
            {/* Personal Language Memory */}
            <div data-reveal="rise" style={{ ...cardBase, opacity: 0, padding: 28 }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 6 }}>
                <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 21, color: "var(--ink)" }}>Personal Language Memory</div>
                <ComingSoonPill />
              </div>
              <p style={{ fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 15, color: "var(--blue-deep)", margin: "0 0 8px" }}>Your matches are step one. The profile keeps growing.</p>
              <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "0 0 20px", maxWidth: "62ch" }}>With your permission we save a profile of how you talk, never your audio, and show what grew between recordings.</p>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14, marginBottom: 16 }}>
                <div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: 20 }}>
                  <SectionLabel style={{ fontSize: 11, letterSpacing: "0.08em", marginBottom: 14 }}>Day 1</SectionLabel>
                  <div style={{ display: "flex", flexDirection: "column", gap: 12, fontSize: 14, color: "var(--ink-secondary)" }}>
                    {dayRows("sometimes", "short", "rarely").map(([label, value]) => (
                      <div key={label}>
                        {label}: <span style={{ color: "var(--ink)", fontWeight: 500 }}>{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
                <div style={{ ...cardBase, padding: 20 }}>
                  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 14 }}>
                    <SectionLabel style={{ fontSize: 11, letterSpacing: "0.08em", color: "var(--blue-deep)" }}>Day 14</SectionLabel>
                  </div>
                  <div style={{ display: "flex", flexDirection: "column", gap: 12, fontSize: 14, color: "var(--ink-secondary)" }}>
                    {dayRows("clearly", "a little longer", "more often").map(([label, value]) => (
                      <div key={label}>
                        {label}: <span style={{ color: "var(--ink)", fontWeight: 500 }}>{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
              <div style={{ display: "flex", alignItems: "center", gap: 12, background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: "14px 16px" }}>
                <span style={{ width: 40, height: 24, flexShrink: 0, borderRadius: 999, background: "var(--border)", position: "relative", display: "block" }}>
                  <span style={{ position: "absolute", top: 3, left: 3, width: 18, height: 18, borderRadius: "50%", background: "#fff", boxShadow: "var(--shadow-card)" }} />
                </span>
                <span style={{ fontSize: 14, color: "var(--ink-secondary)" }}>Save my talk profile (you can delete it anytime)</span>
                <span style={{ marginLeft: "auto", fontFamily: "var(--font-display)", fontSize: 12, fontWeight: 500, color: "var(--ink-tertiary)", flexShrink: 0 }}>Off by default</span>
              </div>
            </div>

            {/* Your Language Twin */}
            <div data-reveal="rise" style={{ ...cardBase, opacity: 0, padding: 28 }}>
              <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 6 }}>
                <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 21, color: "var(--ink)" }}>Your Language Twin</div>
                <ComingSoonPill />
              </div>
              <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "0 0 20px", maxWidth: "62ch" }}>Every session adds to a living picture of how you talk, so your matches and practice get sharper over time.</p>
              <div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: 24 }}>
                <div style={{ display: "flex", alignItems: "center", gap: 14, marginBottom: 20 }}>
                  <span style={{ width: 48, height: 48, flexShrink: 0, borderRadius: "var(--radius-md)", background: "var(--avatar-gradient)", display: "block" }} />
                  <div>
                    <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 17, color: "var(--ink)" }}>Your talk profile</div>
                    <div style={{ fontSize: 13, color: "var(--ink-tertiary)" }}>built from the clips you share</div>
                  </div>
                </div>
                <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
                  {twinBars.map(([label, value]) => (
                    <div key={label}>
                      <div style={{ display: "flex", justifyContent: "space-between", fontSize: 13, color: "var(--ink)", marginBottom: 6, gap: 8 }}>
                        <span style={{ fontFamily: "var(--font-display)", fontWeight: 500, whiteSpace: "nowrap" }}>{label}</span>
                        <span style={{ color: "var(--ink-tertiary)", fontSize: 12 }}>seen in your clips</span>
                      </div>
                      <div style={{ height: 8, borderRadius: 999, background: "var(--border)", overflow: "hidden" }}>
                        <div style={{ height: "100%", width: `${value}%`, borderRadius: 999, background: "var(--blue-deep)" }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Practice loop + creator network */}
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 28 }}>
              <div data-reveal="rise" style={{ ...cardBase, opacity: 0, padding: 28 }}>
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 18 }}>
                  <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 18, color: "var(--ink)", textWrap: "balance" }}>Finding your match is step one of a loop.</div>
                  <ComingSoonPill />
                </div>
                <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap", marginBottom: 16 }}>
                  {["Understand you", "Find your match", "Practice with them", "See what grew"].map((label, index, arr) => (
                    <span key={label} style={{ display: "contents" }}>
                      <span style={{ fontFamily: "var(--font-display)", fontSize: 14, fontWeight: 500, color: "var(--ink)", background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: 999, padding: "9px 15px" }}>{label}</span>
                      {index < arr.length - 1 ? <span style={{ color: "var(--ink-tertiary)" }}>&rarr;</span> : null}
                    </span>
                  ))}
                  <span style={{ color: "var(--ink-tertiary)" }}>&#8617;</span>
                  <span style={{ fontFamily: "var(--font-display)", fontSize: 14, fontWeight: 500, color: "var(--ink-tertiary)" }}>then a fresh match</span>
                </div>
                <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: 0 }}>Each pass through the loop starts from a sharper picture of how you talk.</p>
              </div>

              <div data-reveal="rise" data-delay="0.15s" style={{ ...cardBase, opacity: 0, padding: 28 }}>
                <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 18 }}>
                  <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 18, color: "var(--ink)", textWrap: "balance" }}>A new way for real creators to be found.</div>
                  <ComingSoonPill />
                </div>
                <p style={{ fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 15, color: "var(--blue-deep)", margin: "0 0 14px" }}>The role models are real English vloggers, and that pool keeps growing.</p>
                <div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", padding: "16px 12px 8px", marginBottom: 12 }}>
                  <svg viewBox="0 0 460 280" style={{ display: "block", width: "100%", height: "auto" }} role="img" aria-label="Learners matched to creators, one small new creator receiving its first match">
                    <defs>
                      <linearGradient id="lrm-node-grad" x1="0" y1="0" x2="1" y2="1">
                        <stop offset="0" stopColor="var(--blue-deep)" />
                        <stop offset="1" stopColor="#6f8ff5" />
                      </linearGradient>
                    </defs>
                    <text x="55" y="26" textAnchor="middle" fontSize="11" fontWeight="500" letterSpacing="1" fill="var(--ink-tertiary)" style={{ textTransform: "uppercase", fontFamily: "var(--font-display)" }}>Learners</text>
                    <text x="270" y="26" textAnchor="middle" fontSize="11" fontWeight="500" letterSpacing="1" fill="var(--ink-tertiary)" style={{ textTransform: "uppercase", fontFamily: "var(--font-display)" }}>Creators</text>
                    <line x1="65" y1="58" x2="253" y2="76" stroke="var(--blue-deep)" strokeWidth="1.5" opacity="0.45" />
                    <line x1="65" y1="104" x2="253" y2="82" stroke="var(--blue-deep)" strokeWidth="1.5" opacity="0.45" />
                    <line x1="65" y1="150" x2="253" y2="90" stroke="var(--blue-deep)" strokeWidth="1.5" opacity="0.45" />
                    <line x1="65" y1="196" x2="253" y2="168" stroke="var(--blue-deep)" strokeWidth="1.5" opacity="0.45" />
                    <line x1="65" y1="242" x2="256" y2="240" stroke="var(--blue-deep)" strokeWidth="2" />
                    <circle cx="55" cy="58" r="10" fill="#d4d4d8" />
                    <circle cx="55" cy="104" r="10" fill="#d4d4d8" />
                    <circle cx="55" cy="150" r="10" fill="#d4d4d8" />
                    <circle cx="55" cy="196" r="10" fill="#d4d4d8" />
                    <circle cx="55" cy="242" r="10" fill="#d4d4d8" />
                    <circle cx="270" cy="82" r="18" fill="url(#lrm-node-grad)" />
                    <circle cx="270" cy="168" r="16" fill="url(#lrm-node-grad)" />
                    <circle cx="270" cy="240" r="12" fill="url(#lrm-node-grad)" />
                    <circle cx="270" cy="240" r="19" fill="none" stroke="var(--blue-deep)" strokeWidth="1.5" strokeDasharray="4 4" />
                    <text x="298" y="78" fontSize="11" fill="var(--blue-deep)" fontWeight="500" style={{ fontFamily: "var(--font-display)" }}>found by learners</text>
                    <text x="298" y="92" fontSize="11" fill="var(--blue-deep)" fontWeight="500" style={{ fontFamily: "var(--font-display)" }}>who talk like them</text>
                    <text x="298" y="238" fontSize="11" fill="var(--blue-deep)" fontWeight="500" style={{ fontFamily: "var(--font-display)" }}>a small channel,</text>
                    <text x="298" y="252" fontSize="11" fill="var(--blue-deep)" fontWeight="500" style={{ fontFamily: "var(--font-display)" }}>first match</text>
                  </svg>
                  <div style={{ display: "flex", alignItems: "center", gap: 18, flexWrap: "wrap", padding: "8px 4px 6px" }}>
                    <span style={{ display: "inline-flex", alignItems: "center", gap: 7, fontSize: 12, color: "var(--ink-tertiary)" }}>
                      <svg width="22" height="8" viewBox="0 0 22 8" aria-hidden="true"><line x1="1" y1="4" x2="21" y2="4" stroke="var(--blue-deep)" strokeWidth="1.5" opacity="0.45" /></svg>
                      matched
                    </span>
                    <span style={{ display: "inline-flex", alignItems: "center", gap: 7, fontSize: 12, color: "var(--ink-tertiary)" }}>
                      <svg width="18" height="18" viewBox="0 0 18 18" aria-hidden="true"><circle cx="9" cy="9" r="4.5" fill="url(#lrm-node-grad)" /><circle cx="9" cy="9" r="8" fill="none" stroke="var(--blue-deep)" strokeWidth="1.2" strokeDasharray="3 3" /></svg>
                      gets discovered
                    </span>
                  </div>
                </div>
                <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "0 0 10px" }}>When a learner matches a creator, that creator gets in front of exactly the person who wants to learn from them. For a small vlogger, that is a new way to be discovered, not through ads, but through the way they talk.</p>
                <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-tertiary)", margin: 0 }}>More learners means better matches and more creators found. A bigger pool of creators means a better match for every learner.</p>
              </div>
            </div>
          </div>
        </RevealScope>
      </section>

      {/* Beat 6: close */}
      <section style={{ maxWidth: 720, margin: "0 auto", padding: "88px 24px", textAlign: "center" }}>
        <div style={{ display: "flex", justifyContent: "center", marginBottom: 32 }}>
          <Link className="dc-btn dc-btn-primary" href="/app" style={{ padding: "15px 28px", fontSize: 16 }}>
            Try the demo
          </Link>
        </div>
        <div style={{ borderTop: "1px solid var(--border)", paddingTop: 20, display: "flex", flexDirection: "column", gap: 6, alignItems: "center" }}>
          <p style={{ fontSize: 13, color: "var(--ink-tertiary)", margin: 0 }}>Not affiliated with or endorsed by any creator.</p>
          <a className="dc-inline-link" href={`mailto:${CONTACT_EMAIL}`} style={{ fontSize: 13 }}>Request removal</a>
        </div>
      </section>
    </main>
  );
}
