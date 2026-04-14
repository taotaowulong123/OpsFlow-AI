import type { Task, TaskRun, RunStep, Document, SearchResult, Tool } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status} ${res.statusText}`);
  return res.json();
}

export function createTask(title: string, description: string) {
  return request<Task>("/tasks", {
    method: "POST",
    body: JSON.stringify({ title, description }),
  });
}

export function getTasks() {
  return request<Task[]>("/tasks");
}

export function getTask(id: string) {
  return request<Task>(`/tasks/${id}`);
}

export function runTask(taskId: string): EventSource {
  return new EventSource(`${API_URL}/tasks/${taskId}/run`);
}

export function getDocuments() {
  return request<Document[]>("/documents");
}

export async function uploadDocument(file: File) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API_URL}/documents`, { method: "POST", body: form });
  if (!res.ok) throw new Error(`Upload failed: ${res.status}`);
  return res.json() as Promise<Document>;
}

export function deleteDocument(id: string) {
  return request<void>(`/documents/${id}`, { method: "DELETE" });
}

export function searchKnowledge(query: string) {
  return request<SearchResult[]>(`/knowledge/search?q=${encodeURIComponent(query)}`);
}

export function getTools() {
  return request<Tool[]>("/tools");
}

export function getRuns() {
  return request<TaskRun[]>("/runs");
}

export function getRun(id: string) {
  return request<TaskRun>(`/runs/${id}`);
}

export function getRunSteps(runId: string) {
  return request<RunStep[]>(`/runs/${runId}/steps`);
}

export function approveRun(runId: string, stepId: string, approved: boolean, reason?: string) {
  return request<void>(`/runs/${runId}/approve`, {
    method: "POST",
    body: JSON.stringify({ step_id: stepId, approved, reason }),
  });
}
