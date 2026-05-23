# Supported Languages

These are the default commands templates.
Quikrun detects the language from the file extension if shebang is not present.

> [!NOTE]
>
> - `@ext` means the commands from the `ext` extension are inherited in the current extension.
> - `->` means the binary/command is tried to find in order.

## Interpreted

Interpreted languages are run directly using the interpreter.

<!-- DYNAMIC_INTERPRETED_START -->
<!-- DYNAMIC_INTERPRETED_END -->

## Compiled

Compiled languages are built first, then the resulting binary is executed. The binary is written to a temporary path.

<!-- DYNAMIC_COMPILED_START -->
<!-- DYNAMIC_COMPILED_END -->
