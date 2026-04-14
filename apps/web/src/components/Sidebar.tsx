"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, MessageSquare, BookOpen, Wrench, History, Zap } from "lucide-react";
import { cn } from "@/lib/utils";

const links = [
  { href: "/", label: "Dashboard", icon: LayoutDashboard },
  { href: "/tasks", label: "Tasks", icon: MessageSquare },
  { href: "/knowledge", label: "Knowledge", icon: BookOpen },
  { href: "/tools", label: "Tools", icon: Wrench },
  { href: "/runs", label: "Runs", icon: History },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-60 flex-shrink-0 bg-panel border-r border-border flex flex-col">
      <div className="p-5 flex items-center gap-2">
        <Zap className="w-5 h-5 text-primary" />
        <span className="text-lg font-semibold">OpsFlow AI</span>
      </div>
      <nav className="flex-1 px-3 space-y-1">
        {links.map(({ href, label, icon: Icon }) => {
          const active = href === "/" ? pathname === "/" : pathname.startsWith(href);
          return (
            <Link
              key={href}
              href={href}
              className={cn(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors",
                active
                  ? "bg-primary/15 text-primary"
                  : "text-gray-400 hover:text-gray-200 hover:bg-white/5"
              )}
            >
              <Icon className="w-4 h-4" />
              {label}
            </Link>
          );
        })}
      </nav>
      <div className="p-4 text-xs text-gray-500">v0.1.0</div>
    </aside>
  );
}
