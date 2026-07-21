import { Fragment } from "react";
import Link from "next/link";

import { RevealScope } from "@/components/Reveal";
import { ArrowGlyph, Avatar, Badge, Header, LivePill, SectionLabel } from "@/components/ui";

const steps: [string, string, string][] = [
  ["1", "Speak your mind", "Record a minute or two in your own language. No script, no account, no sign up."],
  ["2", "We listen to how you talk", "We look at how you build a sentence: how you open, add to it, and land your point."],
  ["3", "Meet your matches", "Three English creators whose way of explaining feels familiar, with the reason for each."],
];

const examples: { name: string; role: string; resemblance: string; why: string; quote: string; then: string }[] = [
  {
    name: "Jay Shetty",
    role: "Warm, reflective story-to-lesson host",
    resemblance: "strong resemblance",
    why: "You start with a small personal moment, then quietly turn it into the point you wanted to make all along.",
    quote: '"Last week my sister called me."',
    then: "Jay opens with a moment from his own week.",
  },
  {
    name: "Ali Abdaal",
    role: "Calm, example-first productivity explainer",
    resemblance: "clear resemblance",
    why: "You build an argument by stacking small, concrete examples until the point feels obvious.",
    quote: '"For example, this morning I tried it."',
    then: "Ali proves it with a real example.",
  },
  {
    name: "Cleo Abram",
    role: "Curious, question-led tech storyteller",
    resemblance: "partial resemblance",
    why: "You open with the question everyone is quietly wondering, then answer it one honest step at a time.",
    quote: '"But why does that even happen?"',
    then: "Cleo opens on the question you are asking.",
  },
];

const cardBase = {
  background: "var(--surface-card)",
  border: "1px solid var(--border)",
  borderRadius: "var(--radius-lg)",
  boxShadow: "var(--shadow-card)",
} as const;

