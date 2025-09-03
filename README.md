# 🏠 Homelab — Mojodomowo

Projekt **homelab_mojodomowo** to mój własny serwer domowy, który pełni rolę centrum usług sieciowych i multimedialnych.  
Celem jest nauka, automatyzacja i centralizacja usług w jednej, spójnej infrastrukturze działającej w sieci domowej.

---

## ✨ Funkcje i usługi

🔒 **PiVPN (WireGuard/OpenVPN)**  
- Dostęp VPN do sieci domowej z dowolnego miejsca  
- Bezpieczne połączenie szyfrowane  
- Izolacja użytkowników oraz możliwość zarządzania kluczami  

🕳️ **Pi-hole**  
- Blokowanie reklam, trackerów i niechcianych domen w całej sieci  
- Integracja z własnym DNS  
- Panel webowy do monitoringu zapytań DNS  

💾 **OpenMediaVault (OMV)**  
- Serwer plików i multimediów (NAS)  
- Obsługa SMB/NFS/FTP  
- Wsparcie dla dysków sieciowych i macierzy RAID  

⚙️ **Inne usługi** *(opcjonalnie)*  
- Serwer gier / aplikacji  
- Monitorowanie sieci i urządzeń (np. Grafana/Prometheus)  
- Automatyzacja zadań i skrypty systemowe  

---

## 🛠️ Wykorzystany sprzęt

- Raspberry Pi 3/4/5  
- Dysk zewnętrzny USB 1–2 TB  
- Router Mikrotik (z obsługą VLAN i DHCP)  
- Zasilacz UPS (opcjonalnie, dla stabilności)  

---

## 📦 Instalacja

1. **Przygotowanie systemu**
   - Instalacja systemu Linux (np. Raspberry Pi OS / Debian / openSUSE)  
   - Aktualizacja pakietów:
     ```bash
     sudo apt update && sudo apt upgrade -y
     ```

2. **Instalacja PiVPN**
   ```bash
   curl -L https://install.pivpn.io | bash
