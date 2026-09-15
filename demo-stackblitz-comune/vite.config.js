import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@splidejs/splide/src/css/core/index":
        "node_modules/@splidejs/splide/src/css/core/index.scss",
    },
  },
});

