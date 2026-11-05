# IPPoint

A lightweight Python/Tkinter utility for checking the country associated with an IP address.

## Features

- Look up a manually entered IPv4 or IPv6 address.
- **Check my public IP** detects the public IP address visible to the internet, then looks up its country.
- Displays the country name and flag.
- Uses background threads so the window stays responsive.
- Uses only Python's standard library; no pip packages are required to run from source.
- Includes a **Help → About IPPoint** window with app information, license details, external services, and a link to GitHub Issues.

## Requirements

- Python 3.10 or newer
- Tkinter
  - Windows: included with most standard Python installations.
  - Linux: install your distribution's Tkinter package (for example, `python3-tk` on Debian/Ubuntu).
  - macOS: use a Python installation that includes Tcl/Tk support.

## Run from source

```bash
python ippoint.py
```

On systems where the command is `python3`, use:

```bash
python3 ippoint.py
```

## Build with Nuitka

Build on the operating system you want to target. Nuitka creates native builds for the system where it runs; a Windows build does not produce Linux or macOS binaries, and vice versa.

Each build script creates and uses the project's local `.venv` directory and installs Nuitka there. You do not need to install Nuitka globally.

### Windows

Run:

```bat
build.bat
```

The result is `dist\\IPPoint.exe`.

### Linux

Install Python 3.10+, Tkinter, and a C compiler/toolchain first. On Debian or Ubuntu, for example:

```bash
sudo apt install python3-tk build-essential
```

Then run:

```bash
bash build.sh
```

The result is `dist/IPPoint`.

### macOS

Install Python 3.10+ with Tcl/Tk support and the Xcode Command Line Tools. Then run:

```bash
xcode-select --install
bash build-macos.sh
```

The script asks Nuitka to create a macOS application bundle; check the `dist` directory for `IPPoint.app`.

## External services

- [ipify](https://www.ipify.org/) detects the public IP for the **Check my public IP** feature.
- [ipwho.is](https://ipwho.is/) provides the country and country-code lookup.

Both services are contacted over HTTPS. When you use **Check my public IP**, your public IP is sent to ipify and then to ipwho.is to retrieve its country. When you enter an address manually, that address is sent to ipwho.is.

## Notes

IP geolocation is an estimate, not a physical-location detector. Country-level results are generally more useful than city-level results, but VPN exits, proxies, hosting networks, and geolocation database differences can affect accuracy. The country shown may not match the VPN provider's registered country or the server's physical location.

## License

IPPoint is distributed under the **GNU General Public License, version 3 (GPL-3.0)**. See the [`LICENSE`](LICENSE) file for the complete terms.

## Project support

Report bugs or request features on the [GitHub Issues page](https://github.com/awkbashgrepsed/IPPoint/issues).
