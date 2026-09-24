"""Menu 8 — Grab Registered Domain by Date"""
import os
import json
import requests
from colorama import Fore, Style

CRTSH_URL = "https://crt.sh/"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def run():
    print(f"{Fore.CYAN}[*] Grab Registered Domain by Date (via crt.sh){Style.RESET_ALL}")
    domain = input("Domain dasar (misal: example.com): ").strip().lstrip("%")
    if not domain:
        print(f"{Fore.RED}[!] Domain tidak boleh kosong.{Style.RESET_ALL}")
        return
    date = input("Tanggal (YYYY-MM-DD): ").strip()

    print(f"{Fore.YELLOW}[*] Mengambil data sertifikat untuk %.{domain} ...{Style.RESET_ALL}")
    try:
        r = requests.get(
            CRTSH_URL,
            params={"output": "json", "q": f"%.{domain}"},
            headers=HEADERS,
            timeout=60,
        )
        r.raise_for_status()
        records = r.json()
    except Exception as e:
        print(f"{Fore.RED}[!] Error mengambil data: {e}{Style.RESET_ALL}")
        return

    found = {}
    for rec in records:
        entry = rec.get("common_name") or rec.get("name_value", "")
        not_before = (rec.get("not_before") or "")[:10]
        for name in entry.split("\n"):
            name = name.strip().lower()
            if not name.endswith(domain):
                continue
            if date and not_before != date:
                continue
            found[name] = not_before

    if not found:
        print(f"{Fore.RED}[!] Tidak ada domain ditemukan{f' pada {date}' if date else ''}.{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}[+] Ditemukan {len(found)} domain:{Style.RESET_ALL}")
    for name, nb in sorted(found.items()):
        print(f"    [{nb}] {name}")

    os.makedirs("results", exist_ok=True)
    out = "results/domains_by_date.txt"
    with open(out, "w") as f:
        for name, nb in sorted(found.items()):
            f.write(f"{nb} {name}\n")
    print(f"{Fore.GREEN}[+] Disimpan ke {out}{Style.RESET_ALL}")
