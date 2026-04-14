"use client";

import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { NextIntlClientProvider } from "next-intl";
import { defaultLocale, type Locale, locales } from "@/i18n/config";

type IntlContextType = {
  locale: Locale;
  setLocale: (locale: Locale) => void;
};

const IntlContext = createContext<IntlContextType>({
  locale: defaultLocale,
  setLocale: () => {},
});

export function useLocale() {
  return useContext(IntlContext);
}

function getStoredLocale(): Locale {
  if (typeof window === "undefined") return defaultLocale;
  const stored = localStorage.getItem("locale") as Locale | null;
  if (stored && locales.includes(stored)) return stored;
  return defaultLocale;
}

export function IntlProvider({ children }: { children: React.ReactNode }) {
  const [locale, setLocaleState] = useState<Locale>(defaultLocale);
  const [messages, setMessages] = useState<Record<string, any> | null>(null);

  useEffect(() => {
    const stored = getStoredLocale();
    setLocaleState(stored);
    import(`../messages/${stored}.json`).then((m) => setMessages(m.default));
  }, []);

  const setLocale = useCallback((newLocale: Locale) => {
    localStorage.setItem("locale", newLocale);
    setLocaleState(newLocale);
    import(`../messages/${newLocale}.json`).then((m) => setMessages(m.default));
  }, []);

  if (!messages) return null;

  return (
    <IntlContext.Provider value={{ locale, setLocale }}>
      <NextIntlClientProvider locale={locale} messages={messages}>
        {children}
      </NextIntlClientProvider>
    </IntlContext.Provider>
  );
}
