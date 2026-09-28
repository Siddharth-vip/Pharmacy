/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./static/**/*.{css,js}", "./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: "#173D32",       // Primary dark green
          darker: "#0E2820",     // Deep forest green
          light: "#235345",      // Forest mid-tone
          accent: "#D8C8AA",     // Warm beige/tan
          cream: "#F5EFE3",      // Warm cream background
          "cream-light": "#FBF8F1", // Soft light cream
          "cream-card": "#FAF6EE",  // Card surface
          "text-dark": "#17202A", // Dark typography
          "text-muted": "#65717D", // Muted subheadings/text
          border: "#E5DAC5",     // Subtle warm borders
          gold: "#C29B38",       // Refined gold accent
          goldHover: "#AB852B",
          surface: "#FFFFFF",
        },
      },
      fontFamily: {
        sans: ["'Inter'", "'Plus Jakarta Sans'", "system-ui", "-apple-system", "sans-serif"],
        serif: ["'Playfair Display'", "Georgia", "serif"],
        berkshire: ["'Berkshire Swash'", "cursive"],
      },
      boxShadow: {
        'wellness': '0 4px 20px -2px rgba(23, 61, 50, 0.05), 0 2px 6px -1px rgba(23, 61, 50, 0.03)',
        'wellness-md': '0 10px 25px -3px rgba(23, 61, 50, 0.08), 0 4px 10px -2px rgba(23, 61, 50, 0.04)',
        'wellness-lg': '0 20px 35px -4px rgba(23, 61, 50, 0.12), 0 8px 16px -4px rgba(23, 61, 50, 0.06)',
      }
    },
  },
  plugins: [],
};
