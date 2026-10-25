# Customizing Commands

If your language is not listed, or if you want to override the default command for a language, simply add it to your [config](configuration):

```toml
# using quikrun.toml
[commands]
py = "python3 {file_path}"   # overrides default
ext = "your-cmd {file_path}" # Register new .ext file

# using pyproject.toml
[tool.quikrun.commands]
py = "python3 {file_path}"

# using Cargo.toml
[package.metadata.quikrun.commands]
py = "python3 {file_path}"
```

## Variables

Templates use these variables as placeholders.  
These will be replaced with the actual values during command execution.

| Placeholder      | Value                                                                |
| ---------------- | -------------------------------------------------------------------- |
| `{file_file}`    | Relative path to the given file (<small>quoted</small>)              |
| `{file_dir}`     | Relative path of dir containing the file (<small>uoted</small>)      |
| `{file_name}`    | name of the given file (e.g. `main.py`) (<small>quoted</small>)      |
| `{file_stem}`    | filename without its extension (e.g. `main`) (<small>quoted</small>) |
| `{file_slug}`    | file name without spaces (e.g., 'my file.py' -> 'my_file')           |
| `{file_ext}`     | Given file's extension (e.g. `py`)                                   |
| `{file_shebang}` | Shebang (if present) of given file (<small>quoted</small>)           |
| `{out_dir}`      | Path to the compiled output bin's dir (<small>shell quoted</small>)  |
| `{out_file}`     | path to out_dir/file_stem (<small>quoted</small>)                    |
| `{platform}`     | Platform name ('linux'/'darwin'/'win')                               |
| `{shell}`        | Shell name ('posix'/'cmd'/'pwsh')                                    |

## Cross Platform/Shell Commands

If a same command is valid across all platforms/shells, it can be defined using a flag string:

```toml
[commands]
py = "python3 {file_path}" # ran in any os/shell
c = { compile = "gcc -Wall -Wextra {file_path} -o {out_file}", run = "{out_file}" }  # ran on any os/shell
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
    posix = "ENV_VAR=1 foo {file_path}",       # runs on bash/zsh...   on any OS
    pwsh =  "$env:ENV_VAR=1; foo {file_path}", # runs on PowerShell 7+ on any OS
    cmd =   "set ENV_VAR=1& foo {file_path}",  # runs on Windows CMD   on any OS
}
```

### OS Platform Specific

Used when the executable name differs across operating systems

```toml
[commands]
foo = {
   posix = {
       linux = "foo-linux {file_path}",  # runs on bash/zsh... on Linux
       darwin = "foo-mac {file_path}",   # runs on bash/zsh... on macOS
       win = "foo-win {file_path}",      # runs on bash/zsh... on Windows
    },
    pwsh = "foo-win {file_path}",  # runs on PowerShell 7+ on any OS
    cmd = "foo-win {file_path}",   # runs on Windows CMD   on any OS
}
```

## Command Array

quikrun will automatically pick the first command installed on your system!

```toml
[commands]
js = ["bun run {file_path}", "deno run {file_path}", "node {file_path}"]
```

## Split Compile & Run

For Compiled languages, it's recommended to define compile & run commands separately, this helps measuring execution time correctly.

```toml
[commands]
go = {
  compile = "go build -o {out_file} {file_path}",
  run = "{out_file}",
}
```

### Shell/Platform Specific

You can nest compile-run tables under shell or operating systems (inside shell families) as well.

```toml
[commands]
cpp = {
  posix = {
    linux = { compile = "g++ -Wall {file_path} -o {out_file}", run = "{out_file}" },       # runs on bash/zsh... on Linux
    darwin = { compile = "clang++ -Wall {file_path} -o {out_file}", run = "{out_file}" },  # runs on bash/zsh... on macOS
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
js = ["bun run {file_path}", "deno run {file_path}", "node {file_path}"]
ts = ["@js", "tsc {file_path}"]
```
