import { defineConfig } from "astro/config";

// https://astro.build/config
export default defineConfig({
  // Deployed as a GitHub Pages project site: <user>.github.io/browser-mini-games/
  site: "https://nikitaboyarkin.github.io",
  base: "/browser-mini-games",
  output: "static",
  trailingSlash: "ignore",
  compressHTML: true,
  build: {
    // Inline all CSS so dist/index.html is fully self-contained (works from
    // any subpath — the games site AND the portfolio public/games/ copy).
    inlineStylesheets: "always",
  },
});
