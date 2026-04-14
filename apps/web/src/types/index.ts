export type TaskStatus =
  | "pending"
  | "planning"
  | "retrieving"
  | "executing"
  | "reviewing"
  | "running"
  | "waiting_approval"
  | "completed"
  | "failed";

export interface Task {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  created_at: string;
  updated_at: string;
}

export interface TaskRun {
  id: string;
  task_id: string;
  status: TaskStatus | "running";
  started_at: string;
  finished_at: string | null;
  total_tokens: number | null;
  total_cost?: number | null;
  steps?: RunStep[];
}

export interface RunStep {
  id: string;
  run_id: string;
  node_name: string;
  status: "pending" | "running" | "in_progress" | "completed" | "failed" | "waiting_approval";
  input_data: Record<string, unknown> | null;
  output_data: Record<string, unknown> | null;
  evidence: Record<string, unknown> | string[] | null;
  tokens_used: number | null;
  latency_ms: number | null;
  error_message: string | null;
}

export interface Document {
  id: string;
  filename: string;
  file_type: string;
  file_size: number;
  status: string;
  created_at: string;
}

export interface Tool {
  id: string;
  name: string;
  description: string;
  tool_type: string;
  enabled: boolean;
  risk_level: "low" | "medium" | "high";
}

export interface Approval {
  id: string;
  run_id: string;
  step_id: string;
  status: "pending" | "approved" | "rejected";
  reason: string;
}

export interface SearchResult {
  content: string;
  score: number;
  document_name: string;
  chunk_index: number;
}

export interface SSEEvent {
  event_type: string;
  data: Record<string, unknown>;
}

export interface Skill {
  id: string;
  name: string;
  display_name: string;
  description: string;
  version: string;
  category: "domain" | "action" | "guardrail" | "composite";
  risk_level: "low" | "medium" | "high";
  is_builtin: boolean;
  is_enabled: boolean;
  triggers: string[];
  tools_allow: string[];
  approval_required_for: string[];
  created_at: string;
  updated_at: string;
}

export interface SkillRun {
  id: string;
  task_id: string | null;
  skill_id: string;
  skill_version: string;
  status: string;
  started_at: string;
  completed_at: string | null;
  tokens_used: number;
  duration_ms: number | null;
}
