"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import type { Task, RunStep } from "@/types";
import { cn, formatDate, statusColor } from "@/lib/utils";
import { TaskConsole } from "@/components/TaskConsole";
import { EvidencePanel } from "@/components/EvidencePanel";
import { useTranslations } from "next-intl";

const mockTasks: Task[] = [
  { id: "1", title: "Generate quarterly report", description: "Create Q1 2026 report", status: "completed", created_at: "2026-04-15T09:00:00Z", updated_at: "2026-04-15T09:05:00Z" },
  { id: "2", title: "Analyze customer feedback", description: "Process latest survey", status: "executing", created_at: "2026-04-15T10:00:00Z", updated_at: "2026-04-15T10:02:00Z" },
  { id: "3", title: "Update API docs", description: "Sync with v2 endpoints", status: "completed", created_at: "2026-04-14T14:00:00Z", updated_at: "2026-04-14T14:08:00Z" },
];

export default function TasksPage() {
  const [selectedTask, setSelectedTask] = useState<string | null>(null);
  const [steps] = useState<RunStep[]>([]);
  const t = useTranslations("tasks");

  return (
    <div className="flex gap-4 h-[calc(100vh-3rem)]">
      <div className="w-64 flex-shrink-0 bg-panel border border-border rounded-lg flex flex-col">
        <div className="p-3 border-b border-border flex items-center justify-between">
          <span className="text-sm font-medium">{t("title")}</span>
          <button className="p-1 hover:bg-white/10 rounded transition-colors" title={t("newTask")}>
            <Plus className="w-4 h-4 text-gray-400" />
          </button>
        </div>
        <div className="flex-1 overflow-y-auto divide-y divide-border">
          {mockTasks.map((task) => (
            <button
              key={task.id}
              onClick={() => setSelectedTask(task.id)}
              className={cn(
                "w-full text-left px-3 py-2.5 hover:bg-white/5 transition-colors",
                selectedTask === task.id && "bg-primary/10"
              )}
            >
              <p className="text-sm truncate">{task.title}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className={cn("text-xs capitalize", statusColor(task.status))}>
                  {task.status.replace("_", " ")}
                </span>
                <span className="text-xs text-gray-500">{formatDate(task.created_at)}</span>
              </div>
            </button>
          ))}
        </div>
      </div>
      <div className="flex-1 min-w-0">
        <TaskConsole />
      </div>
      <div className="w-80 flex-shrink-0">
        <EvidencePanel steps={steps} />
      </div>
    </div>
  );
}
