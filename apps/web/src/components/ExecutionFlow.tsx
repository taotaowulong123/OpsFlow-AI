"use client";

import { Play } from "lucide-react";
import type { RunStep } from "@/types";
import { StepCard } from "./StepCard";
import { useTranslations } from "next-intl";

function TimelineConnector({ active }: { active: boolean }) {
  return (
    <div className="flex justify-center py-1">
      <div className={`w-0.5 h-6 ${active ? "bg-primary" : "bg-border"}`} />
    </div>
  );
}

export function ExecutionFlow({ steps }: { steps: RunStep[] }) {
  const t = useTranslations("taskConsole");

  if (steps.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-gray-500">
        <Play className="w-8 h-8 mb-3" />
        <p className="text-sm">{t("emptyState")}</p>
      </div>
    );
  }

  return (
    <div className="space-y-0">
      {steps.map((step, i) => (
        <div key={step.id}>
          <StepCard step={step} />
          {i < steps.length - 1 && (
            <TimelineConnector active={step.status === "completed"} />
          )}
        </div>
      ))}
    </div>
  );
}
