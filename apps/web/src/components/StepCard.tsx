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
  planning: Brain,
  retrieving: Search,
  executing: Play,
  reviewer: CheckCircle,
  approver: Shield,
};

function StatusIndicator({ status }: { status: string }) {
  switch (status) {
    case "running":
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
  const inputData = step.input_data ?? {};
  const outputData = step.output_data ?? {};
  const latencyMs = step.latency_ms ?? 0;
  const tokensUsed = step.tokens_used ?? 0;

  return (
    <div className="bg-panel border border-border rounded-lg overflow-hidden">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full flex items-center gap-3 p-3 text-left hover:bg-white/5 transition-colors"
      >
        <Icon className="w-4 h-4 text-gray-400" />
        <span className="flex-1 text-sm font-medium">{step.node_name}</span>
        <StatusIndicator status={step.status} />
        {latencyMs > 0 && (
          <span className="text-xs text-gray-500">{formatDuration(latencyMs)}</span>
        )}
        {tokensUsed > 0 && (
          <span className="text-xs text-gray-500">{formatTokens(tokensUsed)} tok</span>
        )}
        {expanded ? <ChevronDown className="w-4 h-4 text-gray-500" /> : <ChevronRight className="w-4 h-4 text-gray-500" />}
      </button>
      {expanded && (
        <div className="px-3 pb-3 space-y-2 border-t border-border pt-2">
          {step.error_message && (
            <p className="text-xs text-red-400 bg-red-400/10 p-2 rounded">{step.error_message}</p>
          )}
          {Object.keys(outputData).length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-1">{t("output")}</p>
              <pre className="text-xs text-gray-300 bg-surface p-2 rounded overflow-x-auto">
                {JSON.stringify(outputData, null, 2)}
              </pre>
            </div>
          )}
          {Object.keys(inputData).length > 0 && (
            <div>
              <p className="text-xs text-gray-500 mb-1">{t("input")}</p>
              <pre className="text-xs text-gray-300 bg-surface p-2 rounded overflow-x-auto">
                {JSON.stringify(inputData, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
