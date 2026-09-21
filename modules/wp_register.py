"""Menu 7 — WordPress Register Finder"""
import requests
from colorama import Fore, Style

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def run():
    print(f"{Fore.CYAN}[*] WordPress Register Finder{Style.RESET_ALL}")
    target = input("URL target (https://example.com): ").strip()
    if not target:
        print(f"{Fore.RED}[!] URL kosong.{Style.RESET_ALL}")
        return
    if not target.startswith("http"):
        target = "https://" + target

    url = target.rstrip("/") + "/wp-login.php?action=register"
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        if r.status_code == 200 and ("register" in r.text.lower() or "user_login" in r.text):
            print(f"{Fore.GREEN}[+] Registrasi TERBUKA: {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}[-] Registrasi tertutup atau tidak terdeteksi.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
