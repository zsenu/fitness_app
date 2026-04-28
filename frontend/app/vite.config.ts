import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import dotenv from 'dotenv';

dotenv.config();

export default defineConfig({
    plugins: [react()],
    define: {
        'process.env': {
            DJANGO_BACKEND_URL: process.env.DJANGO_BACKEND_URL
        }
    }
});
