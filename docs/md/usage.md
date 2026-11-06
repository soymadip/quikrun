# Usage

## Basic Usage

```bash
quikrun <file>
```

Quikrun detects how to run the file automatically by checking its [shebang](<https://en.wikipedia.org/wiki/Shebang_(Unix)>) first, then its extension.

```bash
quikrun hello.py       # runs: python3 hello.py
quikrun hello.js       # runs: node hello.js
quikrun hello.c        # compiles with gcc, then runs the binary
```

- To view the help menu:

  ```bash
    quikrun --help
  ```

- To print the version:

  ```bash
  quikrun --version
  ```

## CLI Flags

You can override configuration settings on the fly using CLI flags (these take the highest precedence over configuration files). This reference is generated from the CLI parser:

<!-- DYNAMIC_CLI_FLAGS_START -->

| Flag                                                  | Description                                                                                   |
| :---------------------------------------------------- | :-------------------------------------------------------------------------------------------- |
| `-h`, `--help`                                        | show this help message and exit                                                               |
| `-v`, `--version`                                     | Print the version and exit.                                                                   |
| `-i`, `--info`                                        | Show project information, version, and repository details                                     |
| `-s <shell>`, `--shell <shell>`                       | Which shell to use. (Choices: `auto, posix, cmd, pwsh`)                                       |
| `-p <platform>`, `--platform <platform>`              | Target platform or OS override. (Choices: `auto, linux, win, darwin`)                         |
| `--clear-terminal`, `--no-clear-terminal`             | Clear the terminal before running.                                                            |
| `--scroll-up`                                         | Scroll the terminal up instead of clearing it.                                                |
| `--show-command`                                      | Show the command in the footer.                                                               |
| `--no-show-command`                                   | Do not show the command in the footer.                                                        |
| `--show-time-took`, `--no-show-time-took`             | Whether to display the execution duration at footer.                                          |
| `--show-divider`, `--no-show-divider`                 | Whether to print the separation line before the footer.                                       |
| `--cd-to-file-dir`, `--no-cd-to-file-dir`             | Whether to change the working directory to the target file's folder before running/compiling. |
| `--keep-build-artifacts`, `--no-keep-build-artifacts` | Whether to retain temporary or compiled binaries after execution completes.                   |
| `--cache-dir <path>`                                  | Custom directory used for cache and compiled build artifacts.                                 |
| `--auto-exit <auto-exit>`                             | Controls automatic process exit behavior. (Choices: `always, never, on_success`)              |

<!-- DYNAMIC_CLI_FLAGS_END -->

Example:

```bash
quikrun main.cpp --no-show-command --no-clear-terminal --cd-to-file-dir
```

## Passing Arguments to Script

- For simple cases with no cli flag conflicts:

  ```bash
  quikrun script.py arg1 arg2 --file_flag
  ```

- Use the `--` separator to explicitly forward arguments to the script:

  ```bash
  quikrun script.py -- --verbose --output result.txt
  #                 ↑ everything after '--' goes to script.py
  ```

## Shebang Detection

If the file starts with a shebang (`#!`), quikrun will execute it directly ignoring extension:

```bash
# my_script (no extension, shebang: #!/usr/bin/env python3)
quikrun my_script
```

## Exit Codes

Quikrun forwards the exit code of the executed script directly to the shell, so you can use it in pipelines & scripts:

```bash
quikrun faulty.py || echo "script failed"
```
