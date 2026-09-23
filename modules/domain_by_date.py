"""Menu 8 — Grab Registered Domain by Date"""
import io
import os
import re
import zipfile
import requests
from colorama import Fore, Style

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

FEED_URL = "https://whoisds.com/sample/other-db/nrd-updats.zip"


def fetch_domains():
    r = requests.get(FEED_URL, headers=HEADERS, timeout=60)
    r.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    lines = zf.read(zf.namelist()[0]).decode(errors="ignore").splitlines()
    return [l.strip().lower() for l in lines if l.strip()]


def run():
    print(f"{Fore.CYAN}[*] Grab Registered Domain by Date{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}[*] Sumber: whoisds.com feed NRD (newly registered domains){Style.RESET_ALL}")
    print(f"{Fore.YELLOW}    Arsip per-tanggal spesifik memerlukan akun whoisds;{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}    modul ini memakai feed publik terbaru.{Style.RESET_ALL}")

    keyword = input("Filter keyword / TLD (kosongkan untuk semua, contoh: .id): ").strip().lower()
    limit = int(input("Maksimal hasil ditampilkan [50]: ").strip() or 50)

    try:
        print(f"{Fore.YELLOW}[*] Mengunduh feed NRD...{Style.RESET_ALL}")
        domains = fetch_domains()
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal mengunduh feed: {e}{Style.RESET_ALL}")
        return

    print(f"{Fore.GREEN}[+] Feed dimuat: {len(domains)} domain{Style.RESET_ALL}")

    if keyword:
        if keyword.startswith("."):
            filtered = [d for d in domains if d.endswith(keyword)]
        else:
            filtered = [d for d in domains if keyword in d]
    else:
        filtered = domains

    print(f"{Fore.GREEN}[+] Cocok dengan filter: {len(filtered)} domain{Style.RESET_ALL}")
    for d in filtered[:limit]:
        print(f"    {d}")

    if filtered:
        os.makedirs("results", exist_ok=True)
        with open("results/registered_domains.txt", "w") as f:
            f.write("\n".join(filtered))
        print(f"{Fore.GREEN}[+] Disimpan ke results/registered_domains.txt{Style.RESET_ALL}")
