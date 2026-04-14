"use client";

import { useState } from "react";
import { BarChart3, CheckCircle, Clock, Coins, Send } from "lucide-react";
import { cn, formatDate, statusColor } from "@/lib/utils";
import type { Task } from "@/types";
import { useTranslations } from "next-intl";

const mockTasks: Task[] = [
  { id: "1", title: "Generate quarterly report", description: "", status: "completed", created_at: "2026-04-15T09:00:00Z", updated_at: "2026-04-15T09:05:00Z" },
  { id: "2", title: "Analyze customer feedback", description: "", status: "executing", created_at: "2026-04-15T10:00:00Z", updated_at: "2026-04-15T10:02:00Z" },
  { id: "3", title: "Update API documentation", description: "", status: "completed", created_at: "2026-04-14T14:00:00Z", updated_at: "2026-04-14T14:08:00Z" },
  { id: "4", title: "Deploy staging environment", description: "", status: "failed", created_at: "2026-04-14T11:00:00Z", updated_at: "2026-04-14T11:03:00Z" },
  { id: "5", title: "Run security audit", description: "", status: "waiting_approval", created_at: "2026-04-14T08:00:00Z", updated_at: "2026-04-14T08:10:00Z" },
  { id: "6", title: "Optimize database queries", description: "", status: "completed", created_at: "2026-04-13T16:00:00Z", updated_at: "2026-04-13T16:12:00Z" },
];

export default function DashboardPage() {
  const [quickInput, setQuickInput] = useState("");
  const t = useTranslations("dashboard");

  const stats = [
    { label: t("totalTasks"), value: "128", icon: BarChart3, color: "text-primary" },
    { label: t("successRate"), value: "94%", icon: CheckCircle, color: "text-green-400" },
    { label: t("avgDuration"), value: "4.2s", icon: Clock, color: "text-blue-400" },
    { label: t("totalTokens"), value: "1.2M", icon: Coins, color: "text-yellow-400" },
  ];

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-semibold mb-1">{t("title")}</h1>
        <p className="text-sm text-gray-500">{t("subtitle")}</p>
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
          {mockTasks.map((task) => (
            <div key={task.id} className="flex items-center gap-3 px-4 py-3 hover:bg-white/5 transition-colors">
              <div className={cn("w-2 h-2 rounded-full", statusColor(task.status).replace("text-", "bg-"))} />
              <span className="flex-1 text-sm">{task.title}</span>
              <span className={cn("text-xs capitalize", statusColor(task.status))}>{task.status.replace("_", " ")}</span>
              <span className="text-xs text-gray-500">{formatDate(task.created_at)}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
