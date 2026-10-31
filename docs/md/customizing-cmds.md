# Customizing Commands

To override a default command or register a new command for an extension, add it to your [config](configuration):

```toml
# using quikrun.toml
[commands]
py = "python3 {file_path}"   # overrides default
zig = "zig run {file_path}"  # adds support for .zig files

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

<!-- DYNAMIC_VARIABLES_START -->

| Placeholder      | Value                                                      |
| :--------------- | :--------------------------------------------------------- |
| `{platform}`     | Platform name (e.g., 'linux', 'win', 'darwin')             |
| `{shell}`        | Shell name (e.g., 'posix', 'cmd', 'pwsh')                  |
| `{file_path}`    | Quoted path to the source file as given                    |
| `{file_dir}`     | Quoted absolute path to the source file's directory        |
| `{file_name}`    | Quoted filename with extension (e.g., 'main.py')           |
| `{file_stem}`    | Quoted filename without extension (e.g., 'main')           |
| `{file_slug}`    | File name without spaces (e.g., 'my file.py' -> 'my_file') |
| `{file_ext}`     | File extension (e.g., '.py')                               |
| `{file_shebang}` | Shebang's command (e.g., '/usr/bin/env python3')           |
| `{out_dir}`      | Quoted path to the compiled output bin's dir               |
| `{out_file}`     | Quoted path of out_dir/file_stem                           |
| `{run_args}`     | Arguments to pass to file/bin                              |

<!-- DYNAMIC_VARIABLES_END -->

## Universal Commands

If a same command is valid across all platforms/shells, it can be defined using a flat string:

```toml
[commands]
py = "python3 {file_path}" # ran in any os/shell
```

### Split Compile & Run Commands

For Compiled languages, it's recommended to define compile & run commands separately, this helps measuring execution time correctly.

```toml
[commands]
go = {
  compile = "go build -o {out_file} {file_path}",
  run = "{out_file}",
}
```

## Shell Specific Commands

If a commands is cross platfrorm/os but requires different syntax for different shells,  
it can be defined using a table:

> [!WARNING]
> although for examples we use line breaks for readability, TOML requires inline tables to be defined on a single line

```toml
[commands]
foo = {
    posix = "ENV_VAR=1 foo {file_path}",       # runs on bash/zsh...   on any OS
    cmd =   "set ENV_VAR=1& foo {file_path}",  # runs on Windows CMD   on any OS
    pwsh =  "$env:ENV_VAR=1; foo {file_path}", # runs on PowerShell 7+ on any OS
}
```

## OS Platform Specific

Used when You want to run different commands for different OS platform:

```toml
[commands]
foo = {
    linux = "foo-linux {file_path}",  # runs on on Linux
    darwin = "foo-mac {file_path}",   # runs on on macOS
    win = "foo-win {file_path}",      # runs on on Windows
}
```

## Command Array

quikrun will automatically pick the first command that's binary is installed on your system!

```toml
[commands]
js = ["bun run {file_path}", "deno run {file_path}", "node {file_path}"]
```

## Shell & Platform Specific

You can nest compile-run tables under shell or operating systems (inside shell families) as well.

```toml
[commands]
cpp = {
  posix = {
    linux = { compile = "g++ -Wall {file_path} -o {out_file}", run = "{out_file}" },       # runs on bash/zsh... on Linux
    darwin = { compile = "clang++ -Wall {file_path} -o {out_file}", run = "{out_file}" },  # runs on bash/zsh... on macOS
  }
}

# Or Opposite
cpp = {
  linux = {
    posix = { compile = "g++ -Wall {file_path} -o {out_file}", run = "{out_file}" },       # runs on Linux when using posix shell
    pwsh = { compile = "clang++ -Wall {file_path} -o {out_file}", run = "{out_file}" },  # runs on Linux when using powershell
  }
}

```

## Referencing Extension

Use the `@` prefix to Reference a extension's configuration from an already defined command template!

> [!WARNING]
> Make sure the extension you are referencing is defined before!

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
