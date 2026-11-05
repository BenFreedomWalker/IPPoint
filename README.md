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
- Tkinter (included with most standard Windows Python installations)

## Run from source

```bash
python ippoint.py
```

## Build on Windows with Nuitka

Install Nuitka in the Python environment you use to run IPPoint:

```bat
python -m pip install nuitka
```

Then run `build.bat`. It creates a standalone, single-file `IPPoint.exe` in the `dist` directory. The build script uses the Python interpreter associated with the `python` command.

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
