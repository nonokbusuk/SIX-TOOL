"""Menu 6 — Extract Domain (Auto Add https)"""
import re
from urllib.parse import urlparse
from colorama import Fore, Style


def normalize(url):
    url = url.strip()
    if not url:
        return None
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    try:
        p = urlparse(url)
        return f"{p.scheme}://{p.netloc}"
    except Exception:
        return None


def run():
    print(f"{Fore.CYAN}[*] Extract Domain{Style.RESET_ALL}")
    print("Masukkan URL / domain (satu per baris, kosongkan 2x untuk selesai):")
    results = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        norm = normalize(line)
        if norm:
            results.append(norm)
            print(f"{Fore.GREEN}[+] {norm}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[!] Tidak valid: {line}{Style.RESET_ALL}")

    if results:
        with open("results/domains.txt", "w") as f:
            f.write("\n".join(results))
        print(f"{Fore.GREEN}[+] Disimpan ke results/domains.txt{Style.RESET_ALL}")
