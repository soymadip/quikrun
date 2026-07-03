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

| Setting              | Type      | Default   | Description                                                                                                                                                                                                                     |
| :------------------- | :-------- | :-------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **`clear_terminal`** | bool      | `true`    | Clears the terminal before executing the code file.                                                                                                                                                                             |
| **`auto_close`**     | str/num   | `"never"` | - `"always"` closes immediately after execution<br/>- `"never"` waits for Enter keypress<br/>- `"on_success"` closes only when exit code is 0<br/>- Any non-negative number (e.g. `2.5`) to auto-close after that many seconds. |
| **`show_time_took`** | bool      | `true`    | Shows the execution duration of the command after it exits.                                                                                                                                                                     |
| **`show_command`**   | bool      | `true`    | Shows the command being executed.                                                                                                                                                                                               |
| **`show_shell`**     | bool      | `true`    | Shows the shell command/path.                                                                                                                                                                                                   |
| **`show_divider`**   | bool      | `true`    | Draws a horizontal execution divider line before the footer.                                                                                                                                                                    |
| **`temp_dir`**       | str       | `null`    | Absolute/Relative path to a custom directory where binaries are compiled. Supports env vars (like `$HOME`) & tilde (`~`) expansions.                                                                                            |
| **`cd_to_file_dir`** | bool      | `false`   | Changes the working directory (`cwd`) to the directory containing the source file before running.                                                                                                                               |
| **`keep_artifacts`** | bool      | `false`   | - `true`, keeps the compiled binaries and output directories after execution. <br/>- `false`, these are automatically cleaned up.                                                                                               |
| **`shell`**          | str/table | `null`    | Allows overriding the shell used to run the commands. More info below                                                                                                                                                           |

## Supported Shells

Only certain shells are supported:

- **POSIX**: `sh`, `bash`, `zsh`, `dash`, `ash`
- **Windows**: `cmd.exe`, `pwsh (powershell core)`

If anything other than these are given, quikrun will use default shell as per the platform:

- `sh` on linux/macos
- `%COMSPEC%` on windows, which is usually cmd.exe

The value of the config key can be a string (e.g. `"pwsh"`) or a table specifying different shells for different platforms (`linux`, `darwin`, `win`).  
If not set, uses default.

```toml
# Custom shell configuration example
shell = { linux = "/usr/bin/zsh", win = "pwsh.exe" }  # will use default `sh` in macos

# Or simply a string, will use pwsh for all platforms
shell = "pwsh"
```
