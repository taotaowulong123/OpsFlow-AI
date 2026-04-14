import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";
import { IntlProvider } from "@/providers/IntlProvider";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "OpsFlow AI",
  description: "AI Task Execution Workspace",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="zh">
      <body className={inter.className}>
        <IntlProvider>
          <div className="flex h-screen overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-y-auto p-6">{children}</main>
          </div>
        </IntlProvider>
      </body>
    </html>
  );
}
