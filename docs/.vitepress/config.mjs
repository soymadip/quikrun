import { withMermaid } from "vitepress-plugin-mermaid";
import taskLists from "markdown-it-task-lists";
import { resolve } from "path";
import { resolveVars } from "./plugins/resolveVars.js";
import { autoRedirects } from "./plugins/autoRedirects.js";
import { searchLinks } from "./plugins/searchLinks.js";
import { nav, baseSidebar } from "./navigation.mjs";

const metadata = {
  project: {
    title: "QuikRun",
    desc: "Run your code without hassle",
    tagLine:
      "A CLI tool for running code files instantly without typing complex commands in your terminal.",
    repo: "https://github.com/soymadip/quikrun",
  },
  pkg: {
    name: "quikrun",
    bin: "quikrun",
  },
  versions: {
    quikrun: "2.0.2",
  },
};

const base = process.env.GITHUB_REPOSITORY
  ? `/${process.env.GITHUB_REPOSITORY.split("/")[1]}/`
  : "/";

export default withMermaid({
  base: base,

  vite: {
    publicDir: resolve(process.cwd(), "public"),
    plugins: [autoRedirects({ srcDir: "md", base: base })],

    build: {
      chunkSizeWarningLimit: 1000,
      rollupOptions: {
        onwarn(warning, warn) {
          if (warning.message.includes("Rollup cannot interpret")) return;
          warn(warning);
        },
      },
    },
  },

  markdown: {
    config: (md) => {
      md.use((mdInstance) => resolveVars(mdInstance, metadata));
      md.use((mdInstance) => searchLinks(mdInstance));
      md.use(taskLists);
    },
  },

  srcDir: "md",
  cleanUrls: true,

  head: [
    ["link", { rel: "icon", type: "image/svg+xml", href: `${base}icon.svg` }],
  ],

  title: metadata.project.title,
  description: metadata.project.desc,

  transformPageData(pageData) {
    resolveVars(pageData, metadata);
  },

  themeConfig: {
    logo: `${base}icon.svg`,
    outline: [2, 3],
    metadata: metadata,

    banner: {
      enabled: false,
      text: "⚠️ QuikRun is Work In Progress!",
    },

    search: {
      provider: "local",
      options: {
        detailedView: true,
        miniSearch: {},
      },
    },

    nav: nav,
    sidebar: baseSidebar,

    socialLinks: [{ icon: "github", link: metadata.project.repo }],
  },
});
