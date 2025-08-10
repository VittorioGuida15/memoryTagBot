# memoryTagBot

Un semplice bot Telegram scritto in Python che facilita la menzione automatica dei membri di un gruppo Telegram a partira da dei nickname assegnati ad essi.

---

# Flusso di esecuzione
**Il funzionamento avviene in tre fasi principali:**

1. Fase di registrazione ID

    - All’avvio, il bot monitora i messaggi inviati nel gruppo configurato.
    - Quando un utente scrive un qualsiasi messaggio, il bot registra automaticamente il suo ID Telegram associandolo al nome visualizzato.
    - Questa fase serve per creare un archivio che permetterà di mappare i nomi di gioco con i tag Telegram reali.

2. Fase di collagamento (mappatura nomi)

    - l'amministratore del bot usando il comando /link potrà collegare gli id registrati con un nickname a sua scelta
    - Una volta completato il collegamento, il bot riconoscerà quella persona con il nickname appena inserito.

3. Fase operativa (comando /tagga)

    Per menzionare uno o più utenti, si utilizza il comando:
    
      ```
      /tagga nome1 nome2 nome3
      ```
    *I nomi possono essere scritti in qualsiasi combinazione di maiuscole/minuscole.*
    
    *Il comando funziona anche se il messaggio contiene parole extra, simboli o numeri.*
    *Esempi validi:*
    
     ```
    /tagga Marco Luca Sara
     ```
     ```
    /tagga dhbqw marcooo 123 luCa x_ saraaa
     ```
    *Il bot riconoscerà i nomi presenti nel suo archivio e li menzionerà automaticamente su Telegram.*


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

   ```
   git clone https://github.com/VittorioGuida15/memoryTagBot.git
   cd memoryTagBot
   ```

2. **Configurazione**
Crea il file .env e inserisci il valore delle variabili TOKEN e ADMIN_USER_ID:

   ```
   TOKEN = "TUO_TOKEN_BOT"
   ADMIN_USER_ID = "ID_ADMIN"
   ```
3. **File**
   - Rinomina players.example.json in players.json
   - registered_users.example.json in registered_users.json.

4. **Installa le dipendenze**
    ```
    pip install python-telegram-bot>=20.0
    pip install python-dotenv
    ```
5. **Avvia il bot**
    ```
    python memory.py
    ```
## Deploy su PythonAnywhere
1. **Crea un account su PythonAnywhere.**

2. **Carica i file memory.py, players.json e registered_users.json (vuoti o già popolati) nella tua directory di lavoro.**

3. **Installa le librerie necessarie nella console Bash aperta dal file memory.py:**
    ```   
    pip install python-telegram-bot>=20.0
    ```
4. **Se uilizzi il file .env**
    ```    
    pip install python-dotenv
    ```
5. **Avvia il bot**
    ```
    python3.10 memory.py
    ```


