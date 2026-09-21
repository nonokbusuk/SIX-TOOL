"""Menu 1 — WebShell Finder (Dir Scan with 48k Path)"""
import os
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

WORDLIST = os.path.join("wordlists", "webshell_paths.txt")

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

SUSPICIOUS_KEYWORDS = [
    "shell", "cmd", "eval", "system", "passthru", "exec",
    "backdoor", "b374k", "c99", "r57", "indoxploit", "alfa",
    "wso", "angel", "mini", "uploader", "up.php", "adminer",
]


def check_path(base, path, timeout=8):
    url = base.rstrip("/") + "/" + path.lstrip("/")
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=False)
        if r.status_code in (200, 301, 302, 403):
            return (r.status_code, url, len(r.content))
    except requests.RequestException:
        pass
    return None


def run():
    print(f"{Fore.CYAN}[*] WebShell Finder — Dir Scan{Style.RESET_ALL}")
    target = input("URL target (https://example.com): ").strip()
    if not target:
        print(f"{Fore.RED}[!] URL kosong.{Style.RESET_ALL}")
        return
    if not target.startswith("http"):
        target = "https://" + target

    if not os.path.exists(WORDLIST):
        print(f"{Fore.RED}[!] Wordlist tidak ditemukan: {WORDLIST}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}    Taruh file 'webshell_paths.txt' di folder wordlists/{Style.RESET_ALL}")
        return

    with open(WORDLIST, "r", errors="ignore") as f:
        paths = [line.strip() for line in f if line.strip()]

    print(f"{Fore.YELLOW}[*] Total path: {len(paths)}{Style.RESET_ALL}")
    threads = int(input("Threads [default 20]: ").strip() or 20)

    found = []
    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(check_path, target, p): p for p in paths}
        try:
            for i, fut in enumerate(as_completed(futures), 1):
                res = fut.result()
                if res:
                    status, url, size = res
                    color = Fore.GREEN if status == 200 else Fore.YELLOW
                    print(f"{color}[{status}] {url} ({size} bytes){Style.RESET_ALL}")
                    found.append((status, url))
                if i % 100 == 0:
                    print(f"{Fore.CYAN}    ... {i}/{len(paths)} tested{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}[!] Dibatalkan.{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}[+] Selesai. Ditemukan {len(found)} hasil.{Style.RESET_ALL}")
    if found:
        os.makedirs("results", exist_ok=True)
        with open("results/webshell_dir.txt", "w") as f:
            for s, u in found:
                f.write(f"{s}\t{u}\n")
        print(f"{Fore.GREEN}[+] Disimpan ke results/webshell_dir.txt{Style.RESET_ALL}")
