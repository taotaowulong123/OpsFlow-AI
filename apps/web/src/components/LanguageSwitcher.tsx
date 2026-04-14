"use client";

import { useLocale } from "@/providers/IntlProvider";
import { useTranslations } from "next-intl";
import { Globe } from "lucide-react";
import { locales, type Locale } from "@/i18n/config";

export function LanguageSwitcher() {
  const { locale, setLocale } = useLocale();
  const t = useTranslations("languageSwitcher");

  return (
    <div className="flex items-center gap-2 px-4 py-2">
      <Globe className="w-3.5 h-3.5 text-gray-500" />
      <select
        value={locale}
        onChange={(e) => setLocale(e.target.value as Locale)}
        className="bg-transparent text-xs text-gray-400 focus:outline-none cursor-pointer"
      >
        {locales.map((l) => (
          <option key={l} value={l}>
            {t(l)}
          </option>
        ))}
      </select>
    </div>
  );
}
