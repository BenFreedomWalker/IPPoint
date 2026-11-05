"""IPPoint - a small public-IP and country lookup utility."""

from __future__ import annotations

import ipaddress
import json
import queue
import threading
import urllib.parse
import urllib.request
import webbrowser
import tkinter as tk
from tkinter import ttk


GEO_API = "https://ipwho.is/"
PUBLIC_IP_API = "https://api64.ipify.org?format=json"
TIMEOUT = 12
APP_VERSION = "1.0.0"
ISSUES_URL = "https://github.com/awkbashgrepsed/IPPoint/issues"
LICENSE_URL = "https://github.com/awkbashgrepsed/IPPoint/blob/main/LICENSE"


def http_json(url: str) -> dict:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "IPPoint/1.0", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return json.loads(response.read().decode("utf-8"))


def get_public_ip() -> str:
    data = http_json(PUBLIC_IP_API)
    address = data.get("ip", "").strip()
    return str(ipaddress.ip_address(address))


def lookup_ip(address: str) -> dict:
    encoded = urllib.parse.quote(address, safe=":")
    data = http_json(GEO_API + encoded)
    if not data.get("success"):
        raise ValueError(data.get("message") or "The lookup service rejected this IP.")
    return data


def country_flag(country_code: str) -> str:
    code = country_code.upper()
    if len(code) != 2 or not code.isascii() or not code.isalpha():
        return ""
    return "".join(chr(0x1F1E6 + ord(char) - ord("A")) for char in code)


