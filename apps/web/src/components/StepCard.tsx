"use client";

import { useState } from "react";
import { Brain, Search, Play, CheckCircle, Shield, ChevronDown, ChevronRight, Loader2, XCircle, Pause } from "lucide-react";
import type { RunStep } from "@/types";
import { cn, formatDuration, formatTokens } from "@/lib/utils";
import { useTranslations } from "next-intl";

const nodeIcons: Record<string, React.ElementType> = {
  Planner: Brain,
  Retriever: Search,
  Executor: Play,
  Reviewer: CheckCircle,
  Approver: Shield,
};

function StatusIndicator({ status }: { status: string }) {
  switch (status) {
    case "in_progress":
      return <Loader2 className="w-4 h-4 text-blue-400 animate-spin" />;
    case "completed":
      return <CheckCircle className="w-4 h-4 text-green-400" />;
    case "failed":
      return <XCircle className="w-4 h-4 text-red-400" />;
    case "waiting_approval":
      return <Pause className="w-4 h-4 text-yellow-400" />;
    default:
      return <div className="w-3 h-3 rounded-full bg-gray-500" />;
  }
}

export function StepCard({ step }: { step: RunStep }) {
  const [expanded, setExpanded] = useState(false);
  const Icon = nodeIcons[step.node_name] || Play;
  const t = useTranslations("evidence");

  return (
    <div className="bg-panel border border-border rounded-lg overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 p-3 text-left hover:bg-white/5 transition-colors"
      >
        <Icon className="w-4 h-4 text-gray-400" />
        <span className="flex-1 text-sm font-medium">{step.node_name}</span>
        <StatusIndicator status={step.status} />
        {step.latency_ms > 0 && (
          <span className="text-xs text-gray-500">{formatDuration(step.latency_ms)}</span>
        )}
        {step.tokens_used > 0 && (
          <span className="text-xs text-gray-500">{formatTokens(step.tokens_used)} tok</span>
        )}
        {expanded ? <ChevronDown className="w-4 h-4 text-gray-500" /> : <ChevronRight className="w-4 h-4 text-gray-500" />}
      </button>
      {expanded && (
        <div className="px-3 pb-3 space-y-2 border-t border-border pt-2">
          {step.error_message && (
            <p className="text-xs text-red-400 bg-red-400/10 p-2 rounded">{step.error_message}</p>
          )}
          {Object.keys(step.output_data).length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-1">{t("output")}</p>
              <pre className="text-xs text-gray-300 bg-surface p-2 rounded overflow-x-auto">
                {JSON.stringify(step.output_data, null, 2)}
              </pre>
            </div>
          )}
          {Object.keys(step.input_data).length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-1">{t("input")}</p>
              <pre className="text-xs text-gray-300 bg-surface p-2 rounded overflow-x-auto">
                {JSON.stringify(step.input_data, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
