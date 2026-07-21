"use client";

import { useEffect, useState } from "react";

import { Check, LivePill, ShieldCheck } from "@/components/ui";

const STEP_INTERVAL_MS = 2000;
const FINISH_DELAY_MS = 600;
const CONFIDENCE_STEP = 4;

type StepStatus = "pending" | "active" | "done";

const agents = [
  { title: "Turn your clip into text", copy: "We write down what you said and split it into sentences.", tag: "Transcript Agent" },
  { title: "Look at the way you talk", copy: "How you open a point, connect ideas, and land it.", tag: "Thinking Style Agent" },
  { title: "Find the creators who fit you", copy: "Line you up with creators we have looked at by hand.", tag: "Role Model Matching Agent" },
  { title: "Pull out what lines up", copy: "The exact lines where you and a creator do the same thing.", tag: "Evidence Agent" },
];

function StepIndicator({ status }: { status: StepStatus }) {
  if (status === "done") {
    return <span className="dc-step-status dc-step-status-done" aria-label="Complete"><Check size={13} stroke="#fff" strokeWidth={3} /></span>;
  }

  if (status === "active") {
    return <span className="dc-spin" aria-label="In progress" />;
  }

  return <span className="dc-step-status dc-step-status-pending" aria-label="Waiting" />;
}

export function ProcessingVisualizer({ backendReady, onFinished }: { backendReady: boolean; onFinished: () => void }) {
  const [activeStep, setActiveStep] = useState(0);
  const [confidenceComplete, setConfidenceComplete] = useState(false);

  useEffect(() => {
    const interval = window.setInterval(() => {
      setActiveStep((currentStep) => {
        if (currentStep >= CONFIDENCE_STEP) {
          window.clearInterval(interval);
          return currentStep;
        }

        const nextStep = currentStep + 1;
        if (nextStep === CONFIDENCE_STEP) window.clearInterval(interval);
        return nextStep;
      });
    }, STEP_INTERVAL_MS);

    return () => window.clearInterval(interval);
  }, []);

  useEffect(() => {
    if (backendReady && activeStep === CONFIDENCE_STEP) setConfidenceComplete(true);
  }, [activeStep, backendReady]);

  useEffect(() => {
    if (!confidenceComplete) return;

    const finishTimer = window.setTimeout(onFinished, FINISH_DELAY_MS);
    return () => window.clearTimeout(finishTimer);
  }, [confidenceComplete, onFinished]);

  const stepStatus = (index: number): StepStatus => {
    if (index === CONFIDENCE_STEP && confidenceComplete) return "done";
    if (index < activeStep) return "done";
    return index === activeStep ? "active" : "pending";
  };
  const confidenceStatus = stepStatus(CONFIDENCE_STEP);

  return (
    <div style={{ maxWidth: 660, margin: "0 auto", padding: "48px 24px 72px" }}>
      <div style={{ textAlign: "center", marginBottom: 36 }}>
        <div style={{ marginBottom: 16 }}><LivePill /></div>
        <h1 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 28, lineHeight: 1.15, letterSpacing: "-0.015em", margin: 0, textWrap: "pretty" }}>
          Finding the creators who talk the way you do.
        </h1>
        <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-tertiary)", margin: "14px auto 0", maxWidth: "46ch", textWrap: "pretty" }}>
          This is not one guess. A short chain of steps looks at your clip, then a last step checks every reason against your own words.
        </p>
        <div className="dc-dots" style={{ marginTop: 22 }} role="status" aria-label="Processing"><span /><span /><span /></div>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
        {agents.map((agent, index) => {
          const status = stepStatus(index);
          return (
            <div key={agent.tag} aria-label={`${agent.title}: ${status}`} style={{ opacity: 0, animation: "lrm-rise 460ms ease forwards", animationDelay: `${0.15 + index * 0.35}s`, display: "flex", alignItems: "center", gap: 14, background: "var(--surface-card)", border: "1px solid var(--border)", borderRadius: "var(--radius-md)", boxShadow: "var(--shadow-card)", padding: "14px 18px" }}>
              <span style={{ width: 24, height: 24, flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center" }}><StepIndicator status={status} /></span>
              <div style={{ flex: 1, minWidth: 0, opacity: status === "pending" ? 0.55 : 1 }}>
                <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 15, color: "var(--ink)" }}>{agent.title}</div>
                <div style={{ fontSize: 13, color: "var(--ink-tertiary)" }}>{agent.copy}</div>
              </div>
              <span className="dc-agent-tag" style={{ opacity: status === "pending" ? 0.55 : 1 }}>{agent.tag}</span>
            </div>
          );
        })}

        <div aria-label={`Confidence check: ${confidenceStatus}`} style={{ opacity: 0, animation: "lrm-rise 500ms ease forwards", animationDelay: "1.7s", position: "relative", overflow: "hidden", background: "var(--surface-card)", border: "1.5px solid var(--blue-deep)", borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-raised)", padding: 22, marginTop: 6 }}>
          <div style={{ display: "flex", alignItems: "flex-start", justifyContent: "space-between", gap: 12, marginBottom: 6 }}>
            <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
              <span style={{ width: 32, height: 32, flexShrink: 0, borderRadius: "var(--radius-md)", background: "var(--avatar-gradient)", display: "flex", alignItems: "center", justifyContent: "center" }}><ShieldCheck size={17} /></span>
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
          <p style={{ fontSize: 14, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "12px 0 16px", opacity: confidenceStatus === "pending" ? 0.55 : 1 }}>
            A second pass reads every reason back against your own words. If a reason is not clearly in your clip, it is dropped.
          </p>
          <div style={{ display: "flex", alignItems: "center", gap: 8, background: "var(--bg-subtle)", border: "1px solid var(--border)", borderRadius: "var(--radius-sm)", padding: "10px 12px", fontSize: 13, color: "var(--ink-secondary)" }}>
            <StepIndicator status={confidenceStatus} />
            {confidenceStatus === "pending" ? "Waiting to verify your result." : confidenceStatus === "active" ? "Checking the final evidence against your words…" : "Verification complete."}
          </div>
        </div>

        {confidenceComplete ? (
          <div className="dc-processing-footer" style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 10, marginTop: 16, fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 15, color: "var(--blue-deep)" }}>
            <span className="dc-spin" /> Building your Language Twin...
          </div>
        ) : null}
      </div>

      <div style={{ display: "flex", alignItems: "center", justifyContent: "center", gap: 8, marginTop: 24, color: "var(--ink-tertiary)", fontSize: 13 }}>
        <Check size={14} strokeWidth={2.5} />
        We use this clip only to make this match, then the backend deletes its request copy after transcription.
      </div>
    </div>
  );
}
