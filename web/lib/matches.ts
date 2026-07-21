export const CONTACT_EMAIL = "takedown@languagerolemodel.app";
export const RESULT_STORAGE_KEY = "your-ideal-role-model-results";

export type Evidence = {
  trait_id: string;
  you_quote: { sentence_id: string; text: string };
  creator_descriptor: string;
  match_reason: string;
};

export type Match = {
  creator_id: string;
  name: string;
  role: string;
  video_url: string;
  similarity: number;
  resemblance: "strong" | "clear" | "partial";
  trait_chips: string[];
  evidence: Evidence[];
  why: string;
};

export type StepTrace = { step: string; status: "started" | "completed" | "failed" | "skipped"; elapsed_ms: number };
export type MatchResponse = {
  matches: Match[];
  step_trace: StepTrace[];
  audio_deleted: boolean;
  judge_skipped?: boolean;
  match_confidence_capped?: boolean;
  memory_available?: boolean;
  message?: string | null;
};

export const labelForStep = (step: string) => ({
  transcript: "Transcript Agent",
  input_gate: "Input check",
  style_reader: "Thinking Style Agent",
  matcher: "Role Model Matching Agent",
  memory: "Memory",
  evidence_writer: "Evidence Agent",
  confidence_judge: "Confidence Judge",
}[step] ?? step.replaceAll("_", " "));
