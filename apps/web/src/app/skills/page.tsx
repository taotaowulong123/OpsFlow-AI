"use client";

import { useState } from "react";
import { RefreshCw, AlertTriangle, Wrench, Play } from "lucide-react";
import type { Skill } from "@/types";
import { cn } from "@/lib/utils";
import { useTranslations } from "next-intl";

const categoryColors: Record<string, string> = {
  domain: "bg-blue-400/10 text-blue-400",
  action: "bg-green-400/10 text-green-400",
  guardrail: "bg-yellow-400/10 text-yellow-400",
  composite: "bg-purple-400/10 text-purple-400",
};

const riskColors: Record<string, string> = {
  low: "bg-green-400/10 text-green-400",
  medium: "bg-yellow-400/10 text-yellow-400",
  high: "bg-red-400/10 text-red-400",
};

const mockSkills: Skill[] = [
  {
    id: "1", name: "knowledge-qa", display_name: "Knowledge QA with Citations",
    description: "Answer questions using the knowledge base with source citations and confidence scoring.",
    version: "0.1.0", category: "domain", risk_level: "low", is_builtin: true, is_enabled: true,
    triggers: ["查知识库", "知识问答", "FAQ", "search knowledge"],
    tools_allow: ["rag.search_kb"], approval_required_for: [],
    created_at: "2026-04-15T00:00:00Z", updated_at: "2026-04-15T00:00:00Z",
  },
  {
    id: "2", name: "refund-analyzer", display_name: "Refund Analyzer",
    description: "Analyze refund anomalies, retrieve SOP evidence, and generate an action draft with ticket.",
    version: "0.1.0", category: "domain", risk_level: "medium", is_builtin: true, is_enabled: true,
    triggers: ["退款异常", "退款率", "售后分析", "refund anomaly"],
    tools_allow: ["sql.query_refund_stats", "rag.search_sop", "http.create_ticket_draft", "browser.open_console"],
    approval_required_for: ["http.submit_ticket", "browser.click_submit"],
    created_at: "2026-04-15T00:00:00Z", updated_at: "2026-04-15T00:00:00Z",
  },
  {
    id: "3", name: "ticket-draft-writer", display_name: "Ticket Draft Writer",
    description: "Generate structured ticket or work order drafts from context and templates.",
    version: "0.1.0", category: "action", risk_level: "medium", is_builtin: true, is_enabled: true,
    triggers: ["生成工单", "创建工单", "draft ticket"],
    tools_allow: ["rag.search_kb", "http.create_ticket_draft"],
    approval_required_for: ["http.submit_ticket"],
    created_at: "2026-04-15T00:00:00Z", updated_at: "2026-04-15T00:00:00Z",
  },
  {
    id: "4", name: "browser-form-filler", display_name: "Browser Form Filler",
    description: "Automate browser-based form filling with field mapping, screenshot verification, and approval before submission.",
    version: "0.1.0", category: "action", risk_level: "high", is_builtin: true, is_enabled: false,
    triggers: ["填写表单", "打开后台", "browser form", "自动填报"],
    tools_allow: ["browser.navigate", "browser.fill", "browser.click", "browser.screenshot", "browser.get_text"],
    approval_required_for: ["browser.click_submit"],
    created_at: "2026-04-15T00:00:00Z", updated_at: "2026-04-15T00:00:00Z",
  },
  {
    id: "5", name: "daily-report-generator", display_name: "Daily Report Generator",
    description: "Aggregate data and generate daily or weekly summary reports in Markdown or CSV format.",
    version: "0.1.0", category: "action", risk_level: "low", is_builtin: true, is_enabled: true,
    triggers: ["生成日报", "生成周报", "daily report", "数据汇总"],
    tools_allow: ["sql.query_orders", "sql.query_refund_stats", "file.generate_markdown", "file.generate_csv"],
    approval_required_for: [],
    created_at: "2026-04-15T00:00:00Z", updated_at: "2026-04-15T00:00:00Z",
  },
];

