# Default Command Templates

Below are the default commands templates.  
These are used as fallbacks when no user or project configuration is found for a given file's extension.

> [!NOTE]
>
> - `@ext1` means the commands from the `ext1` extension are inherited for that extension.
> - `->` means the command's binary is tried to find if installed in that order.

## Interpreted

Interpreted languages are run directly using the interpreter.

<!-- DYNAMIC_INTERPRETED_START -->

| Extension | Command                                    |
| --------- | ------------------------------------------ |
| `.bash`   | `bash {file_path}`                         |
| `.c++`    | `@cpp`                                     |
| `.cjs`    | `@js`                                      |
| `.cxx`    | `@cpp`                                     |
| `.dart`   | `dart run {file_path}`                     |
| `.fish`   | `fish {file_path}`                         |
| `.java`   | `java {file_path}`                         |
| `.jl`     | `julia {file_path}`                        |
| `.js`     | `bun run {file_path}` → `node {file_path}` |
| `.lua`    | `lua {file_path}`                          |
| `.mjs`    | `@js`                                      |
| `.php`    | `php {file_path}`                          |
| `.pl`     | `perl {file_path}`                         |
| `.py`     | `python3 {file_path}`                      |
| `.r`      | `Rscript {file_path}`                      |
| `.rb`     | `ruby {file_path}`                         |
| `.sh`     | `bash {file_path}`                         |
| `.swift`  | `swift {file_path}`                        |
| `.ts`     | `@js` → `ts-node {file_path}`              |

<!-- DYNAMIC_INTERPRETED_END -->

## Compiled

Compiled languages are built first, then the resulting binary is executed. The binary is written to a temporary path.

<!-- DYNAMIC_COMPILED_START -->

| Extension | Compile Command                                                   | Run Command                |
| --------- | ----------------------------------------------------------------- | -------------------------- |
| `.c`      | `gcc -Wall -Wextra {file_path} -o {out_file}`                     | `{out_file}`               |
| `.cpp`    | `g++ -std=c++23 -Wall -Wextra -Wshadow {file_path} -o {out_file}` | `{out_file}`               |
| `.go`     | `go build -o {out_file} {file_path}`                              | `{out_file}`               |
| `.hs`     | `ghc -o {out_file} {file_path}`                                   | `{out_file}`               |
| `.kt`     | `kotlinc {file_path} -include-runtime -d {out_stem}.jar`          | `java -jar {out_stem}.jar` |
| `.nim`    | `nim c --out:{out_file} {file_path}`                              | `{out_file}`               |
| `.rs`     | `rustc {file_path} -o {out_file}`                                 | `{out_file}`               |
| `.v`      | `v -o {out_file} {file_path}`                                     | `{out_file}`               |
| `.zig`    | `zig build-exe {file_path} -femit-bin={out_file}`                 | `{out_file}`               |

<!-- DYNAMIC_COMPILED_END -->
