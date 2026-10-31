# Configuration

Quikrun supports several levels of configuration, merged in this priority order (highest to lowest).  
A key defined at a higher-priority level overrides the same key at lower levels.

| Priority        | File                                         | Scope   |
| --------------- | -------------------------------------------- | ------- |
| **1 (highest)** | `quikrun.toml` in project directory          | Project |
| **2**           | `pyproject.toml` -> `[tool.quikrun]`         | Project |
| **3**           | `Cargo.toml` -> `[package.metadata.quikrun]` | Project |
| **4**           | `package.json` -> `"quikrun"` key            | Project |
| **5**           | `$XDG_CONFIG_HOME/quikrun/config.toml`       | User    |
| **6**           | `/etc/quikrun/config.toml`                   | System  |
| **7 (lowest)**  | [Built-in defaults](/default-cmds)          | Global  |

Flow:

```json5
built-in: { py: "python3 {file}", js: "node {file}", rs: (...) }
user:     { py: "pypy {file}",    nim: "nim compile --run {file}" }
project:  { py: "python3 -O {file}" }

result:
        { py: "python3 -O {file}",          ← project wins
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

| Setting                    | Type                                        | Default       | Description                                                                                   |
| :------------------------- | :------------------------------------------ | :------------ | :-------------------------------------------------------------------------------------------- |
| **`shell`**                | `"auto"` / `"posix"` / `"cmd"` / `"pwsh"`   | `"auto"`      | Which shell to use.                                                                           |
| **`platform`**             | `"auto"` / `"linux"` / `"win"` / `"darwin"` | `"auto"`      | Target platform or OS override for execution.                                                 |
| **`clear_terminal`**       | `bool` / `"scroll_up"`                      | `"scroll_up"` | Whether to clear the terminal or scroll up before running.                                    |
| **`show_time_took`**       | `bool`                                      | `True`        | Whether to display the execution duration at footer                                           |
| **`show_command`**         | `bool`                                      | `True`        | Whether to display the command in footer.                                                     |
| **`show_divider`**         | `bool`                                      | `True`        | Whether to print the separation line before the footer                                        |
| **`cache_dir`**            | `string` / `str`                            | `".quikrun"`  | Custom directory used for cache and compiled build artifacts.                                 |
| **`cd_to_file_dir`**       | `bool`                                      | `False`       | Whether to change the working directory to the target file's folder before running/compiling. |
| **`keep_build_artifacts`** | `bool`                                      | `True`        | Whether to retain temporary or compiled binaries after execution completes.                   |
| **`auto_exit`**            | `"always"` / `"never"` / `"on_success"`     | `"never"`     | Controls automatic process exit behavior.                                                     |

<!-- DYNAMIC_CONFIG_REF_END -->
