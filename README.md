<div align="center">
  <img src="https://raw.githubusercontent.com/soymadip/quikrun/main/src/img/icon.svg" height="85">
  <h1>Quikrun</h1>
  <h4>Run your code files without hassle</h4>
  <p>Quikrun is a CLI tool designed to run code files instantly without typing complex compilation or runner commands in the terminal.</p>
</div>

---

## Features

- **Shebang Detection:** Auto-detects shebang headers (`#!`) and runs scripts directly using the system interpreter.
- **Clean Argument Forwarding:** Fully supports the standard POSIX `--` separator to cleanly route command-line arguments to target script.

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

```bash
# Using uv (highly recommended)
uv tool install quikrun

# Using pipx
pipx install quikrun

# Using pip (not recommended for global installation)
pip install quikrun
```

---

## Quick Start & Usage

Simply pass your file to `quikrun`:

```bash
quikrun main.py                   # runs with python3
quikrun hello.c                   # compiles using gcc and runs the binary
```

### Forwarding Arguments

Everything after the `--` separator is forwarded directly to your script:

```bash
quikrun script.py -- --verbose --threads 4
```

## Configuration

quikrun merges config options in a hierarchy (highest priority wins):

1. **Project:** `quikrun.toml` in your current working directory.
2. **Project:** `[tool.quikrun.runners]` table inside `pyproject.toml`.
3. **User:** `~/.config/quikrun/config.toml` (XDG-compliant).
4. **Built-in:** Default fallbacks for common languages.

### Customizing Runners

Add a customized command configuration inside `~/.config/quikrun/config.toml`:

```toml
[runners]
# Use PyPy as the default runner for Python files
py = "pypy {file}"

# Register a completely new language extension
zig = "zig run {file}"
```

Or Using `pyproject.toml`:

```toml
[tool.quikrun.runners]
# Use PyPy as the default runner for Python files
py = "pypy {file}"

# Register a completely new language extension
zig = "zig run {file}"
```

---

## Documentation

For deep-dive usage, details about built-in compilers, or configuration, check out **[Wiki Pages](https://github.com/soymadip/quikrun/wiki)**:
