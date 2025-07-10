# memoryIdBot e – Telegram Id Assistant

Un semplice bot Telegram scritto in Python che rileva automaticamente la presenza di determinati nomi nei messaggi e restituisce i relativi id.

---


## Comandi disponibili nel bot:

- /register - Registra il tuo ID Telegram con il tuo nome
- /tagga - Tagga i membri presenti nel messaggio corrente
- /link - Collega un nickname a un ID Telegram (solo admin)
- /syncname - Sincronizza il nome di un utente registrato tramite il suo ID (solo admin)
- /update - Aggiorna il nick di un utente (solo admin)
- /remove - Rimuove un utente dal sistema (solo admin)
- /search - Cerca l'ID di un utente (solo admin)
- /listplayers - Mostra tutti i nickname registrati (solo admin)

---

##  Requisiti

- Python 3.10 o superiore
- Un bot Telegram (puoi crearlo tramite [@BotFather](https://t.me/BotFather))
- Librerie Python:
  - `python-telegram-bot>=20.0`

---

## Installazione locale con Visual Studio Code

1. **Clona il repository**

   ```bash
   git clone https://github.com/VittorioGuida15/memoryTagBot.git
   cd memoryTagBot

2. **Configura il tuo token**
  Apri il file memory.py e sostituisci il valore della variabile TOKEN con quello del tuo bot Telegram:

   ```bash
   TOKEN = "TUO_TOKEN_BOT"

3. **Installa le dipendenze**
    ```bash
    pip install -r requirements.txt  

4. **Avvia il bot**
    ```bash
    python memory.py
    
## Deploy su PythonAnywhere
1. **Crea un account gratuito su PythonAnywhere.**

2. **Carica i file memory.py, players.json (vuoto o già popolato) e requirements.txt nella tua directory di lavoro.**

3. **Installa le librerie necessarie in una console Bash:**
    ```bash    
    pip install --user -r requirements.txt

4. **Avvia il bot**
    ```bash
    python3.10 /home/.../memory/memory.py

