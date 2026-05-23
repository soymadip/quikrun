<div align="center">
  <img src="https://raw.githubusercontent.com/soymadip/quikrun/main/src/img/icon.svg" height="85">
  <h1>Quikrun</h1>
  <h4>Run your code files without hassle</h4>
  <p>Quikrun is a CLI tool for running code files instantly without typing complex commands in your terminal.</p>
</div>

## Features

- **Auto language Detection:** Auto-detects language by extension or shebang headers (`#!`).
- **Sane Defaults:** Default command templates preconfigured with generally recommended compiler/interpreter flags.
- **Highly Configurable:** Add new languages or override behavior to suit your own taste
- **Argument Forwarding:** Safely forward arguments/flags to your scripts easily, with support for POSIX `--` separator.

---

## Installation

### Distro Packages

#### 1. Arch Linux (AUR)

```bash
paru -S quikrun

# or
yay -S quikrun
```

### Via PyPI

If there is not package for your distro, you can install directly:

```bash
# Using uv (highly recommended for global installation)
uv tool install quikrun

# Using pipx (another good way to install globally)
pipx install quikrun

# Using pip (if you wanna install locally in a project)
pip install quikrun
```

---

## Quick Usage

Simply pass your file to `quikrun`:

```bash
quikrun main.py   # runs with python3
quikrun hello.c   # compiles using gcc and runs the binary
```

### Forwarding Arguments

- For simple cases with no flag conflicts:

  ```bash
  quikrun script.py arg1 arg2
  ```

- Use the `--` separator to forcely forward instead of quikrun:

  ```bash
  quikrun script.py -- --verbose --threads 4
  ```

## Configuration

quikrun merges config options in a hierarchy (highest priority wins):

1. **Project:** `quikrun.toml` in your current working directory.
2. **Project:** `[tool.quikrun]` table inside `pyproject.toml`.
3. **Project:** `[package.metadata.quikrun]` table inside `Cargo.toml`.
4. **Project:** `"quikrun"` key inside `package.json`.
5. **User:** `~/.config/quikrun/config.toml` (XDG-compliant).
6. **Built-in:** Default fallbacks for common languages.

For customization, default commands, or custom commands, check out **[Documentation](https://soymadip.github.io/quikrun)**:
