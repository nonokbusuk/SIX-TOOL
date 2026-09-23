"""Menu 5 — Scanner ENV & Debug Method"""
import os
import random
import string
import requests
from colorama import Fore, Style

PATHS = [
    "/.env", "/.env.local", "/.env.production", "/.env.dev",
    "/config/.env", "/app/.env", "/laravel/.env", "/wp-config.php.bak",
    "/debug", "/debug.log", "/phpinfo.php", "/info.php",
    "/server-status", "/server-info", "/.git/config", "/.git/HEAD",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def run():
    print(f"{Fore.CYAN}[*] Scanner ENV & Debug{Style.RESET_ALL}")
    target = input("URL target (https://example.com): ").strip()
    if not target:
        print(f"{Fore.RED}[!] URL kosong.{Style.RESET_ALL}")
        return
    if not target.startswith("http"):
        target = "https://" + target

    baseline_path = "/" + "".join(random.choices(string.ascii_lowercase + string.digits, k=16))
    baseline = None
    try:
        baseline = requests.get(target.rstrip("/") + baseline_path, headers=HEADERS, timeout=10, allow_redirects=False)
    except requests.RequestException as e:
        print(f"{Fore.RED}[!] Target tidak dapat dijangkau: {e}{Style.RESET_ALL}")
        return
    print(f"{Fore.YELLOW}[*] Baseline soft-404: {baseline.status_code} ({len(baseline.content)} bytes){Style.RESET_ALL}")

    def is_soft_404(r):
        if baseline.status_code != 200:
            return False
        return r.status_code == 200 and (
            r.content == baseline.content or len(r.content) == len(baseline.content)
        )

    found = []
    for path in PATHS:
        url = target.rstrip("/") + path
        try:
            r = requests.get(url, headers=HEADERS, timeout=10, allow_redirects=False)
            if is_soft_404(r):
                print(f"{Fore.YELLOW}[~] {url} -> soft-404 (diabaikan){Style.RESET_ALL}")
            elif r.status_code == 200:
                print(f"{Fore.GREEN}[200] {url} ({len(r.content)} bytes){Style.RESET_ALL}")
                found.append(url)
            elif r.status_code in (301, 302, 403):
                print(f"{Fore.YELLOW}[{r.status_code}] {url}{Style.RESET_ALL}")
        except requests.RequestException:
            pass

    print(f"\n{Fore.GREEN}[+] Selesai. Ditemukan {len(found)} file sensitif.{Style.RESET_ALL}")
    if found:
        os.makedirs("results", exist_ok=True)
        with open("results/env_debug.txt", "w") as f:
            f.write("\n".join(found))
        print(f"{Fore.GREEN}[+] Disimpan ke results/env_debug.txt{Style.RESET_ALL}")
