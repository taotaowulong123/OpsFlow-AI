import type { Task, TaskRun, RunStep, Document, SearchResult, Tool, Skill } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

// Tasks
export function createTask(title: string, description: string) {
  return request<Task>("/api/tasks", { method: "POST", body: JSON.stringify({ title, description }) });
}

export function getTasks() {
  return request<Task[]>("/api/tasks");
}

export function getTask(id: string) {
  return request<Task>(`/api/tasks/${id}`);
}

export function runTask(taskId: string): EventSource {
  return new EventSource(`${API_URL}/api/tasks/${taskId}/run`);
}

// Knowledge
export function getDocuments() {
  return request<Document[]>("/api/knowledge");
}

export async function uploadDocument(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/api/knowledge/upload`, { method: "POST", body: form });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json() as Promise<Document>;
}

export function deleteDocument(id: string) {
  return request<void>(`/api/knowledge/${id}`, { method: "DELETE" });
}

export function searchKnowledge(query: string) {
  return request<SearchResult[]>(`/api/knowledge/search?q=${encodeURIComponent(query)}`);
}

// Tools
export function getTools() {
  return request<Tool[]>("/api/tools");
}

// Runs
export function getRuns() {
  return request<TaskRun[]>("/api/runs");
}

export function getRun(id: string) {
  return request<TaskRun>(`/api/runs/${id}`);
}

export function getRunSteps(runId: string) {
  return request<RunStep[]>(`/api/runs/${runId}/steps`);
}

export function approveRun(runId: string, stepId: string, approved: boolean, reason?: string) {
  return request<void>(`/api/runs/${runId}/approve`, {
    method: "POST",
    body: JSON.stringify({ step_id: stepId, approved, reason }),
  });
}

// Skills
export function fetchSkills(filters?: { category?: string; risk_level?: string; is_enabled?: boolean }) {
  const params = new URLSearchParams();
  if (filters?.category) params.set("category", filters.category);
  if (filters?.risk_level) params.set("risk_level", filters.risk_level);
  if (filters?.is_enabled !== undefined) params.set("is_enabled", String(filters.is_enabled));
  const qs = params.toString();
  return request<{ count: number; skills: Skill[] }>(`/api/skills${qs ? `?${qs}` : ""}`);
}

export function fetchSkill(id: string) {
  return request<Skill>(`/api/skills/${id}`);
}

export function toggleSkill(id: string) {
  return request<Skill>(`/api/skills/${id}/toggle`, { method: "POST" });
}

export function fetchSkillRuns(id: string) {
  return request<any[]>(`/api/skills/${id}/runs`);
}

export function syncSkills() {
  return request<{ synced: number }>("/api/skills/sync", { method: "POST" });
}

export function testSkill(id: string, input: string) {
  return request<any>(`/api/skills/${id}/test`, {
    method: "POST",
    body: JSON.stringify({ input }),
  });
}
