import { defineConfig } from "vite";
import uni from "@dcloudio/vite-plugin-uni";
const target = "https://crm.shoxfashion.com/api/cms-dashboard/";
// https://vitejs.dev/config/
export default defineConfig({
  plugins: [uni()],
  server: {
    // 确保热重载功能是启用的
    hmr: true, // 这是默认值，通常可以省略
    host: "0.0.0.0",
    proxy: {
      "/api/cms-dashboard": {
        target,
        rewrite: (path) => {
          console.log(path);
          return path.replace("/api/cms-dashboard", "/");
        },
        changeOrigin: true,
        secure: false,
        xfwd: false,
      },
    },
  },
});
