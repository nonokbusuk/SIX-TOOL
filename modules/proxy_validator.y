"""Menu 13 — Mass Proxy Validator"""
import os
import requests
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

TEST_URL = "http://httpbin.org/ip"


def check_proxy(proxy):
    try:
        r = requests.get(TEST_URL, proxies={"http": proxy, "https": proxy}, timeout=10)
        if r.status_code == 200:
            return (proxy, r.json().get("origin", "?"))
    except Exception:
        pass
    return None


def run():
    print(f"{Fore.CYAN}[*] Mass Proxy Validator{Style.RESET_ALL}")
    print("Format: ip:port (satu per baris). Kosongkan 2x untuk selesai.")
    proxies = []
    while True:
        line = input("> ").strip()
        if not line:
            break
        proxies.append(line)

    if not proxies:
        print(f"{Fore.RED}[!] Tidak ada proxy.{Style.RESET_ALL}")
        return

    threads = int(input("Threads [default 20]: ").strip() or 20)
    valid = []

    with ThreadPoolExecutor(max_workers=threads) as ex:
        futures = {ex.submit(check_proxy, p): p for p in proxies}
        for fut in as_completed(futures):
            res = fut.result()
            if res:
                proxy, ip = res
                print(f"{Fore.GREEN}[+] VALID: {proxy} -> {ip}{Style.RESET_ALL}")
                valid.append(proxy)
            else:
                print(f"{Fore.RED}[-] INVALID: {futures[fut]}{Style.RESET_ALL}")

    print(f"\n{Fore.GREEN}[+] Total valid: {len(valid)}{Style.RESET_ALL}")
    if valid:
        os.makedirs("results", exist_ok=True)
        with open("results/valid_proxies.txt", "w") as f:
            f.write("\n".join(valid))
        print(f"{Fore.GREEN}[+] Disimpan ke results/valid_proxies.txt{Style.RESET_ALL}")
