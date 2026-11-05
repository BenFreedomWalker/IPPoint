# IPPoint

A lightweight Python/Tkinter utility for checking the country associated with an IP address.

## Features

- Look up a manually entered IPv4 or IPv6 address.
- **Check my public IP** detects the public IP address visible to the internet, then looks up its country.
- Displays the country name and flag.
- Uses background threads so the window stays responsive.
- Uses only Python's standard library; no pip packages are required.

## Requirements

- Python 3.10 or newer
- Tkinter (included with most standard Windows Python installations)

## Run

```bash
python ippoint.py
```

## Services

- [ipify](https://www.ipify.org/) detects the public IP for the **Check my public IP** feature.
- [ipwho.is](https://ipwho.is/) provides the country and country-code lookup.

Both services are contacted over HTTPS. When you use **Check my public IP**, your public IP is sent to the lookup service to retrieve its country. When you enter an address manually, that address is sent to the lookup service.

## Notes

IP geolocation is an estimate, not a physical-location detector. Country-level results are generally more useful than city-level results, but VPN exits, proxies, hosting networks, and geolocation database differences can affect accuracy. The country shown may not match the VPN provider's registered country or the server's physical location.

## License

No license has been added yet.
