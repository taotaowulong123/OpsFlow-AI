"use client";

import { useEffect, useMemo, useState, Fragment } from "react";
import { ChevronDown, ChevronRight, Filter } from "lucide-react";
import { getRuns, getTasks } from "@/lib/api";
import type { TaskRun, Task } from "@/types";
import { cn, formatDate, formatTokens, statusColor } from "@/lib/utils";
import { StepCard } from "@/components/StepCard";
import { useTranslations } from "next-intl";

type RunListItem = TaskRun & { task_title: string };

const filterOptions = ["running", "completed", "failed", "pending", "waiting_approval"] as const;

export default function RunsPage() {
  const [expandedRun, setExpandedRun] = useState<string | null>(null);
  const [filter, setFilter] = useState<string>("all");
  const [runs, setRuns] = useState<RunListItem[]>([]);
  const [initialLoading, setInitialLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const t = useTranslations("runs");

  useEffect(() => {
    let active = true;

    async function loadRuns(background = false) {
      if (!background) {
        setInitialLoading(true);
      }

      try {
        const [runData, taskData] = await Promise.all([getRuns(), getTasks()]);
        if (!active) return;

        const taskTitleMap = new Map(taskData.map((task: Task) => [task.id, task.title]));
        const hydratedRuns: RunListItem[] = runData.map((run) => ({
          ...run,
          task_title: taskTitleMap.get(run.task_id) ?? run.task_id,
        }));

        setRuns(hydratedRuns);
        setError(null);
      } catch (err) {
        if (!active) return;
        setError(err instanceof Error ? err.message : "Failed to load runs");
      } finally {
        if (active && !background) {
          setInitialLoading(false);
        }
      }
    }

    void loadRuns();
    const intervalId = window.setInterval(() => {
      void loadRuns(true);
    }, 3000);

    return () => {
      active = false;
      window.clearInterval(intervalId);
    };
  }, []);

  const filtered = useMemo(
    () => (filter === "all" ? runs : runs.filter((run) => run.status === filter)),
    [filter, runs]
  );

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold mb-1">{t("title")}</h1>
          <p className="text-sm text-gray-500">{t("subtitle")}</p>
          {error ? <p className="mt-2 text-sm text-red-400">{error}</p> : null}
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
            {initialLoading ? (
              <tr>
                <td colSpan={7} className="px-4 py-6 text-sm text-gray-500">
                  Loading runs...
                </td>
              </tr>
            ) : filtered.length > 0 ? (
              filtered.map((run) => (
                <Fragment key={run.id}>
                  <tr onClick={() => setExpandedRun(expandedRun === run.id ? null : run.id)} className="hover:bg-white/5 transition-colors cursor-pointer">
                    <td className="px-3 py-2.5">{expandedRun === run.id ? <ChevronDown className="w-4 h-4 text-gray-500" /> : <ChevronRight className="w-4 h-4 text-gray-500" />}</td>
                    <td className="px-3 py-2.5 text-xs text-gray-400 font-mono">{run.id}</td>
                    <td className="px-3 py-2.5 text-sm">{run.task_title}</td>
                    <td className="px-3 py-2.5"><span className={cn("text-xs capitalize", statusColor(run.status))}>{run.status.replace("_", " ")}</span></td>
                    <td className="px-3 py-2.5 text-xs text-gray-500">{formatDate(run.started_at)}</td>
                    <td className="px-3 py-2.5 text-xs text-gray-400">{formatTokens(run.total_tokens ?? 0)}</td>
                    <td className="px-3 py-2.5 text-xs text-gray-400">{run.steps?.length ?? 0}</td>
                  </tr>
                  {expandedRun === run.id && (
                    <tr>
                      <td colSpan={7} className="px-6 py-4 bg-surface">
                        <div className="space-y-2">
                          {(run.steps ?? []).length > 0 ? (
                            (run.steps ?? []).map((step) => <StepCard key={step.id} step={step} />)
                          ) : (
                            <p className="text-sm text-gray-500">No step data yet.</p>
                          )}
                        </div>
                      </td>
                    </tr>
                  )}
                </Fragment>
              ))
            ) : (
              <tr>
                <td colSpan={7} className="px-4 py-6 text-sm text-gray-500">
                  No runs yet.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
