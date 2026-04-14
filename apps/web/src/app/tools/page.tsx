"use client";

import { useState } from "react";
import { Database, Globe, Monitor, FileOutput, Search, AlertTriangle } from "lucide-react";
import type { Tool } from "@/types";
import { cn } from "@/lib/utils";
import { useTranslations } from "next-intl";

const iconMap: Record<string, React.ElementType> = {
  "SQL Query": Database,
  "HTTP Request": Globe,
  "Browser Automation": Monitor,
  "File Generator": FileOutput,
  "Knowledge Search": Search,
};

const riskColors = {
  low: "bg-green-400/10 text-green-400",
  medium: "bg-yellow-400/10 text-yellow-400",
  high: "bg-red-400/10 text-red-400",
};

const mockTools: Tool[] = [
  { id: "1", name: "SQL Query", description: "Execute read-only SQL queries against connected databases", tool_type: "database", enabled: true, risk_level: "medium" },
  { id: "2", name: "HTTP Request", description: "Make HTTP requests to external APIs and services", tool_type: "network", enabled: true, risk_level: "medium" },
  { id: "3", name: "Browser Automation", description: "Automate browser interactions for web scraping and testing", tool_type: "automation", enabled: false, risk_level: "high" },
  { id: "4", name: "File Generator", description: "Generate and write files to the output directory", tool_type: "filesystem", enabled: true, risk_level: "low" },
  { id: "5", name: "Knowledge Search", description: "Search the indexed knowledge base for relevant information", tool_type: "retrieval", enabled: true, risk_level: "low" },
];

export default function ToolsPage() {
  const [tools, setTools] = useState<Tool[]>(mockTools);
  const t = useTranslations("tools");

  function toggleTool(id: string) {
    setTools((prev) => prev.map((t) => (t.id === id ? { ...t, enabled: !t.enabled } : t)));
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-semibold mb-1">{t("title")}</h1>
        <p className="text-sm text-gray-500">{t("subtitle")}</p>
      </div>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tools.map((tool) => {
          const Icon = iconMap[tool.name] || Search;
          return (
            <div key={tool.id} className="bg-panel border border-border rounded-lg p-4 space-y-3">
              <div className="flex items-start justify-between">
                <div className="p-2 bg-surface rounded-lg">
                  <Icon className="w-5 h-5 text-primary" />
                </div>
                <button
                  onClick={() => toggleTool(tool.id)}
                  className={cn("w-10 h-5 rounded-full transition-colors relative", tool.enabled ? "bg-primary" : "bg-gray-600")}
                >
                  <div className={cn("w-4 h-4 bg-white rounded-full absolute top-0.5 transition-transform", tool.enabled ? "translate-x-5" : "translate-x-0.5")} />
                </button>
              </div>
              <div>
                <h3 className="text-sm font-medium mb-1">{tool.name}</h3>
                <p className="text-xs text-gray-400 leading-relaxed">{tool.description}</p>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs px-2 py-0.5 rounded-full bg-surface text-gray-400">{tool.tool_type}</span>
                <span className={cn("text-xs px-2 py-0.5 rounded-full flex items-center gap-1", riskColors[tool.risk_level])}>
                  <AlertTriangle className="w-3 h-3" />
                  {tool.risk_level}
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
