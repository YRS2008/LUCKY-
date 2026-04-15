import socket
import re
import time

def solve():
    host = '154.57.164.66'
    port = 30303

    # Serverga ulanish
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((host, port))
        s.settimeout(5)
        
        def recv_until(target):
            data = ""
            while target not in data:
                try:
                    chunk = s.recv(1).decode('utf-8', errors='ignore')
                    if not chunk:
                        break
                    data += chunk
                except:
                    break
            return data

        # O'yinni boshlash
        print("[+] Serverga ulanildi. O'yin boshlanmoqda...")
        recv_until("> ")
        s.sendall(b"1\n")

        for r in range(100):
            data = recv_until("Who wins this round?")
            
            # O'yinchilarning ballarini yig'ish
            player_data = re.findall(r"Player (\d+): ([\d\s]+)", data)
            
            dice_sum = {}
            for p_num, p_dices in player_data:
                total = sum(map(int, p_dices.strip().split()))
                dice_sum[int(p_num)] = total

            # G'olibni aniqlash (durang bo'lsa oxirgi o'yinchi yutadi)
            max_score = -1
            winner = -1
            for p_id in sorted(dice_sum.keys()):
                if dice_sum[p_id] >= max_score:
                    max_score = dice_sum[p_id]
                    winner = p_id

            # Javobni yuborish
            recv_until("> ")
            s.sendall(f"{winner}\n".encode())
            
            if (r + 1) % 10 == 0:
                print(f"[#] Round {r+1} tugadi...")

        # Flagni olish qismi
        print("[!] Barcha raundlar tugadi. Flag kutilmoqda...")
        
        # Serverga javobni shakllantirish uchun vaqt beramiz
        time.sleep(2)
        
        # Barcha qolgan ma'lumotlarni o'qiymiz
        final_output = ""
        s.settimeout(3)
        while True:
            try:
                chunk = s.recv(4096).decode('utf-8', errors='ignore')
                if not chunk:
                    break
                final_output += chunk
            except:
                break

        print("\n" + "="*40)
        print("SERVER JAVOBI:")
        print(final_output.strip())
        print("="*40)

    except Exception as e:
        print(f"[X] Xatolik: {e}")
    finally:
        s.close()

if __name__ == "__main__":
    solve()