export default function LandingPage() {
  return (
    <main className="lrm-page">
      <Header />
      <RevealScope>
        {/* Hero */}
        <section style={{ maxWidth: 880, margin: "0 auto", padding: "110px 24px 88px", textAlign: "center" }}>
          <div data-reveal="rise" style={{ opacity: 0, display: "inline-flex", marginBottom: 26 }}>
            <Badge variant="neutral">Share a clip in your own language</Badge>
          </div>
          <h1
            data-reveal="rise"
            data-delay="0.15s"
            style={{ opacity: 0, fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 52, lineHeight: 1.12, letterSpacing: "-0.02em", margin: 0, textWrap: "balance" }}
          >
            Learn English from someone who already talks the way you do.
          </h1>
          <p
            data-reveal="rise"
            data-delay="0.4s"
            style={{ opacity: 0, fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 21, lineHeight: 1.5, color: "var(--ink)", margin: "28px auto 0", maxWidth: "44ch", textWrap: "balance" }}
          >
            Most apps help you sound like a native speaker.{" "}
            <span style={{ color: "var(--blue-deep)" }}>We find the native speaker who already sounds like you.</span>
          </p>
          <p
            data-reveal="rise"
            data-delay="0.55s"
            style={{ opacity: 0, fontSize: 15, lineHeight: 1.6, color: "var(--ink-tertiary)", margin: "16px auto 0", maxWidth: "52ch", textWrap: "pretty" }}
          >
            The way you build a sentence, ask a question, or tell a story is similar in any language, and that is what we
            listen for.
          </p>
          <div data-reveal="rise" data-delay="0.7s" style={{ opacity: 0, display: "flex", gap: 12, justifyContent: "center", marginTop: 36, flexWrap: "wrap" }}>
            <Link className="dc-btn dc-btn-primary" href="/app" style={{ padding: "15px 26px", fontSize: 16 }}>
              Try it, no account
            </Link>
            <a className="dc-btn dc-btn-secondary" href="#how-it-works" style={{ padding: "15px 26px", fontSize: 16 }}>
              See how it works
            </a>
          </div>
        </section>

        {/* How it works */}
        <section id="how-it-works" style={{ background: "var(--bg-subtle)", borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)" }}>
          <div style={{ maxWidth: 1020, margin: "0 auto", padding: "80px 24px" }}>
            <div data-reveal="rise" style={{ opacity: 0, textAlign: "center", marginBottom: 48 }}>
              <SectionLabel style={{ marginBottom: 12 }}>How it works</SectionLabel>
              <h2 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 28, margin: 0 }}>
                Three steps, about a minute or two
              </h2>
            </div>
            <div style={{ display: "grid", gridTemplateColumns: "1fr 24px 1fr 24px 1fr", alignItems: "stretch", gap: 0 }}>
              {steps.map(([number, title, copy], index) => (
                <Fragment key={number}>
                  <div data-reveal="rise" data-delay={index ? `${index * 0.15}s` : "0s"} style={{ opacity: 0 }}>
                    <div style={{ ...cardBase, padding: 24, height: "100%" }}>
                      <span
                        style={{
                          width: 28,
                          height: 28,
                          borderRadius: "50%",
                          background: "var(--blue-tint)",
                          color: "var(--blue-deep)",
                          fontFamily: "var(--font-display)",
                          fontWeight: 600,
                          fontSize: 13,
                          display: "flex",
                          alignItems: "center",
                          justifyContent: "center",
                          marginBottom: 14,
                        }}
                      >
                        {number}
                      </span>
                      <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 18, marginBottom: 8 }}>{title}</div>
                      <p style={{ fontSize: 15, lineHeight: 1.6, color: "var(--ink-secondary)", margin: 0 }}>{copy}</p>
                    </div>
                  </div>
                  {index < steps.length - 1 ? (
                    <div data-reveal="rise" data-delay={`${index * 0.15 + 0.1}s`} style={{ opacity: 0, display: "flex", alignItems: "center", justifyContent: "center" }}>
                      <ArrowGlyph />
                    </div>
                  ) : null}
                </Fragment>
              ))}
            </div>
            <div data-reveal="rise" data-delay="0.35s" style={{ opacity: 0, display: "flex", justifyContent: "center", marginTop: 40 }}>
              <Link className="dc-btn dc-btn-primary" href="/about" style={{ padding: "15px 26px", fontSize: 16 }}>
                See the whole idea <span aria-hidden="true">&rarr;</span>
              </Link>
            </div>
          </div>
        </section>

        {/* What you get back */}
        <section style={{ maxWidth: 1020, margin: "0 auto", padding: "96px 24px" }}>
          <div data-reveal="rise" style={{ opacity: 0, textAlign: "center", marginBottom: 48 }}>
            <div style={{ marginBottom: 14 }}>
              <LivePill />
            </div>
            <SectionLabel style={{ marginBottom: 12 }}>What you get back</SectionLabel>
            <h2 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 28, margin: 0, textWrap: "pretty" }}>
              Not just names. The reason each one fits.
            </h2>
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 20 }}>
            {examples.map((example, index) => (
              <div
                data-reveal="rise"
                data-delay={index ? `${index * 0.12}s` : "0s"}
                key={example.name}
                style={{ ...cardBase, opacity: 0, padding: 24, display: "flex", flexDirection: "column", gap: 14 }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                  <Avatar name={example.name} size={48} />
                  <div style={{ minWidth: 0, flex: 1 }}>
                    <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 17, color: "var(--ink)", lineHeight: 1.2 }}>{example.name}</div>
                    <div style={{ fontSize: 13, color: "var(--ink-tertiary)", marginTop: 3 }}>{example.role}</div>
                  </div>
                </div>
                <Badge variant="match">{example.resemblance}</Badge>
                <p style={{ fontSize: 15, lineHeight: 1.6, color: "var(--ink-secondary)", margin: 0, textWrap: "pretty" }}>{example.why}</p>
                <div style={{ background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-sm)", padding: "10px 12px", fontSize: 12, lineHeight: 1.55, color: "var(--ink-secondary)" }}>
                  <span style={{ fontFamily: "var(--font-display)", fontSize: 10, fontWeight: 500, letterSpacing: "0.08em", textTransform: "uppercase", color: "var(--ink-tertiary)", marginRight: 6 }}>
                    You said
                  </span>
                  {example.quote} <span style={{ color: "var(--ink-tertiary)" }}>then</span> {example.then}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* The bigger idea */}
        <section style={{ background: "var(--bg-subtle)", borderTop: "1px solid var(--border)", borderBottom: "1px solid var(--border)" }}>
          <div data-reveal="rise" style={{ opacity: 0, maxWidth: 720, margin: "0 auto", padding: "64px 24px", textAlign: "center" }}>
            <SectionLabel style={{ marginBottom: 14 }}>The bigger idea</SectionLabel>
            <p style={{ fontFamily: "var(--font-display)", fontWeight: 500, fontSize: 22, lineHeight: 1.45, color: "var(--ink)", margin: 0, textWrap: "balance" }}>
              This is step one of a loop that keeps building a profile of how you talk.
            </p>
            <div style={{ display: "flex", justifyContent: "center", marginTop: 24 }}>
              <Link className="dc-btn dc-btn-primary" href="/about" style={{ padding: "15px 26px", fontSize: 16 }}>
                See the whole idea <span aria-hidden="true">&rarr;</span>
              </Link>
            </div>
          </div>
        </section>
      </RevealScope>

      {/* Closing CTA */}
      <footer style={{ background: "var(--blue-deep)", color: "#fff" }}>
        <div style={{ maxWidth: 720, margin: "0 auto", padding: "88px 24px", textAlign: "center" }}>
          <h2 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 32, lineHeight: 1.15, margin: 0, textWrap: "pretty" }}>
            Someone already speaks English the way you do.
          </h2>
          <p style={{ fontSize: 16, lineHeight: 1.6, color: "rgba(255,255,255,0.82)", margin: "16px auto 0", maxWidth: "40ch" }}>
            Go find them. It takes a minute or two and no account.
          </p>
          <div style={{ display: "flex", justifyContent: "center", marginTop: 32 }}>
            <Link className="dc-btn dc-btn-white" href="/app" style={{ padding: "15px 28px", fontSize: 16 }}>
              Record my clip
            </Link>
          </div>
          <div style={{ marginTop: 56, paddingTop: 24, borderTop: "1px solid rgba(255,255,255,0.16)", display: "flex", justifyContent: "space-between", fontSize: 13, color: "rgba(255,255,255,0.6)" }}>
            <span>Language Role Model</span>
            <span>Your clip is analyzed, never shared.</span>
          </div>
        </div>
      </footer>
    </main>
  );
}
