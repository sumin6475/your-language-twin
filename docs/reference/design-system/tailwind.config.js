/**
 * Tailwind config — Your Ideal Role Model
 * Derived from tokens.json (the source of truth). If you change a value,
 * change it in tokens.json first, then mirror it here.
 *
 * Fonts to load in index.html <head>:
 *   Clash Display  → https://api.fontshare.com/v2/css?f[]=clash-display@500,600&display=swap
 *   Inter          → https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap
 */
module.exports = {
  theme: {
    extend: {
      colors: {
        bg:        { DEFAULT: "#FFFFFF", subtle: "#FAFAFB" },
        ink:       { DEFAULT: "#18181B", secondary: "#52525B", tertiary: "#71717A" },
        blue:      { deep: "#1E40AF", bright: "#3B82F6", tint: "#EFF3FF" },
        border:    { DEFAULT: "#ECECF0" }
      },
      fontFamily: {
        display: ["Clash Display", "sans-serif"],
        body:    ["Inter", "sans-serif"]
      },
      fontSize: {
        h1:    ["34px", { lineHeight: "1.1", letterSpacing: "-0.015em" }],
        h2:    ["24px", { lineHeight: "1.15" }],
        h3:    ["18px", { lineHeight: "1.3" }],
        body:  ["15px", { lineHeight: "1.6" }],
        small: ["13px", { lineHeight: "1.5" }],
        label: ["12px", { lineHeight: "1.4", letterSpacing: "0.1em" }]
      },
      spacing: {
        1: "4px", 2: "8px", 3: "12px", 4: "16px", 6: "24px", 8: "32px", 12: "48px"
      },
      borderRadius: {
        sm: "8px", md: "12px", lg: "16px", xl: "24px"
      },
      boxShadow: {
        card:   "0 4px 14px rgba(0,0,0,0.04)",
        raised: "0 12px 32px rgba(0,0,0,0.10)",
        device: "0 20px 48px rgba(0,0,0,0.14)"
      }
    }
  }
};
