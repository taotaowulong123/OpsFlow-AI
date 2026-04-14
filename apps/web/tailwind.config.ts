import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#6366f1",
        surface: "#f9fafb",
        panel: "#ffffff",
        border: "#e5e7eb",
      },
    },
  },
  plugins: [],
};

export default config;