class IPPoint:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("IPPoint")
        self.root.geometry("460x350")
        self.root.minsize(420, 330)

        menu = tk.Menu(self.root)
        help_menu = tk.Menu(menu, tearoff=False)
        help_menu.add_command(label="About IPPoint", command=self.show_about)
        menu.add_cascade(label="Help", menu=help_menu)
        self.root.configure(menu=menu)

        self.results: queue.Queue = queue.Queue()
        self.busy = False

        self.ip_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Enter an IP address or check your public IP.")
        self.country_var = tk.StringVar(value="—")
        self.flag_var = tk.StringVar(value="🌐")
        self.address_var = tk.StringVar(value="No address checked yet")

        self._build_ui()
        self.root.after(100, self._process_results)

    def show_about(self) -> None:
        window = tk.Toplevel(self.root)
        window.title("About IPPoint")
        window.resizable(False, False)
        window.transient(self.root)
        window.grab_set()

        frame = ttk.Frame(window, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="IPPoint", font=("Segoe UI", 18, "bold")).pack(anchor="w")
        ttk.Label(frame, text=f"Version {APP_VERSION}").pack(anchor="w", pady=(0, 12))
        ttk.Label(
            frame,
            text="A lightweight desktop utility for checking the country associated "
                 "with an IPv4 or IPv6 address.",
            wraplength=390,
            justify="left",
        ).pack(anchor="w", pady=(0, 12))

        ttk.Label(frame, text="External services", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Label(
            frame,
            text="• ipify — detects your public IP when you use “Check my public IP”.\n"
                 "• ipwho.is — looks up the country and country code for the IP address.\n\n"
                 "The address is sent to these services as needed; requests use HTTPS.",
            wraplength=390,
            justify="left",
        ).pack(anchor="w", pady=(3, 12))

        ttk.Label(frame, text="License", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        ttk.Label(
            frame,
            text="GNU General Public License, version 3 (GPL-3.0). "
                 "This software is provided without warranty. See the LICENSE file "
                 "for the complete terms.",
            wraplength=390,
            justify="left",
        ).pack(anchor="w", pady=(3, 14))

        links = ttk.Frame(frame)
        links.pack(fill="x")
        ttk.Button(
            links, text="GitHub Issues",
            command=lambda: webbrowser.open(ISSUES_URL),
        ).pack(side="left")
        ttk.Button(
            links, text="View license",
            command=lambda: webbrowser.open(LICENSE_URL),
        ).pack(side="left", padx=(8, 0))
        ttk.Button(links, text="Close", command=window.destroy).pack(side="right")

        window.update_idletasks()
        x = self.root.winfo_rootx() + (self.root.winfo_width() - window.winfo_width()) // 2
        y = self.root.winfo_rooty() + (self.root.winfo_height() - window.winfo_height()) // 2
        window.geometry(f"+{x}+{y}")

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=22)
        outer.pack(fill="both", expand=True)

        ttk.Label(outer, text="IPPoint", font=("Segoe UI", 22, "bold")).pack(anchor="w")
        ttk.Label(
            outer,
            text="Find the country behind a public IP address.",
            foreground="#666666",
        ).pack(anchor="w", pady=(2, 18))

        entry_row = ttk.Frame(outer)
        entry_row.pack(fill="x")
        self.entry = ttk.Entry(entry_row, textvariable=self.ip_var, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True)
        self.entry.bind("<Return>", lambda _event: self.lookup_manual())

        self.lookup_button = ttk.Button(entry_row, text="Look up", command=self.lookup_manual)
        self.lookup_button.pack(side="left", padx=(8, 0))

        self.public_button = ttk.Button(
            outer, text="Check my public IP", command=self.lookup_public_ip
        )
        self.public_button.pack(anchor="w", pady=(10, 22))

        result = ttk.LabelFrame(outer, text="Result", padding=16)
        result.pack(fill="both", expand=True)

        result_row = ttk.Frame(result)
        result_row.pack(fill="x")
        ttk.Label(result_row, textvariable=self.flag_var, font=("Segoe UI Emoji", 34)).pack(
            side="left", padx=(0, 14)
        )
        ttk.Label(
            result_row, textvariable=self.country_var, font=("Segoe UI", 19, "bold")
        ).pack(side="left", anchor="center")

        ttk.Separator(result).pack(fill="x", pady=12)
        ttk.Label(result, text="IP address", foreground="#666666").pack(anchor="w")
        ttk.Label(result, textvariable=self.address_var, font=("Consolas", 11)).pack(
            anchor="w", pady=(3, 0)
        )

        ttk.Label(
            outer,
            textvariable=self.status_var,
            foreground="#666666",
            wraplength=410,
        ).pack(anchor="w", pady=(12, 0))

        self.entry.focus_set()

    def _set_busy(self, busy: bool, message: str) -> None:
        self.busy = busy
        state = "disabled" if busy else "normal"
        self.lookup_button.configure(state=state)
        self.public_button.configure(state=state)
        self.entry.configure(state=state)
        self.status_var.set(message)

    def lookup_manual(self) -> None:
        if self.busy:
            return
        raw = self.ip_var.get().strip()
        try:
            address = str(ipaddress.ip_address(raw))
        except ValueError:
            self.status_var.set("Please enter a valid IPv4 or IPv6 address.")
            return
        self._start_lookup(address)

    def lookup_public_ip(self) -> None:
        if self.busy:
            return
        self._set_busy(True, "Checking your current public IP…")
        threading.Thread(target=self._public_worker, daemon=True).start()

    def _public_worker(self) -> None:
        try:
            address = get_public_ip()
            data = lookup_ip(address)
            self.results.put(("success", address, data))
        except Exception as exc:
            self.results.put(("error", str(exc)))

    def _start_lookup(self, address: str) -> None:
        self._set_busy(True, f"Looking up {address}…")
        threading.Thread(target=self._lookup_worker, args=(address,), daemon=True).start()

    def _lookup_worker(self, address: str) -> None:
        try:
            data = lookup_ip(address)
            self.results.put(("success", address, data))
        except Exception as exc:
            self.results.put(("error", str(exc)))

    def _process_results(self) -> None:
        try:
            while True:
                result = self.results.get_nowait()
                if result[0] == "success":
                    _, address, data = result
                    country = data.get("country") or "Unknown country"
                    flag = country_flag(data.get("country_code", ""))
                    self.flag_var.set(flag or "🌐")
                    self.country_var.set(country)
                    self.address_var.set(address)
                    self.ip_var.set(address)
                    self._set_busy(False, "Country-level IP geolocation; VPN exits and databases may vary.")
                else:
                    self._set_busy(False, f"Lookup failed: {result[1]}")
        except queue.Empty:
            pass
        self.root.after(100, self._process_results)


def main() -> None:
    root = tk.Tk()
    IPPoint(root)
    root.mainloop()


if __name__ == "__main__":
    main()
