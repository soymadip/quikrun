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

## Cross Platform/Shell Commands

If a same command is valid across all platforms/shells, it can be defined using a flag string:

```toml
[commands]
py = "python3 {file}" # ran in any os/shell
c = { compile = "gcc -Wall -Wextra {file} -o {out}", run = "{out}" }  # ran on any os/shell
```

## Platform & Shell Specific Commands

There are different shells and OSs, You can define which command runs on which shell and OS.

- **Shell Families:** `posix` (bash, zsh, sh), `cmd` (Windows CMD), `pwsh` (PowerShell Core or 7+).
- **OS Platforms:** `linux`, `darwin`, `win`.

### Shell Family Specific

Used if a specific shell requires unique syntax (e.g. setting environment variables differently)

> [!WARNING]
> although for examples we use line breaks for readability, TOML requires inline tables to be defined on a single line

```toml
[commands]
foo = {
    posix = "ENV_VAR=1 foo {file}",       # runs on bash/zsh...   on any OS
    pwsh =  "$env:ENV_VAR=1; foo {file}", # runs on PowerShell 7+ on any OS
    cmd =   "set ENV_VAR=1& foo {file}",  # runs on Windows CMD   on any OS
}
```

### OS Platform Specific

Used when the executable name differs across operating systems

```toml
[commands]
foo = {
   posix = {
       linux = "foo-linux {file}",  # runs on bash/zsh... on Linux
       darwin = "foo-mac {file}",   # runs on bash/zsh... on macOS
       win = "foo-win {file}",      # runs on bash/zsh... on Windows
    },
    pwsh = "foo-win {file}",  # runs on PowerShell 7+ on any OS
    cmd = "foo-win {file}",   # runs on Windows CMD   on any OS
}
```

## Command Array

quikrun will automatically pick the first command installed on your system!

```toml
[commands]
js = ["bun run {file}", "deno run {file}", "node {file}"]
```

## Split Compile & Run

For Compiled languages, it's recommended to define compile & run commands separately, this helps measuring execution time correctly.

```toml
[commands]
go = {
  compile = "go build -o {out} {file}",
  run = "{out}",
}
```

### Shell/Platform Specific

You can nest compile-run tables under shell or operating systems (inside shell families) as well.

```toml
[commands]
cpp = {
  posix = {
    linux = { compile = "g++ -Wall {file} -o {out}", run = "{out}" },       # runs on bash/zsh... on Linux
    darwin = { compile = "clang++ -Wall {file} -o {out}", run = "{out}" },  # runs on bash/zsh... on macOS
  }
}

```

## Command Inheritance

Use the `@` prefix to inherit a configuration from an already defined command template!

```toml
[commands]
cxx = "@cpp"
jsx = "@js"
```

### Extending Inheritance

Your can also inherit commands from an template and add more

```toml
[commands]
js = ["bun run {file}", "deno run {file}", "node {file}"]
ts = ["@js", "tsc {file}"]
```
