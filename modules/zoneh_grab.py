"""Menu 10 — Grab Domain from zone-h.org"""
import os
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Style

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def run():
    print(f"{Fore.CYAN}[*] Grab Domain from zone-h.org{Style.RESET_ALL}")
    try:
        r = requests.get("http://www.zone-h.org/archive", headers=HEADERS, timeout=20)
        soup = BeautifulSoup(r.text, "html.parser")
        domains = set()
        for td in soup.find_all("td"):
            text = td.get_text(strip=True)
            if "." in text and " " not in text and len(text) < 100:
                domains.add(text)
        print(f"{Fore.GREEN}[+] Ditemukan {len(domains)} domain:{Style.RESET_ALL}")
        for d in sorted(domains)[:50]:
            print(f"    {d}")
        if domains:
            os.makedirs("results", exist_ok=True)
            with open("results/zoneh_domains.txt", "w") as f:
                f.write("\n".join(sorted(domains)))
            print(f"{Fore.GREEN}[+] Disimpan ke results/zoneh_domains.txt{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
