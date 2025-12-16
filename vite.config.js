import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  root: './frontend',
  server: {
    port: 3001,
    proxy: {
      '/medical': {
        target: 'http://localhost:3000',
        changeOrigin: true,
      }
    }
  },
  build: {
    outDir: '../dist/frontend'
  }
})
