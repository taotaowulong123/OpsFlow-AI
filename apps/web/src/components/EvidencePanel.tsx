"use client";

import { useState } from "react";
import { FileText, Wrench, ScrollText } from "lucide-react";
import type { RunStep, SearchResult } from "@/types";
import { cn } from "@/lib/utils";

type Tab = "evidence" | "tools" | "logs";

interface EvidencePanelProps {
  steps: RunStep[];
  evidence?: SearchResult[];
}

export function EvidencePanel({ steps, evidence = [] }: EvidencePanelProps) {
  const [tab, setTab] = useState<Tab>("evidence");

  const tabs: { key: Tab; label: string; icon: React.ElementType }[] = [
    { key: "evidence", label: "Evidence", icon: FileText },
    { key: "tools", label: "Tools", icon: Wrench },
    { key: "logs", label: "Logs", icon: ScrollText },
  ];

  return (
    <div className="bg-panel border border-border rounded-lg flex flex-col h-full">
      <div className="flex border-b border-border">
        {tabs.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            onClick={() => setTab(key)}
            className={cn(
              "flex items-center gap-2 px-4 py-2.5 text-xs font-medium transition-colors",
              tab === key ? "text-primary border-b-2 border-primary" : "text-gray-500 hover:text-gray-300"
            )}
          >
            <Icon className="w-3.5 h-3.5" />
            {label}
          </button>
        ))}
      </div>
      <div className="flex-1 overflow-y-auto p-3 space-y-2">
        {tab === "evidence" && (
          evidence.length > 0 ? (
            evidence.map((e, i) => (
              <div key={i} className="bg-surface p-3 rounded-lg border border-border">
                <div className="flex justify-between mb-1">
                  <span className="text-xs font-medium text-gray-300">{e.document_name}</span>
                  <span className="text-xs text-gray-500">Score: {e.score.toFixed(2)}</span>
                </div>
                <p className="text-xs text-gray-400 leading-relaxed">{e.content}</p>
              </div>
            ))
          ) : (
            <p className="text-xs text-gray-500 text-center py-8">No evidence retrieved yet</p>
          )
        )}
        {tab === "tools" && (
          steps.filter(s => s.node_name === "Executor").length > 0 ? (
            steps.filter(s => s.node_name === "Executor").map((s, i) => (
              <div key={i} className="bg-surface p-3 rounded-lg border border-border">
                <p className="text-xs font-medium text-gray-300 mb-1">Tool Invocation</p>
                <pre className="text-xs text-gray-400 overflow-x-auto">
                  {JSON.stringify(s.output_data, null, 2)}
                </pre>
              </div>
            ))
          ) : (
            <p className="text-xs text-gray-500 text-center py-8">No tool invocations yet</p>
          )
        )}
        {tab === "logs" && (
          steps.length > 0 ? (
            steps.map((s, i) => (
              <div key={i} className="text-xs font-mono text-gray-400 py-1 border-b border-border/50">
                <span className="text-gray-500">[{s.node_name}]</span>{" "}
                <span className={s.status === "failed" ? "text-red-400" : "text-gray-300"}>
                  {s.status}
                </span>
                {s.error_message && <span className="text-red-400"> - {s.error_message}</span>}
              </div>
            ))
          ) : (
            <p className="text-xs text-gray-500 text-center py-8">No logs yet</p>
          )
        )}
      </div>
    </div>
  );
}
