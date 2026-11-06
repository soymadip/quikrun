# Installation

<center>
Install {{meta.project.title }} from your distro's package manager or PyPI.
</center>

## Distro Packages

Install {{meta.project.title }} With your distro's package Manager.

### Arch Linux (MyRepo Repo)

You can add MyRepo Repository to Your system & Install quikrun with pacman directly.

- Setup: Head to [this page](https://mydehq.github.io/my-repo)
- Then: `sudo pacman -Syu {{meta.project.title}}`

### Arch Linux (AUR)

To Build the package directly in your system use an AUR helper:

```bash
paru -S quikrun

# or
yay -S quikrun
```

## Other Methods

### Prebuilt Binary

Prebuilt binaries are available for different platforms in the [Releases](https://github.com/soymadip/quikrun/releases/latest).

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
