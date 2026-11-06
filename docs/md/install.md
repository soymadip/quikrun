# Installation

<center>
Install {{meta.project.title }} from your distro's package manager or PyPI.
</center>

## Package Manager

Install {{meta.project.title }} With your distro's package Manager.

### Windows (WinGet)

Install {{meta.project.title}} from the Winget Repo:

```sh
winget install soymadip.quikrun
```

> [!WARNING]
> As WinGet package needs quite some time to get approved,  
> Winget package may not be up-to-date

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

## Via PyPI

If there's not a package for your distro/OS, you can install directly from [PyPI](https://pypi.org):

- Globally uing [pipx](https://pipx.pypa.io/): `pipx install quikrun` (recommended)
- Locally using pip: `pip install quikrun`

## Prebuilt Binary

Prebuilt binaries for Linux and Windows are available in [Releases](https://github.com/soymadip/quikrun/releases/latest).

> [!TIP]
> The Windows `.exe` is portable and needs no installer.  
> For the Linux binary, after downloading, run `chmod +x quikrun-linux-amd64` and then `./quikrun-linux-amd64`.

## From Source

Clone the repository and install locally:

```bash
git clone {{meta.project.repo }}
cd quikrun
pip install .
```
