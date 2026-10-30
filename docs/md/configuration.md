# Configuration

Quikrun supports two levels of configuration, merged in this priority order (highest wins).  
A key defined at a higher-priority level overrides the same key at lower levels.

| Priority        | File                                                                              | Scope   |
| --------------- | --------------------------------------------------------------------------------- | ------- |
| **1 (highest)** | `quikrun.toml` in project directory                                               | Project |
| **2**           | `[tool.quikrun]` in `pyproject.toml`                                              | Project |
| **3**           | `[package.metadata.quikrun]` in `Cargo.toml`                                      | Project |
| **4**           | `"quikrun"` key in `package.json`                                                 | Project |
| **5**           | `$XDG_CONFIG_HOME/quikrun/config.toml` (default: `~/.config/quikrun/config.toml`) | User    |
| **6 (lowest)**  | Built-in defaults                                                                 | Global  |

Flow:

```json5
built-in: { py: "python3 {file}", js: "node {file}", rs: (...) }
user:     { py: "pypy {file}",    nim: "nim compile --run {file}" }
project:  { py: "python3 -O {file}" }

result: { py: "python3 -O {file}",          ← project wins
          js: "node {file}",                ← inherited from built-in
          rs: (...),                        ← inherited from built-in
          nim: "nim compile --run {file}" } ← from user
```

<details><summary><big>Examples</big></summary>

## User Config

**Location:** `~/.config/quikrun/config.toml` (or `$XDG_CONFIG_HOME/quikrun/config.toml` if `XDG_CONFIG_HOME` is set)

Use this to set personal preferences that apply across all your projects.

```toml
clear_terminal = true
...

[commands]
# Always run Python files with pypy instead of python3
py = "pypy {file}"
...
```

## Project Config

You can configure `quikrun` at the project level using one of the following files:

#### `quikrun.toml`

Place a `quikrun.toml` in your project root:

```toml
clear_terminal = true
...

[commands]
py = "python3 -O {file}"
..
```

#### `pyproject.toml`

Add a `[tool.quikrun]` section to your `pyproject.toml`:

```toml

[tool.quikrun]
clear_terminal = true
...

[tool.quikrun.commands]
py = "python3 -O {file}"
```

#### `Cargo.toml`

Add a `[package.metadata.quikrun.commands]` section to your `Cargo.toml`:

```toml
[package.metadata.quikrun]
clear_terminal = true

[package.metadata.quikrun.commands]
rs = "cargo run --bin {file_stem}"
```

#### `package.json`

Add a `"quikrun"` key containing a `"commands"` block to your `package.json`:

```json
{
  "quikrun": {
    "clear_terminal": true,
    "commands": {
      "js": "node --harmony {file}"
    }
  }
}
```

</details>

<br>

## Configuration Reference

The following root-level settings are supported in all configuration files:

<!-- DYNAMIC_CONFIG_REF_START -->
<!-- DYNAMIC_CONFIG_REF_END -->

## Supported Shells

Only certain shells are supported:

- **POSIX**: `sh`, `bash`, `zsh`, `dash`, `ash`
- **Windows**: `cmd.exe`, `pwsh (powershell core)`

If anything other than these are given, quikrun will use default shell as per the platform:

- `sh` on linux/macos
- `%COMSPEC%` on windows, which is usually cmd.exe

The value of `shell` must be one of the supported shell names above. If not set, quikrun uses the platform default.

```toml
# Use PowerShell for all platforms
shell = "pwsh"
```
