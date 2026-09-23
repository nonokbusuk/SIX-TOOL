"""Menu 2 — WebShell Finder (Automatic Filename Enumeration)"""
import os
import random
import string
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

WORDLISTS = [
    os.path.join("wordlists", "webshell_names.txt"),
    os.path.join("wordlists", "shell.txt"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

DEFAULT_NAMES = [
    "shell.php", "cmd.php", "c99.php", "r57.php", "b374k.php",
    "wso.php", "alfa.php", "indoxploit.php", "mini.php", "uploader.php",
    "backdoor.php", "x.php", "1.php", "a.php", "test.php",
]


def check_file(base, name, timeout=8):
    url = base.rstrip("/") + "/" + name.lstrip("/")
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=False)
        if r.status_code in (200, 301, 302):
            return (r.status_code, url, len(r.content))
    except requests.RequestException:
        pass
    return None


def get_baseline(target):
    path = "".join(random.choices(string.ascii_lowercase + string.digits, k=16)) + ".php"
    try:
        r = requests.get(target.rstrip("/") + "/" + path, headers=HEADERS, timeout=10, allow_redirects=False)
        return r
    except requests.RequestException as e:
        print(f"{Fore.RED}[!] Target tidak dapat dijangkau: {e}{Style.RESET_ALL}")
        return None


def run():
    print(f"{Fore.CYAN}[*] WebShell Finder — Filename Enumeration{Style.RESET_ALL}")
    target = input("URL target (https://example.com): ").strip()
    if not target:
        print(f"{Fore.RED}[!] URL kosong.{Style.RESET_ALL}")
        return
    if not target.startswith("http"):
        target = "https://" + target

    names = list(DEFAULT_NAMES)
    wordlist = next((w for w in WORDLISTS if os.path.exists(w)), None)
    if wordlist:
        with open(wordlist, "r", errors="ignore") as f:
            names += [line.strip() for line in f if line.strip()]
        print(f"{Fore.YELLOW}[*] Wordlist dimuat ({wordlist}): {len(names)} nama{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}[*] Wordlist tidak ada, pakai default: {len(names)} nama{Style.RESET_ALL}")

    threads = int(input("Threads [default 20]: ").strip() or 20)

    baseline = get_baseline(target)
    if baseline is None:
        return
    soft_404 = baseline.status_code == 200
    if soft_404:
        print(f"{Fore.YELLOW}[*] Baseline soft-404: {baseline.status_code} ({len(baseline.content)} bytes){Style.RESET_ALL}")

    found = []

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(check_file, target, n): n for n in names}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                status, url, size = res
                if soft_404 and status == 200 and size == len(baseline.content):
                    continue
                print(f"{Fore.GREEN}[{status}] {url} ({size} bytes){Style.RESET_ALL}")
                found.append((status, url))

    print(f"\n{Fore.GREEN}[+] Selesai. Ditemukan {len(found)} hasil.{Style.RESET_ALL}")
    if found:
        os.makedirs("results", exist_ok=True)
        with open("results/webshell_names.txt", "w") as f:
            for s, u in found:
                f.write(f"{s}\t{u}\n")
        print(f"{Fore.GREEN}[+] Disimpan ke results/webshell_names.txt{Style.RESET_ALL}")
