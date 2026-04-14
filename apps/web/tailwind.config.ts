import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        primary: "#6366f1",
        surface: "#1e1e2e",
        panel: "#252536",
        border: "#2e2e42",
      },
    },
  },
  plugins: [],
};

export default config;
