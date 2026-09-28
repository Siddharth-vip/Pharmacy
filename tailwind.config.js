/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./static/**/*.{css,js}", "./templates/**/*.html"],
  theme: {
    extend: {
      colors: {
        brand: {
          dark: "#123F35",       // Deep forest green
          darker: "#0D332B",     // Darker green
          light: "#1B5448",      // Mid forest green
          accent: "#C9B27C",     // Muted gold
          "accent-soft": "#E5D5B8", // Soft beige
          health: "#1A8F6B",     // Healthcare green
          cream: "#F7F2E8",      // Warm cream
          "cream-light": "#FCFAF5", // Soft ivory
          "cream-card": "#FAF7F0",  // Card surface
          "text-dark": "#123F35", // Deep teal typography
          "text-slate": "#64748B", // Secondary slate
          "text-muted": "#7C8794", // Muted subheadings/text
          border: "#E5D5B8",     // Soft beige/cream borders
          "border-light": "#EFE6D5", // Subtle inner borders
          gold: "#C9B27C",       // Refined gold accent
          goldHover: "#B89F66",
          success: "#138A5B",    // Healthcare success green
          surface: "#FFFFFF",
        },
      },
      fontFamily: {
        sans: ["'Inter'", "'Plus Jakarta Sans'", "system-ui", "-apple-system", "sans-serif"],
        serif: ["'Playfair Display'", "Georgia", "serif"],
        berkshire: ["'Berkshire Swash'", "cursive"],
      },
      boxShadow: {
        'wellness': '0 4px 20px -2px rgba(18, 63, 53, 0.05), 0 2px 6px -1px rgba(18, 63, 53, 0.03)',
        'wellness-md': '0 10px 25px -3px rgba(18, 63, 53, 0.08), 0 4px 10px -2px rgba(18, 63, 53, 0.04)',
        'wellness-lg': '0 20px 35px -4px rgba(18, 63, 53, 0.12), 0 8px 16px -4px rgba(18, 63, 53, 0.06)',
      },
      animation: {
        'float-slow': 'float 6s ease-in-out infinite',
        'float-delayed': 'float 7s ease-in-out 2s infinite',
        'float-reverse': 'float-reverse 8s ease-in-out 1s infinite',
        'pulse-subtle': 'pulse-subtle 4s ease-in-out infinite',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(-12px) rotate(2deg)' },
        },
        'float-reverse': {
          '0%, 100%': { transform: 'translateY(0px) rotate(0deg)' },
          '50%': { transform: 'translateY(10px) rotate(-2deg)' },
        },
        'pulse-subtle': {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.88', transform: 'scale(1.02)' },
        },
      }
    },
  },
  plugins: [],
};
