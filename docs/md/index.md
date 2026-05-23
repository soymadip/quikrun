---
layout: home

hero:
  name: "QuikRun"
  text: "Run your code without hassle"
  tagline: "A CLI tool for running code files instantly without typing complex commands in your terminal."
  image:
    src: /icon.svg
    alt: Quikrun Logo

  actions:
    - theme: brand
      text: "Get Started"
      link: /install

    - theme: alt
      text: "Usage"
      link: /usage

features:
  - icon: "🔍"
    title: "Auto Language Detection"
    details: "Instantly detects the language using file extensions or shebang headers."

  - icon: "⚡"
    title: "Sane Defaults"
    details: "Built-in command templates pre-configured with generally recommended compiler or interpreter flags."

  - icon: "🛠️"
    title: "Highly Configurable"
    details: "Add new languages or override behavior via quikrun.toml, pyproject.toml, Cargo.toml, or package.json."

  - icon: "➡️"
    title: "Clean Argument Forwarding"
    details: "Safely forwards all arguments and flags to your scripts using the standard POSIX -- separator."
---