export default function SkillsPage() {
  const [skills, setSkills] = useState<Skill[]>(mockSkills);
  const [categoryFilter, setCategoryFilter] = useState<string>("all");
  const [riskFilter, setRiskFilter] = useState<string>("all");
  const t = useTranslations("skills");

  function toggleSkill(id: string) {
    setSkills((prev) => prev.map((s) => (s.id === id ? { ...s, is_enabled: !s.is_enabled } : s)));
  }

  const filtered = skills.filter((s) => {
    if (categoryFilter !== "all" && s.category !== categoryFilter) return false;
    if (riskFilter !== "all" && s.risk_level !== riskFilter) return false;
    return true;
  });

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-semibold mb-1">{t("title")}</h1>
          <p className="text-sm text-gray-500">{t("subtitle")}</p>
        </div>
        <button className="px-4 py-2 bg-primary text-white text-sm rounded-lg hover:bg-primary/80 transition-colors flex items-center gap-2">
          <RefreshCw className="w-4 h-4" />
          {t("syncSkills")}
        </button>
      </div>

      <div className="flex items-center gap-3">
        <select value={categoryFilter} onChange={(e) => setCategoryFilter(e.target.value)} className="bg-panel border border-border rounded-lg px-3 py-1.5 text-sm text-gray-300 focus:outline-none focus:border-primary">
          <option value="all">{t("category")}</option>
          <option value="domain">{t("domain")}</option>
          <option value="action">{t("action")}</option>
          <option value="guardrail">{t("guardrail")}</option>
          <option value="composite">{t("composite")}</option>
        </select>
        <select value={riskFilter} onChange={(e) => setRiskFilter(e.target.value)} className="bg-panel border border-border rounded-lg px-3 py-1.5 text-sm text-gray-300 focus:outline-none focus:border-primary">
          <option value="all">{t("riskLevel")}</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map((skill) => (
          <div key={skill.id} className="bg-panel border border-border rounded-lg p-4 space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-sm font-medium">{skill.display_name}</h3>
                <p className="text-xs text-gray-500 font-mono">{skill.name}</p>
              </div>
              <button
                onClick={() => toggleSkill(skill.id)}
                className={cn("w-10 h-5 rounded-full transition-colors relative", skill.is_enabled ? "bg-primary" : "bg-gray-600")}
              >
                <div className={cn("w-4 h-4 bg-white rounded-full absolute top-0.5 transition-transform", skill.is_enabled ? "translate-x-5" : "translate-x-0.5")} />
              </button>
            </div>
            <p className="text-xs text-gray-400 leading-relaxed line-clamp-2">{skill.description}</p>
            <div className="flex items-center gap-2 flex-wrap">
              <span className={cn("text-xs px-2 py-0.5 rounded-full", categoryColors[skill.category])}>
                {skill.category}
              </span>
              <span className={cn("text-xs px-2 py-0.5 rounded-full flex items-center gap-1", riskColors[skill.risk_level])}>
                <AlertTriangle className="w-3 h-3" />
                {skill.risk_level}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-surface text-gray-400">
                v{skill.version}
              </span>
              <span className="text-xs px-2 py-0.5 rounded-full bg-surface text-gray-400 flex items-center gap-1">
                <Wrench className="w-3 h-3" />
                {skill.tools_allow.length} {t("toolsAllowed")}
              </span>
            </div>
            <div className="flex flex-wrap gap-1">
              {skill.triggers.slice(0, 4).map((trigger) => (
                <span key={trigger} className="text-xs px-2 py-0.5 rounded bg-white/5 text-gray-400">
                  {trigger}
                </span>
              ))}
              {skill.triggers.length > 4 && (
                <span className="text-xs px-2 py-0.5 text-gray-500">+{skill.triggers.length - 4}</span>
              )}
            </div>
            <div className="flex items-center gap-2 pt-1 border-t border-border">
              <button className="px-3 py-1.5 text-xs bg-primary/10 text-primary rounded-lg hover:bg-primary/20 transition-colors flex items-center gap-1">
                <Play className="w-3 h-3" />
                {t("test")}
              </button>
              {skill.approval_required_for.length > 0 && (
                <span className="text-xs text-yellow-400/70">
                  {skill.approval_required_for.length} approval gate(s)
                </span>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
