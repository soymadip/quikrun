# Usage

## Basic Usage

```bash
quikrun <file>
```

Quikrun detects how to run the file automatically by checking its shebang line first, then its extension.

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

## Passing Arguments to Script

- For simple cases with no flag conflicts:

  ```bash
  quikrun script.py arg1 arg2
  ```

- Use the `--` separator to forward arguments to the script instead of quikrun:

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

Quikrun forwards the exit code of the executed script directly to the shell, so you can use it in pipelines and scripts:

```bash
quikrun test.py || echo "script failed"
```
