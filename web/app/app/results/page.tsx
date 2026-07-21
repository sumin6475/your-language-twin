"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { ComingSoonVision } from "@/components/ComingSoonVision";
import { MatchCard } from "@/components/MatchCard";
import { Check, Header, LivePill, ShieldCheck } from "@/components/ui";
import { CONTACT_EMAIL, labelForStep, RESULT_STORAGE_KEY, type MatchResponse, type StepTrace } from "@/lib/matches";

export default function ResultsPage() {
  const [result, setResult] = useState<MatchResponse | null>(null);

  useEffect(() => {
    const saved = sessionStorage.getItem(RESULT_STORAGE_KEY);
    if (!saved) return;
    try {
      const parsed = JSON.parse(saved) as MatchResponse;
      if (parsed.matches.length === 3) setResult(parsed);
    } catch {
      sessionStorage.removeItem(RESULT_STORAGE_KEY);
    }
  }, []);

  if (!result) {
    return (
      <main className="lrm-page">
        <Header variant="app" />
        <div style={{ maxWidth: 520, margin: "0 auto", padding: "88px 24px" }}>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", textAlign: "center", gap: 20 }}>
            <span style={{ width: 56, height: 56, borderRadius: "var(--radius-lg)", background: "var(--bg-subtle)", border: "1px solid var(--border)", display: "flex", alignItems: "center", justifyContent: "center", color: "var(--ink-tertiary)" }}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
                <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3Z" />
                <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                <line x1="12" y1="19" x2="12" y2="22" />
              </svg>
            </span>
            <div>
              <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 22, color: "var(--ink)" }}>Your matches will appear here.</div>
              <p style={{ fontSize: 15, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "10px auto 0", maxWidth: "36ch", textWrap: "pretty" }}>
                Upload a clip first, then we can introduce you to three creators.
              </p>
            </div>
            <Link className="dc-btn dc-btn-primary" href="/app" style={{ padding: "15px 26px", fontSize: 16 }}>
              Choose an audio file
            </Link>
          </div>
        </div>
      </main>
    );
  }

  const stageTrace = result.step_trace.reduce<StepTrace[]>((stages, item) => {
    const index = stages.findIndex((stage) => stage.step === item.step);
    if (index === -1) stages.push(item);
    else stages[index] = item;
    return stages;
  }, []);
  const hasEvidence = result.matches.some((match) => match.evidence.length > 0);
  const isDegraded = result.analysis_complete === false || Boolean(result.degraded_reason) || !hasEvidence;
  const partialResultMessage = result.message ?? "We found possible creator matches, but the detailed evidence breakdown did not complete. Try another clip for a full explanation.";

  return (
    <main className="lrm-page">
      <Header variant="app" />
      <div style={{ maxWidth: 760, margin: "0 auto", padding: "48px 24px 72px" }}>
        <div style={{ textAlign: "center", marginBottom: 14 }}>
          <div style={{ marginBottom: 16 }}>
            <LivePill />
          </div>
          <h1 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 30, lineHeight: 1.15, letterSpacing: "-0.015em", margin: 0, textWrap: "pretty" }}>
            These three English speakers talk the way you do.
          </h1>
          <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-tertiary)", margin: "14px auto 0", maxWidth: "48ch", textWrap: "pretty" }}>
            {isDegraded
              ? "These are provisional learning-fit picks. The detailed comparison below shows which analysis steps completed."
              : "Each match comes with the exact things you both do the same way, checked against your own words. These are learning-fit picks, not a verdict on your voice."}
          </p>
          {result.match_confidence_capped ? (
            <p style={{ fontSize: 13, color: "var(--ink-tertiary)", margin: "10px auto 0", maxWidth: "48ch" }}>Based on a short sample, we are showing a careful first match.</p>
          ) : null}
        </div>

        {isDegraded ? (
          <div role="status" style={{ background: "var(--bg-subtle)", border: "1px dashed var(--border)", borderRadius: "var(--radius-md)", padding: "14px 16px", color: "var(--ink-secondary)", fontSize: 14, lineHeight: 1.55, marginTop: 24 }}>
            <span style={{ fontFamily: "var(--font-display)", fontWeight: 600, color: "var(--ink)", marginRight: 6 }}>Partial result.</span>
            {partialResultMessage}
          </div>
        ) : null}

        <section aria-label="Your creator matches" style={{ display: "flex", flexDirection: "column", gap: 24, marginTop: 36 }}>
          {result.matches.map((match, index) => (
            <MatchCard key={match.creator_id} match={match} judgeSkipped={result.judge_skipped} analysisComplete={result.analysis_complete} raised={index === 0} />
          ))}
        </section>

        {result.audio_deleted ? (
          <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, marginTop: 24, color: "var(--ink-tertiary)", fontSize: 13 }}>
            <Check size={15} strokeWidth={2.5} />
            Audio deleted. Nothing you said was stored.
          </div>
        ) : null}

        {/* How we got here — real step trace */}
        <div style={{ background: "var(--surface-card)", border: "1px solid var(--border)", borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-card)", padding: 22, marginTop: 36 }}>
          <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", gap: 12, marginBottom: 16 }}>
            <div>
              <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 16, color: "var(--ink)" }}>How we got here</div>
              <div style={{ fontSize: 13, color: "var(--ink-tertiary)", marginTop: 2 }}>The steps that produced these matches.</div>
            </div>
            <LivePill />
          </div>
          <div style={{ display: "flex", alignItems: "center", gap: 8, flexWrap: "wrap" }}>
            {stageTrace.map((item, index) => {
              const isJudgePassed = item.step === "confidence_judge" && item.status === "completed" && !result.judge_skipped && result.analysis_complete !== false;
              const state = item.status === "completed"
                ? { mark: "✓", copy: "completed", color: "var(--blue-deep)", background: "var(--blue-tint)", border: "1px solid #BFDBFE" }
                : item.status === "failed"
                  ? { mark: "×", copy: "failed", color: "#B91C1C", background: "#FEF2F2", border: "1px solid #FECACA" }
                  : item.status === "skipped"
                    ? { mark: "⊘", copy: "skipped", color: "var(--ink-tertiary)", background: "var(--bg-subtle)", border: "1px dashed var(--border)" }
                    : { mark: "…", copy: "not finished", color: "var(--ink-secondary)", background: "var(--bg-subtle)", border: "1px solid var(--border)" };
              return (
                <span key={`${item.step}-${item.elapsed_ms}-${index}`} style={{ display: "contents" }}>
                  {isJudgePassed ? (
                    <span style={{ display: "inline-flex", alignItems: "center", gap: 6, fontFamily: "var(--font-display)", fontSize: 13, fontWeight: 600, color: "var(--blue-deep)", background: "var(--blue-tint)", borderRadius: 999, padding: "6px 12px" }}>
                      <ShieldCheck size={12} stroke="var(--blue-deep)" strokeWidth={2.4} />
                      Confidence Judge passed
                    </span>
                  ) : (
                    <span style={{ display: "inline-flex", alignItems: "center", gap: 6, fontFamily: "var(--font-display)", fontSize: 13, fontWeight: 500, color: state.color, background: state.background, border: state.border, borderRadius: 999, padding: "6px 12px" }}>
                      <span aria-hidden="true">{state.mark}</span>
                      {labelForStep(item.step)}: {state.copy}
                    </span>
                  )}
                  {index < stageTrace.length - 1 ? <span style={{ color: "var(--ink-tertiary)" }}>&rarr;</span> : null}
                </span>
              );
            })}
          </div>
        </div>

        <div style={{ marginTop: 36 }}>
          <Link className="dc-btn dc-btn-primary" href="/app" style={{ width: "100%", padding: "16px 26px", fontSize: 16 }}>
            Try another clip
          </Link>
        </div>

        <ComingSoonVision />

        <footer style={{ borderTop: "1px solid var(--border)", marginTop: 40, paddingTop: 20, display: "flex", flexDirection: "column", gap: 6 }}>
          <p style={{ fontSize: 13, color: "var(--ink-tertiary)", margin: 0 }}>Not affiliated with or endorsed by any creator.</p>
          <a className="dc-inline-link" href={`mailto:${CONTACT_EMAIL}`} style={{ fontSize: 13, alignSelf: "flex-start" }}>
            Request removal
          </a>
        </footer>
      </div>
    </main>
  );
}
