"use client";

import { ChangeEvent, FormEvent, useCallback, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { Check, Header, LivePill } from "@/components/ui";
import { ProcessingVisualizer } from "@/components/ProcessingVisualizer";
import { RESULT_STORAGE_KEY, type MatchResponse } from "@/lib/matches";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL ?? "http://127.0.0.1:8000";
export default function AppFlowPage() {
  const router = useRouter();
  const [audio, setAudio] = useState<File | null>(null);
  const [consent, setConsent] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [backendReady, setBackendReady] = useState(false);
  const [matchResult, setMatchResult] = useState<MatchResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    sessionStorage.removeItem(RESULT_STORAGE_KEY);
  }, []);

  function selectAudio(event: ChangeEvent<HTMLInputElement>) {
    setAudio(event.target.files?.[0] ?? null);
    setError("");
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!audio || !consent) {
      setError("Choose an audio file and confirm consent before continuing.");
      return;
    }
    const formData = new FormData();
    formData.append("audio", audio);
    setProcessing(true);
    setBackendReady(false);
    setMatchResult(null);
    setError("");
    try {
      const response = await fetch(`${BACKEND_URL}/match`, { method: "POST", body: formData });
      const payload = (await response.json()) as MatchResponse | { detail?: string };
      if (!response.ok) throw new Error("detail" in payload ? payload.detail : "The match could not be completed. Please try again.");
      if (!("matches" in payload) || payload.matches.length !== 3)
        throw new Error("message" in payload && payload.message ? payload.message : "The match could not be completed. Please try again.");
      setMatchResult(payload);
      setBackendReady(true);
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "The match could not be completed. Please try again.");
      setProcessing(false);
    }
  }

  const finishProcessing = useCallback(() => {
    if (!matchResult) return;
    sessionStorage.setItem(RESULT_STORAGE_KEY, JSON.stringify(matchResult));
    router.push("/app/results");
  }, [matchResult, router]);

  return (
    <main className="lrm-page">
      <Header variant="app" />
      {processing ? (
        <ProcessingVisualizer backendReady={backendReady} onFinished={finishProcessing} />
      ) : (
        <div style={{ maxWidth: 560, margin: "0 auto", padding: "56px 24px 80px" }}>
          <div style={{ textAlign: "center", marginBottom: 32 }}>
            <div style={{ marginBottom: 16 }}>
              <LivePill />
            </div>
            <h1 style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 32, lineHeight: 1.12, letterSpacing: "-0.015em", margin: 0, textWrap: "pretty" }}>
              Learn English from someone who already talks the way you do.
            </h1>
            <p style={{ fontSize: 15, lineHeight: 1.6, color: "var(--ink-secondary)", margin: "16px auto 0", maxWidth: "46ch", textWrap: "pretty" }}>
              The way you build a sentence, ask a question, or tell a story is similar in any language, and that is what we listen for.
            </p>
          </div>

          <form
            onSubmit={submit}
            style={{ background: "var(--surface-card)", border: "1px solid var(--border)", borderRadius: "var(--radius-lg)", boxShadow: "var(--shadow-raised)", padding: 28, display: "flex", flexDirection: "column", gap: 18 }}
          >
            <div>
              <div style={{ fontFamily: "var(--font-display)", fontWeight: 600, fontSize: 18, color: "var(--ink)" }}>Choose a voice note</div>
              <p style={{ fontSize: 13, lineHeight: 1.5, color: "var(--ink-tertiary)", margin: "6px 0 0" }}>
                About a minute or two of natural talking works best. Speak in your own language, the way you would with a friend.
              </p>
            </div>

            <div style={{ display: "flex", alignItems: "center", gap: 14, flexWrap: "wrap" }}>
              <label className="dc-btn dc-btn-secondary" style={{ padding: "11px 18px", fontSize: 15, cursor: "pointer" }}>
                Choose file
                <input accept="audio/*,.m4a,.mp3,.wav,.mp4,.webm,.ogg" onChange={selectAudio} type="file" style={{ display: "none" }} />
              </label>
              {audio ? (
                <span style={{ fontSize: 14, color: "var(--ink-tertiary)", minWidth: 0, overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>Selected: {audio.name}</span>
              ) : null}
            </div>

            <div style={{ height: 1, background: "var(--border)" }} />

            <label style={{ display: "flex", alignItems: "flex-start", gap: 12, cursor: "pointer", fontSize: 15, lineHeight: 1.5, color: "var(--ink-secondary)" }}>
              <input
                type="checkbox"
                checked={consent}
                onChange={(event) => {
                  setConsent(event.target.checked);
                  setError("");
                }}
                style={{ position: "absolute", width: 1, height: 1, padding: 0, margin: -1, overflow: "hidden", clip: "rect(0 0 0 0)", whiteSpace: "nowrap", border: 0 }}
              />
              <span
                aria-hidden="true"
                style={{
                  width: 20,
                  height: 20,
                  flexShrink: 0,
                  marginTop: 1,
                  borderRadius: 6,
                  border: `1.5px solid ${consent ? "var(--blue-deep)" : "var(--border)"}`,
                  background: consent ? "var(--blue-deep)" : "var(--bg-base)",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  transition: "background 120ms ease, border-color 120ms ease",
                }}
              >
                {consent ? <Check size={13} stroke="#fff" strokeWidth={3} /> : null}
              </span>
              <span>I&apos;m okay with my clip being analyzed to find my matches. It is deleted right after.</span>
            </label>

            <p style={{ fontSize: 13, lineHeight: 1.5, color: "var(--ink-tertiary)", margin: 0 }}>You confirm that you are 18 or older.</p>

            {error ? <p style={{ fontSize: 14, lineHeight: 1.5, color: "var(--ink-tertiary)", margin: 0 }}>{error}</p> : null}

            <button className="dc-btn dc-btn-primary" disabled={!audio || !consent} type="submit" style={{ padding: "15px 26px", fontSize: 16, width: "100%" }}>
              Find my matches
            </button>
          </form>
        </div>
      )}
    </main>
  );
}
