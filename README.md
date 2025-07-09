# 🧠 memoryTagBot – Telegram Tagging Assistant

Un semplice bot Telegram scritto in Python che rileva automaticamente la presenza di determinati nomi nei messaggi e restituisce i relativi tag configurati, utile per coordinare squadre, clan o gruppi di gioco.

---

## 🚀 Funzionalità principali

- 📥 **Aggiunta giocatori:** aggiungi un giocatore con il suo tag (es. @username).
- ♻️ **Aggiorna giocatori:** modifica il tag di un giocatore esistente.
- ❌ **Rimuovi giocatori:** rimuovi un giocatore registrato.
- 📋 **Lista giocatori:** visualizza tutti i giocatori registrati.
- 🕵️ **Controllo messaggi:** verifica se un messaggio contiene uno o più nomi registrati.
- 🤖 **Ascolto automatico:** (facoltativo) monitora ogni messaggio nella chat e tagga i giocatori se nominati.

---

## 🛠️ Requisiti

- Python 3.10 o superiore
- Un bot Telegram (puoi crearlo tramite [@BotFather](https://t.me/BotFather))
- Librerie Python:
  - `python-telegram-bot>=20.0`

---

## 📦 Installazione locale con Visual Studio Code

1. **Clona il repository**

   ```bash
   git clone https://github.com/VittorioGuida15/memoryTagBot.git
   cd memoryTagBot
