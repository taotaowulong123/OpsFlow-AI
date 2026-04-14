"use client";

import { useState, Fragment } from "react";
import { ChevronDown, ChevronRight, Filter } from "lucide-react";
import type { TaskRun, RunStep, TaskStatus } from "@/types";
import { cn, formatDate, formatTokens, statusColor } from "@/lib/utils";
import { StepCard } from "@/components/StepCard";
import { useTranslations } from "next-intl";

const mockRuns: (TaskRun & { task_title: string; steps: RunStep[] })[] = [
  {
    id: "r1", task_id: "1", task_title: "Generate quarterly report", status: "completed",
    started_at: "2026-04-15T09:00:00Z", finished_at: "2026-04-15T09:05:00Z", total_tokens: 4520,
    steps: [
      { id: "s1", run_id: "r1", node_name: "Planner", status: "completed", input_data: { task: "Generate report" }, output_data: { plan: "1. Gather data 2. Analyze 3. Format" }, evidence: [], tokens_used: 1200, latency_ms: 1800, error_message: null },
      { id: "s2", run_id: "r1", node_name: "Retriever", status: "completed", input_data: { query: "Q1 2026 data" }, output_data: { chunks: 5 }, evidence: ["revenue.pdf"], tokens_used: 800, latency_ms: 950, error_message: null },
      { id: "s3", run_id: "r1", node_name: "Executor", status: "completed", input_data: { action: "generate" }, output_data: { file: "report.pdf" }, evidence: [], tokens_used: 2000, latency_ms: 3200, error_message: null },
      { id: "s4", run_id: "r1", node_name: "Reviewer", status: "completed", input_data: { review: "report.pdf" }, output_data: { approved: true }, evidence: [], tokens_used: 520, latency_ms: 800, error_message: null },
    ],
  },
  {
    id: "r2", task_id: "2", task_title: "Analyze customer feedback", status: "executing",
    started_at: "2026-04-15T10:00:00Z", finished_at: null, total_tokens: 1800,
    steps: [
      { id: "s5", run_id: "r2", node_name: "Planner", status: "completed", input_data: { task: "Analyze feedback" }, output_data: { plan: "1. Collect 2. Categorize 3. Summarize" }, evidence: [], tokens_used: 1100, latency_ms: 1500, error_message: null },
      { id: "s6", run_id: "r2", node_name: "Retriever", status: "in_progress", input_data: { query: "customer feedback" }, output_data: {}, evidence: [], tokens_used: 700, latency_ms: 0, error_message: null },
    ],
  },
  {
    id: "r3", task_id: "4", task_title: "Deploy staging environment", status: "failed",
    started_at: "2026-04-14T11:00:00Z", finished_at: "2026-04-14T11:03:00Z", total_tokens: 2100,
    steps: [
      { id: "s7", run_id: "r3", node_name: "Planner", status: "completed", input_data: { task: "Deploy staging" }, output_data: { plan: "1. Build 2. Test 3. Deploy" }, evidence: [], tokens_used: 900, latency_ms: 1200, error_message: null },
      { id: "s8", run_id: "r3", node_name: "Executor", status: "failed", input_data: { action: "deploy" }, output_data: {}, evidence: [], tokens_used: 1200, latency_ms: 2800, error_message: "Connection refused: staging server unreachable" },
    ],
  },
];

const filterOptions: TaskStatus[] = ["completed", "executing", "failed", "pending", "waiting_approval"];

export default function RunsPage() {
  const [expandedRun, setExpandedRun] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const t = useTranslations("runs");

  const filtered = filter === "all" ? mockRuns : mockRuns.filter((r) => r.status === filter);

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold mb-1">{t("title")}</h1>
          <p className="text-sm text-gray-500">{t("subtitle")}</p>
        </div>
        <div className="flex items-center gap-2">
          <Filter className="w-4 h-4 text-gray-500" />
          <select value={filter} onChange={(e) => setFilter(e.target.value)} className="bg-panel border border-border rounded-lg px-3 py-1.5 text-sm text-gray-300 focus:outline-none focus:border-primary">
            <option value="all">{t("all")}</option>
            {filterOptions.map((s) => (
              <option key={s} value={s}>{s.replace("_", " ")}</option>
            ))}
          </select>
        </div>
      </div>
      <div className="bg-panel border border-border rounded-lg overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="text-xs text-gray-500 border-b border-border">
              <th className="w-8 px-3 py-2"></th>
              <th className="text-left px-3 py-2 font-medium">{t("id")}</th>
              <th className="text-left px-3 py-2 font-medium">{t("task")}</th>
              <th className="text-left px-3 py-2 font-medium">{t("status")}</th>
              <th className="text-left px-3 py-2 font-medium">{t("started")}</th>
              <th className="text-left px-3 py-2 font-medium">{t("tokens")}</th>
              <th className="text-left px-3 py-2 font-medium">{t("steps")}</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {filtered.map((run) => (
              <Fragment key={run.id}>
                <tr onClick={() => setExpandedRun(expandedRun === run.id ? null : run.id)} className="hover:bg-white/5 transition-colors cursor-pointer">
                  <td className="px-3 py-2.5">{expandedRun === run.id ? <ChevronDown className="w-4 h-4 text-gray-500" /> : <ChevronRight className="w-4 h-4 text-gray-500" />}</td>
                  <td className="px-3 py-2.5 text-xs text-gray-400 font-mono">{run.id}</td>
                  <td className="px-3 py-2.5 text-sm">{run.task_title}</td>
                  <td className="px-3 py-2.5"><span className={cn("text-xs capitalize", statusColor(run.status))}>{run.status.replace("_", " ")}</span></td>
                  <td className="px-3 py-2.5 text-xs text-gray-500">{formatDate(run.started_at)}</td>
                  <td className="px-3 py-2.5 text-xs text-gray-400">{formatTokens(run.total_tokens)}</td>
                  <td className="px-3 py-2.5 text-xs text-gray-400">{run.steps.length}</td>
                </tr>
                {expandedRun === run.id && (
                  <tr><td colSpan={7} className="px-6 py-4 bg-surface"><div className="space-y-2">{run.steps.map((step) => (<StepCard key={step.id} step={step} />))}</div></td></tr>
                )}
              </Fragment>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
