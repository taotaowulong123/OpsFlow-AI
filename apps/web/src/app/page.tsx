"use client";

import { useEffect, useMemo, useState } from "react";
import { BarChart3, CheckCircle, Clock, Coins, Send } from "lucide-react";
import { getRuns, getTasks } from "@/lib/api";
import { cn, formatDate, statusColor } from "@/lib/utils";
import type { Task, TaskRun } from "@/types";
import { useTranslations } from "next-intl";

function formatCompactNumber(value: number) {
  return new Intl.NumberFormat("en", {
    notation: "compact",
    maximumFractionDigits: value >= 1_000_000 ? 1 : 0,
  }).format(value);
}

function formatAverageDuration(runs: TaskRun[]) {
  const completedRuns = runs.filter((run) => run.started_at && run.finished_at);
  if (completedRuns.length === 0) return "--";

  const totalMs = completedRuns.reduce((sum, run) => {
    const startedAt = new Date(run.started_at).getTime();
    const finishedAt = new Date(run.finished_at as string).getTime();
    return sum + Math.max(finishedAt - startedAt, 0);
  }, 0);

  const averageMs = totalMs / completedRuns.length;
  if (averageMs < 1000) return `${Math.round(averageMs)}ms`;
  return `${(averageMs / 1000).toFixed(1)}s`;
}

export default function DashboardPage() {
  const [quickInput, setQuickInput] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [runs, setRuns] = useState<TaskRun[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const t = useTranslations("dashboard");

  useEffect(() => {
    let active = true;

    async function loadDashboard() {
      setLoading(true);
      setError(null);

      try {
        const [taskData, runData] = await Promise.all([getTasks(), getRuns()]);
        if (!active) return;
        setTasks(taskData);
        setRuns(runData);
      } catch (err) {
        if (!active) return;
        const message = err instanceof Error ? err.message : "Failed to load dashboard";
        setError(message);
      } finally {
        if (active) {
          setLoading(false);
        }
      }
    }

    void loadDashboard();

    return () => {
      active = false;
    };
  }, []);

  const recentTasks = useMemo(() => tasks.slice(0, 6), [tasks]);

  const finishedRuns = useMemo(
    () => runs.filter((run) => run.status === "completed" || run.status === "failed"),
    [runs]
  );

  const completedRuns = useMemo(
    () => finishedRuns.filter((run) => run.status === "completed"),
    [finishedRuns]
  );

  const successRate =
    finishedRuns.length > 0 ? `${Math.round((completedRuns.length / finishedRuns.length) * 100)}%` : "--";

  const totalTokens = useMemo(
    () => runs.reduce((sum, run) => sum + (run.total_tokens ?? 0), 0),
    [runs]
  );

  const stats = [
    { label: t("totalTasks"), value: loading ? "--" : `${tasks.length}`, icon: BarChart3, color: "text-primary" },
    { label: t("successRate"), value: loading ? "--" : successRate, icon: CheckCircle, color: "text-green-400" },
    { label: t("avgDuration"), value: loading ? "--" : formatAverageDuration(runs), icon: Clock, color: "text-blue-400" },
    { label: t("totalTokens"), value: loading ? "--" : formatCompactNumber(totalTokens), icon: Coins, color: "text-yellow-400" },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-semibold mb-1">{t("title")}</h1>
        <p className="text-sm text-gray-500">{t("subtitle")}</p>
        {error ? <p className="mt-2 text-sm text-red-400">{error}</p> : null}
      </div>

      <div className="flex gap-2">
        <input
          value={quickInput}
          onChange={(e) => setQuickInput(e.target.value)}
          placeholder={t("quickTaskPlaceholder")}
          className="flex-1 bg-panel border border-border rounded-lg px-4 py-2.5 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-primary"
        />
        <button className="px-4 py-2.5 bg-primary text-white text-sm rounded-lg hover:bg-primary/80 transition-colors flex items-center gap-2">
          <Send className="w-4 h-4" />
          {t("run")}
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {stats.map((s) => (
          <div key={s.label} className="bg-panel border border-border rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs text-gray-500">{s.label}</span>
              <s.icon className={cn("w-4 h-4", s.color)} />
            </div>
            <p className="text-2xl font-semibold">{s.value}</p>
          </div>
        ))}
      </div>

      <div className="bg-panel border border-border rounded-lg">
        <div className="px-4 py-3 border-b border-border">
          <h2 className="text-sm font-medium">{t("recentTasks")}</h2>
        </div>
        <div className="divide-y divide-border">
          {loading ? (
            <div className="px-4 py-6 text-sm text-gray-500">Loading tasks...</div>
          ) : recentTasks.length > 0 ? (
            recentTasks.map((task) => (
              <div key={task.id} className="flex items-center gap-3 px-4 py-3 hover:bg-white/5 transition-colors">
                <div className={cn("w-2 h-2 rounded-full", statusColor(task.status).replace("text-", "bg-"))} />
                <span className="flex-1 text-sm">{task.title}</span>
                <span className={cn("text-xs capitalize", statusColor(task.status))}>{task.status.replace("_", " ")}</span>
                <span className="text-xs text-gray-500">{formatDate(task.created_at)}</span>
              </div>
            ))
          ) : (
            <div className="px-4 py-6 text-sm text-gray-500">No tasks yet.</div>
          )}
        </div>
      </div>
    </div>
  );
}
