"use client";

import { useState, useRef } from "react";
import { Send, Loader2 } from "lucide-react";
import type { RunStep } from "@/types";
import { createTask, runTask } from "@/lib/api";
import { ExecutionFlow } from "./ExecutionFlow";

export function TaskConsole() {
  const [input, setInput] = useState("");
  const [steps, setSteps] = useState<RunStep[]>([]);
  const [running, setRunning] = useState(false);
  const esRef = useRef<EventSource | null>(null);

  async function handleRun() {
    if (!input.trim() || running) return;
    setRunning(true);
    setSteps([]);

    try {
      const task = await createTask(input, input);
      const es = runTask(task.id);
      esRef.current = es;

      es.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          if (data.step) {
            setSteps((prev) => {
              const idx = prev.findIndex((s) => s.id === data.step.id);
              if (idx >= 0) {
                const updated = [...prev];
                updated[idx] = data.step;
                return updated;
              }
              return [...prev, data.step];
            });
          }
          if (data.event_type === "complete" || data.event_type === "error") {
            es.close();
            setRunning(false);
          }
        } catch {}
      };

      es.onerror = () => {
        es.close();
        setRunning(false);
      };
    } catch {
      setRunning(false);
    }
  }

  return (
    <div className="flex flex-col h-full">
      <div className="flex gap-2 mb-4">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleRun()}
          placeholder="Describe a task to execute..."
          className="flex-1 bg-surface border border-border rounded-lg px-4 py-2.5 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-primary transition-colors"
        />
        <button
          onClick={handleRun}
          disabled={running || !input.trim()}
          className="px-5 py-2.5 bg-primary text-white text-sm font-medium rounded-lg hover:bg-primary/80 transition-colors disabled:opacity-50 flex items-center gap-2"
        >
          {running ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
          Run
        </button>
      </div>
      <div className="flex-1 overflow-y-auto">
        <ExecutionFlow steps={steps} />
      </div>
    </div>
  );
}
