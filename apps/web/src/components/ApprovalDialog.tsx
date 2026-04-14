"use client";

import { useState } from "react";
import { Shield, AlertTriangle } from "lucide-react";
import { approveRun } from "@/lib/api";
import { useTranslations } from "next-intl";

interface ApprovalDialogProps {
  runId: string;
  stepId: string;
  action: string;
  riskLevel: "low" | "medium" | "high";
  onComplete: () => void;
  onClose: () => void;
}

const riskColors = {
  low: "text-green-400 bg-green-400/10",
  medium: "text-yellow-400 bg-yellow-400/10",
  high: "text-red-400 bg-red-400/10",
};

export function ApprovalDialog({ runId, stepId, action, riskLevel, onComplete, onClose }: ApprovalDialogProps) {
  const [reason, setReason] = useState("");
  const [loading, setLoading] = useState(false);
  const t = useTranslations("approval");
  const tc = useTranslations("common");

  async function handleDecision(approved: boolean) {
    setLoading(true);
    try {
      await approveRun(runId, stepId, approved, reason || undefined);
      onComplete();
    } catch {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
      <div className="bg-panel border border-border rounded-xl w-full max-w-md p-5 space-y-4">
        <div className="flex items-center gap-3">
          <Shield className="w-5 h-5 text-yellow-400" />
          <h3 className="text-sm font-semibold">{t("title")}</h3>
        </div>
        <p className="text-sm text-gray-300">{action}</p>
        <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${riskColors[riskLevel]}`}>
          <AlertTriangle className="w-3 h-3" />
          {t(riskLevel)}
        </div>
        <textarea
          value={reason}
          onChange={(e) => setReason(e.target.value)}
          placeholder={t("reasonPlaceholder")}
          className="w-full bg-surface border border-border rounded-lg p-2.5 text-sm text-gray-200 placeholder-gray-500 resize-none h-20 focus:outline-none focus:border-primary"
        />
        <div className="flex gap-2 justify-end">
          <button onClick={onClose} className="px-4 py-2 text-sm text-gray-400 hover:text-gray-200 transition-colors">
            {tc("cancel")}
          </button>
          <button onClick={() => handleDecision(false)} disabled={loading} className="px-4 py-2 text-sm bg-red-500/20 text-red-400 rounded-lg hover:bg-red-500/30 transition-colors disabled:opacity-50">
            {t("reject")}
          </button>
          <button onClick={() => handleDecision(true)} disabled={loading} className="px-4 py-2 text-sm bg-primary text-white rounded-lg hover:bg-primary/80 transition-colors disabled:opacity-50">
            {t("approve")}
          </button>
        </div>
      </div>
    </div>
  );
}
