# Customizing Commands

If your language is not listed, or if you want to override the default command for a language, simply add it to your [config](configuration):

```toml
# using quikrun.toml
[commands]
py = "python3 {file}"   # overrides default
ext = "your-cmd {file}" # Register new .ext file

# using pyproject.toml
[tool.quikrun.commands]
py = "python3 {file}"

# using Cargo.toml
[package.metadata.quikrun.commands]
py = "python3 {file}"
```

## Placeholders

Templates use these placeholders (shell-quoted):

| Placeholder   | Value                                                                            |
| ------------- | -------------------------------------------------------------------------------- |
| `{file}`      | absolute path to the source file                                                 |
| `{file_stem}` | filename without its extension (e.g. `main`)                                     |
| `{file_dir}`  | directory path containing the source file                                        |
| `{file_name}` | name of the source file (e.g. `main.py`)                                         |
| `{out}`       | absolute path to the compiled binary (compiled langs only)                       |
| `{out_stem}`  | absolute path to the compiled binary without its extension (compiled langs only) |

## Cross platform/Shell commands

if a same command is valid across all platforms/shells, it can be defined using a flag string:

```toml
[commands]
py = "python3 {file}" # ran in any os/shell
c = { compile = "gcc -Wall -Wextra {file} -o {out}", run = "{out}" }  # ran on any os/shell
```

## Platform & Shell Specific Commands

There are different shells and OSs, You can define which command runs on which shell and OS.

- **Shell Families:** `posix` (bash, zsh, sh), `cmd` (Windows CMD), `pwsh` (PowerShell Core).
- **OS Platforms:** `linux`, `darwin`, `win`.

```toml
[commands]

# Shell-Family specific configuration
# Used if a specific shell requires unique syntax (e.g. setting environment variables differently)
foo = {
    posix = "ENV_VAR=1 foo {file}",       # runs on bash/zsh/sh...   on any OS
    pwsh =  "$env:ENV_VAR=1; foo {file}", # runs on PowerShell Core  on any OS
    cmd =   "set ENV_VAR=1& foo {file}",  # runs on Windows CMD      on any OS
}

# OS Platform specific configuration (nested inside the Shell Family)
# Used when the executable name differs across operating systems
foo = {
    posix = {
        linux = "foo-linux {file}",  # runs on bash/zsh/sh... on Linux
        darwin = "foo-mac {file}",   # runs on bash/zsh/sh... on macOS
        win = "foo-win {file}",      # runs on bash/zsh/sh... on Windows
    },
    pwsh = "foo-win {file}",   # runs on PowerShell Core  on any OS
    cmd = "foo-win {file}",    # runs on Windows CMD      on any OS
}

# Command array (smart fallback)
# quikrun will automatically pick the first command installed on your system!
js = ["bun run {file}", "deno run {file}", "node {file}"]


# Platform-Specific Split Compile & Run
# You can nest compile-run tables under operating systems (inside shell families) as well.
cpp = { posix = { linux = { compile = "g++ -Wall {file} -o {out}", run = "{out}" }, darwin = { compile = "clang++ -Wall {file} -o {out}", run = "{out}" } } }

# Command Inheritance
# Use the @ prefix to inherit a configuration from an already defined command template!
cxx = "@cpp"
jsx = "@js"

# Extending Inheritance
# Inherit commands from an runner and add more
js = ["bun run {file}", "deno run {file}", "node {file}"]
ts = ["@js", "tsc {file}"]
```
