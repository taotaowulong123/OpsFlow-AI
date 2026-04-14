"use client";

import { useState } from "react";
import { Upload, Search, Trash2, FileText } from "lucide-react";
import type { Document, SearchResult } from "@/types";
import { cn, formatDate } from "@/lib/utils";
import { useTranslations } from "next-intl";

const mockDocs: Document[] = [
  { id: "1", filename: "api-reference.pdf", file_type: "pdf", file_size: 245000, status: "indexed", created_at: "2026-04-14T10:00:00Z" },
  { id: "2", filename: "runbook.md", file_type: "md", file_size: 12400, status: "indexed", created_at: "2026-04-13T15:00:00Z" },
  { id: "3", filename: "architecture.docx", file_type: "docx", file_size: 89000, status: "processing", created_at: "2026-04-15T08:00:00Z" },
];

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

export default function KnowledgePage() {
  const [docs] = useState<Document[]>(mockDocs);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults] = useState<SearchResult[]>([]);
  const [dragOver, setDragOver] = useState(false);
  const t = useTranslations("knowledge");

  function handleDrop(e: React.DragEvent) {
    e.preventDefault();
    setDragOver(false);
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      <div>
        <h1 className="text-xl font-semibold mb-1">{t("title")}</h1>
        <p className="text-sm text-gray-500">{t("subtitle")}</p>
      </div>
      <div
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={cn("border-2 border-dashed rounded-lg p-8 text-center transition-colors", dragOver ? "border-primary bg-primary/5" : "border-border")}
      >
        <Upload className="w-8 h-8 text-gray-500 mx-auto mb-3" />
        <p className="text-sm text-gray-400 mb-1">{t("dragDrop")}</p>
        <p className="text-xs text-gray-500">{t("fileTypes")}</p>
      </div>
      <div className="bg-panel border border-border rounded-lg overflow-hidden">
        <div className="px-4 py-3 border-b border-border">
          <h2 className="text-sm font-medium">{t("documents")}</h2>
        </div>
        <table className="w-full">
          <thead>
            <tr className="text-xs text-gray-500 border-b border-border">
              <th className="text-left px-4 py-2 font-medium">{t("filename")}</th>
              <th className="text-left px-4 py-2 font-medium">{t("type")}</th>
              <th className="text-left px-4 py-2 font-medium">{t("size")}</th>
              <th className="text-left px-4 py-2 font-medium">{t("status")}</th>
              <th className="text-left px-4 py-2 font-medium">{t("date")}</th>
              <th className="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody className="divide-y divide-border">
            {docs.map((doc) => (
              <tr key={doc.id} className="hover:bg-white/5 transition-colors">
                <td className="px-4 py-2.5 text-sm flex items-center gap-2">
                  <FileText className="w-4 h-4 text-gray-500" />
                  {doc.filename}
                </td>
                <td className="px-4 py-2.5 text-xs text-gray-400 uppercase">{doc.file_type}</td>
                <td className="px-4 py-2.5 text-xs text-gray-400">{formatSize(doc.file_size)}</td>
                <td className="px-4 py-2.5">
                  <span className={cn("text-xs px-2 py-0.5 rounded-full", doc.status === "indexed" ? "bg-green-400/10 text-green-400" : "bg-yellow-400/10 text-yellow-400")}>{doc.status}</span>
                </td>
                <td className="px-4 py-2.5 text-xs text-gray-500">{formatDate(doc.created_at)}</td>
                <td className="px-4 py-2.5">
                  <button className="p-1 hover:bg-red-500/10 rounded transition-colors">
                    <Trash2 className="w-3.5 h-3.5 text-gray-500 hover:text-red-400" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="bg-panel border border-border rounded-lg p-4 space-y-3">
        <h2 className="text-sm font-medium">{t("searchKnowledge")}</h2>
        <div className="flex gap-2">
          <input value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)} placeholder={t("searchPlaceholder")} className="flex-1 bg-surface border border-border rounded-lg px-4 py-2 text-sm text-gray-200 placeholder-gray-500 focus:outline-none focus:border-primary" />
          <button className="px-4 py-2 bg-primary text-white text-sm rounded-lg hover:bg-primary/80 transition-colors flex items-center gap-2">
            <Search className="w-4 h-4" />
            {t("search")}
          </button>
        </div>
        {searchResults.length > 0 ? (
          <div className="space-y-2">
            {searchResults.map((r, i) => (
              <div key={i} className="bg-surface p-3 rounded-lg border border-border">
                <div className="flex justify-between mb-1">
                  <span className="text-xs font-medium text-gray-300">{r.document_name}</span>
                  <span className="text-xs text-gray-500">Score: {r.score.toFixed(2)}</span>
                </div>
                <p className="text-xs text-gray-400">{r.content}</p>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-xs text-gray-500 text-center py-4">{t("searchPrompt")}</p>
        )}
      </div>
    </div>
  );
}
