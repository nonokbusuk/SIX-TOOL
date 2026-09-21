"""Menu 9 — Grab Domain from haxor.id"""
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def run():
    print(f"{Fore.CYAN}[*] Grab Domain from haxor.id{Style.RESET_ALL}")
    try:
        r = requests.get("https://haxor.id/", headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        domains = set()
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if "http" in href and "haxor.id" not in href:
                domains.add(href.split("/")[2])
        print(f"{Fore.GREEN}[+] Ditemukan {len(domains)} domain:{Style.RESET_ALL}")
        for d in sorted(domains):
            print(f"    {d}")
        if domains:
            with open("results/haxor_domains.txt", "w") as f:
                f.write("\n".join(sorted(domains)))
            print(f"{Fore.GREEN}[+] Disimpan ke results/haxor_domains.txt{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
