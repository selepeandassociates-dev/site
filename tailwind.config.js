/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./*.html', './assets/site.js'],
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#eef1f7',
          100: '#d5dcec',
          200: '#a9b6d4',
          300: '#7488b3',
          400: '#4a6094',
          500: '#2f4678',
          600: '#243a68',
          700: '#1b3263',
          800: '#13254f',
          900: '#0c1b3f',
          950: '#070f26',
        },
        gold: {
          50: '#fbf7ee',
          100: '#f4ead4',
          200: '#e8d3a5',
          300: '#d8b97a',
          400: '#c4a05e',
          500: '#b0884a',
          600: '#94703a',
          700: '#745730',
        },
        silver: {
          100: '#eef0f3',
          200: '#dde1e7',
          300: '#c3c9d2',
          400: '#a4acb8',
        },
        cream: {
          50: '#fcfaf6',
          100: '#f8f4ec',
          200: '#efe8da',
        },
      },
      fontFamily: {
        display: ['"Playfair Display"', 'Georgia', 'serif'],
        serif: ['"Cormorant Garamond"', 'Georgia', 'serif'],
        sans: ['Inter', 'system-ui', 'sans-serif'],
      },
      letterSpacing: {
        caps: '0.24em',
        wideCaps: '0.32em',
      },
      boxShadow: {
        card: '0 1px 2px rgba(12,27,63,.06), 0 8px 24px -12px rgba(12,27,63,.18)',
        lift: '0 2px 4px rgba(12,27,63,.08), 0 18px 40px -16px rgba(12,27,63,.35)',
      },
      maxWidth: {
        site: '80rem',
      },
    },
  },
  plugins: [],
};
