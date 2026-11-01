# Installation

<center>
Install {{meta.project.title }} from your distro's package manager or PyPI.
</center>

## Distro Packages

Install {{meta.project.title }} With your distro's package Manager.

### Arch Linux (AUR)

Use an AUR helper:

```bash
paru -S quikrun

# or
yay -S quikrun
```

## Other Methods

### Prebuilt Binary

Prebuilt binaries are available for different platforms in the [Releases](https://github.com/soymadip/quikrun/releases/latest).

> [!INFO]
> This project uses the SignPath Foundation for code signing.

### Via PyPI

If there is not package for your distro/os, you can install directly:

```bash
# Using uv (highly recommended for global installation)
uv tool install quikrun

# Using pipx (another good way to install globally)
pipx install quikrun

# Using pip (if you wanna install locally in a project)
pip install quikrun
```

## From Source

Clone the repository and install locally:

```bash
git clone {{meta.project.repo }}
cd quikrun
pip install .
```
