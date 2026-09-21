"""Menu 3 — Reverse IP Lookup"""
import requests
from colorama import Fore, Style


def run():
    print(f"{Fore.CYAN}[*] Reverse IP Lookup{Style.RESET_ALL}")
    ip = input("IP address: ").strip()
    if not ip:
        print(f"{Fore.RED}[!] IP kosong.{Style.RESET_ALL}")
        return

    # Sumber publik: hackertarget API (free)
    try:
        r = requests.get(f"https://api.hackertarget.com/reverseiplookup/?q={ip}", timeout=15)
        if r.status_code == 200 and "error" not in r.text.lower():
            domains = [d.strip() for d in r.text.splitlines() if d.strip()]
            print(f"{Fore.GREEN}[+] Ditemukan {len(domains)} domain:{Style.RESET_ALL}")
            for d in domains:
                print(f"    {d}")
        else:
            print(f"{Fore.YELLOW}[!] Tidak ada hasil atau API limit: {r.text[:100]}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
