"""Menu 12 — Mini Shell FTP Client"""
import os
import ftplib
from colorama import Fore, Style


def connect(host, port, tls, user, password):
    try:
        ftp = ftplib.FTP_TLS() if tls else ftplib.FTP()
        ftp.connect(host, port, timeout=15)
        ftp.login(user, password)
        if tls:
            ftp.prot_p()
        return ftp
    except Exception as e:
        print(f"{Fore.RED}[!] Gagal konek/login: {e}{Style.RESET_ALL}")
        return None


def handle(cmd, ftp):
    parts = cmd.split()
    op = parts[0].lower()
    arg = parts[1] if len(parts) > 1 else None
    arg2 = parts[2] if len(parts) > 2 else None

    try:
        if op in ("exit", "quit", "bye"):
            ftp.quit()
            return False
        elif op == "help":
            print("Perintah: ls | pwd | cd <dir> | get <remote> [lokal] | put <lokal> [remote]")
            print("          mkdir <dir> | rm <file> | rmdir <dir> | size <file> | exit")
        elif op == "ls":
            for name in ftp.nlst():
                print(f"    {name}")
        elif op == "pwd":
            print(f"    {ftp.pwd()}")
        elif op == "cd":
            ftp.cwd(arg)
        elif op == "get":
            local = arg2 or os.path.basename(arg)
            with open(local, "wb") as f:
                ftp.retrbinary(f"RETR {arg}", f.write)
            print(f"{Fore.GREEN}[+] Tersimpan: {local}{Style.RESET_ALL}")
        elif op == "put":
            remote = arg2 or os.path.basename(arg)
            with open(arg, "rb") as f:
                ftp.storbinary(f"STOR {remote}", f)
            print(f"{Fore.GREEN}[+] Terupload: {remote}{Style.RESET_ALL}")
        elif op == "mkdir":
            ftp.mkd(arg)
        elif op == "rm":
            ftp.delete(arg)
        elif op == "rmdir":
            ftp.rmd(arg)
        elif op == "size":
            print(f"    {arg}: {ftp.size(arg)} bytes")
        else:
            print(f"{Fore.YELLOW}[?] Perintah tidak dikenal. Ketik 'help'.{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}[!] Error: {e}{Style.RESET_ALL}")
    return True


def run():
    print(f"{Fore.CYAN}[*] Mini Shell FTP Client{Style.RESET_ALL}")
    host = input("Host (IP / domain): ").strip()
    if not host:
        print(f"{Fore.RED}[!] Host kosong.{Style.RESET_ALL}")
        return
    port = int(input("Port [21]: ").strip() or 21)
    tls = input("Pakai FTPS? [y/N]: ").strip().lower() == "y"
    user = input("Username: ").strip()
    password = input("Password: ").strip()

    ftp = connect(host, port, tls, user, password)
    if ftp is None:
        return
    print(f"{Fore.GREEN}[+] Terhubung. Ketik 'help' untuk daftar perintah.{Style.RESET_ALL}")

    try:
        while True:
            cmd = input(f"{Fore.CYAN}ftp> {Style.RESET_ALL}").strip()
            if not cmd:
                continue
            if not handle(cmd, ftp):
                break
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[!] Putus.{Style.RESET_ALL}")
        try:
            ftp.quit()
        except Exception:
            pass
    print(f"{Fore.YELLOW}[+] Koneksi ditutup.{Style.RESET_ALL}")
