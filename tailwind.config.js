/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./frontend/**/*.{js,ts,jsx,tsx,html}",
  ],
  theme: {
    extend: {
      colors: {
        medical: {
          blue: '#1a5490',
          lightblue: '#e8f0f8',
          gray: '#4a5568',
        }
      }
    },
  },
  plugins: [],
}
