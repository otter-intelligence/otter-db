## Installing uv and Python

This project is set up to use [**uv**](https://docs.astral.sh/uv/), the new package
manager for Python. `uv` replaces traditional use of `pyenv`, `pipx`, `poetry`, `pip`,
etc. This is a quick cheat sheet on that:

On macOS or Linux, if you don't have `uv` installed, a quick way to install it:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

For macOS, you prefer [brew](https://brew.sh/) you can install or upgrade uv with:

```shell
brew update
brew install uv
```

On Windows, open PowerShell and run:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or install via [winget](https://learn.microsoft.com/en-us/windows/package-manager/):

```powershell
winget install --id=astral-sh.uv -e
```

Or via [scoop](https://scoop.sh/):

```powershell
scoop install uv
```

See [uv's docs](https://docs.astral.sh/uv/getting-started/installation/) for more
installation methods and platforms.

Now you can use uv to install a current Python environment:

```shell
uv python install 3.13 # Or pick another version.
```

## Installing just (optional)

[just](https://github.com/casey/just) is a cross-platform command runner. It's optional—you can use `make` instead—but `just` works better on Windows.

On macOS or Linux:

```shell
# via cargo
cargo install just

# via brew (macOS)
brew install just
```

On Windows:

```powershell
# via winget
winget install --id=Casey.Just -e

# via scoop
scoop install just
```

See [just's docs](https://github.com/casey/just#installation) for more installation methods.
