# memoryTagBot – Telegram Tagging Assistant

Un semplice bot Telegram scritto in Python che rileva automaticamente la presenza di determinati nomi nei messaggi e restituisce i relativi tag configurati, utile per coordinare squadre, clan o gruppi di gioco.

---

##  Funzionalità principali

-  **Aggiunta giocatori:** aggiungi un giocatore con il suo tag (es. @username).
-  **Aggiorna giocatori:** modifica il tag di un giocatore esistente.
-  **Rimuovi giocatori:** rimuovi un giocatore registrato.
-  **Lista giocatori:** visualizza tutti i giocatori registrati.
-  **Controllo messaggi:** verifica se un messaggio contiene uno o più nomi registrati.
-  **Ascolto automatico:** (facoltativo) monitora ogni messaggio nella chat e tagga i giocatori se nominati.

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
    python memory.py
