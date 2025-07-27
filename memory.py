import json
import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
from dotenv import load_dotenv


load_dotenv()  # Carica le variabili dal .env

bot_token = os.getenv("TOKEN")
admin_id = os.getenv("ADMIN_USER_ID")


TOKEN = bot_token
FILE_PLAYERS = "players.json"
FILE_REGISTERED = "registered_users.json"
ADMIN_USER_ID = admin_id


# Carica i dati nei file JSON
def load_registered_users():
    try:
        with open(FILE_REGISTERED, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
def load_player_tags():
    try:
        with open(FILE_PLAYERS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

#ricarica file    
def reload_data():
    global REGISTERED_USERS, PLAYER_TAGS
    REGISTERED_USERS = load_registered_users()
    PLAYER_TAGS = load_player_tags() 

# carica i tag e id all'avvio
PLAYER_TAGS = load_player_tags()
REGISTERED_USERS = load_registered_users()


# Salva i dati nel file JSON
def save_registered_users(data):
    with open(FILE_REGISTERED, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def save_player_tags(tags):
    with open(FILE_PLAYERS, "w", encoding="utf-8") as f:
        json.dump(tags, f, indent=2, ensure_ascii=False)


# ascolto dei messaggi
async def auto_register_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reload_data()
    user = update.effective_user
    name = user.full_name
    user_id = str(user.id)

    if user_id not in REGISTERED_USERS:
        REGISTERED_USERS[user_id] = name
        save_registered_users(REGISTERED_USERS)
        print(f"✅ Registrato automaticamente: {user_id} -> {name}")

# register
async def register(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reload_data()
    user = update.effective_user
    user_id = str(user.id)
    name = user.full_name

    if user_id in REGISTERED_USERS:
        await update.message.reply_text("✅ Sei già registrato.")
        return

    REGISTERED_USERS[user_id] = name
    save_registered_users(REGISTERED_USERS)

    await update.message.reply_text(f"🔐 Registrazione completata!\n nome: {name}\n id: {user_id}")

# link
async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_USER_ID):
        await update.message.reply_text("⛔ Solo l'amministratore può usare questo comando.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("❌ Usa il comando così: /link user_id nickname")
        return

    user_id = context.args[0]
    nickname = context.args[1].lower()

    if user_id not in REGISTERED_USERS:
        await update.message.reply_text("❌ Questo ID utente non è registrato.")
        return

    if nickname in PLAYER_TAGS:
        if PLAYER_TAGS[nickname] == user_id:
            await update.message.reply_text(f"ℹ️ Il nickname '{nickname}' è già collegato al tuo ID.")
            return
        else:
            await update.message.reply_text(f"⚠️ Il nickname '{nickname}' è già collegato a un altro utente.")
            return

    PLAYER_TAGS[nickname] = user_id
    save_player_tags(PLAYER_TAGS)
    await update.message.reply_text(f"✅ Il nickname '{nickname}' è stato collegato all'ID Telegram {user_id}.")



# Converte un nickname in una regex flessibile che accetta lettere ripetute es: 'ahccu' -> a+h+c+c+u+
def nickname_to_fuzzy_regex(nickname):

    return ''.join(f"{re.escape(char)}+" for char in nickname)

# tagga
async def check_mentions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    reload_data()

    if not context.args:
        await update.message.reply_text("❗ Usa il comando così: /tagga messaggio_da_controllare")
        return

    message_text = " ".join(context.args).lower()
    mentioned = []

    for nickname, user_id in PLAYER_TAGS.items():
        fuzzy_pattern = nickname_to_fuzzy_regex(nickname.lower())
        if re.search(rf"\b{fuzzy_pattern}\b", message_text):
            name = REGISTERED_USERS.get(user_id, "Utente")
            mention = f"[{name}](tg://user?id={user_id})"
            mentioned.append(mention)

    if mentioned:
        response = "👀 Sono stati nominati in chat i seguenti giocatori:\n" + "\n".join(set(mentioned))
    else:
        response = "✅ Nessun giocatore menzionato nel messaggio."

    await update.message.reply_text(response, parse_mode="Markdown")



# syncname user_id
async def sync_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_USER_ID):
        await update.message.reply_text("⛔ Solo l'amministratore può usare questo comando.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("❌ Usa il comando così: /syncname user_id")
        return

    target_id = context.args[0]

    if target_id not in REGISTERED_USERS:
        await update.message.reply_text("❌ Utente non registrato.")
        return

    try:
        user = await context.bot.get_chat(int(target_id))
        nuovo_nome = user.full_name
        vecchio_nome = REGISTERED_USERS[target_id] 

        REGISTERED_USERS[target_id] = nuovo_nome
        save_registered_users(REGISTERED_USERS)

        await update.message.reply_text(
            f"🔁 Nome aggiornato per l'utente {target_id}:\n"
            f"Vecchio nome: '{vecchio_nome}'\n"
            f"Nuovo nome: '{nuovo_nome}'"
        )

    except Exception as e:
        await update.message.reply_text(f"⚠️ Impossibile ottenere informazioni sull'utente. Errore: {e}")





# update
async def update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_USER_ID):
        await update.message.reply_text("⛔ Solo l'amministratore può usare questo comando.")
        return

    if len(context.args) != 2:
        await update.message.reply_text("❌ Usa il comando così: /update user_id nuovo_nick")
        return

    user_id = context.args[0]
    nuovo_nick = context.args[1].lower()

    if user_id not in REGISTERED_USERS:
        await update.message.reply_text("⚠️ Questo ID non è registrato.")
        return

    # Cerca vecchio nickname per questo user_id (se presente)
    vecchio_nick = None
    for k, v in PLAYER_TAGS.items():
        if v == user_id:
            vecchio_nick = k
            break

    # Rimuove vecchie associazioni per quell'ID
    to_remove = [k for k, v in PLAYER_TAGS.items() if v == user_id]
    for k in to_remove:
        del PLAYER_TAGS[k]

    # Aggiorna con il nuovo nickname
    PLAYER_TAGS[nuovo_nick] = user_id
    save_player_tags(PLAYER_TAGS)

    if vecchio_nick:
        await update.message.reply_text(f"✅ Nickname Clash aggiornato:\nDa '{vecchio_nick}' a '{nuovo_nick}'")
    else:
        await update.message.reply_text(f"✅ Nickname Clash impostato a '{nuovo_nick}' per l'ID {user_id}")

#remove
async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_USER_ID):
        await update.message.reply_text("⛔ Solo l'amministratore può usare questo comando.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("❌ Usa il comando così: /remove user_id")
        return

    user_id = context.args[0]

    # Rimuovi utente da REGISTERED_USERS
    if user_id in REGISTERED_USERS:
        del REGISTERED_USERS[user_id]
        save_registered_users(REGISTERED_USERS)
    else:
        await update.message.reply_text("⚠️ Questo ID non è registrato.")
        return

    # Rimuovi nickname associati in PLAYER_TAGS
    to_remove = [nick for nick, uid in PLAYER_TAGS.items() if uid == user_id]
    for nick in to_remove:
        del PLAYER_TAGS[nick]
    save_player_tags(PLAYER_TAGS)

    await update.message.reply_text(f"✅ Eliminati registrazione e nickname per l'ID Telegram {user_id}.")

# search
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_USER_ID):
        await update.message.reply_text("⛔ Solo l'amministratore può usare questo comando.")
        return

    if len(context.args) != 1:
        await update.message.reply_text("❌ Usa il comando così: /search nome")
        return

    query = context.args[0].lower()
    risultati = []

    # Primo ciclo: cerca per nome Telegram
    for user_id, nome_tg in REGISTERED_USERS.items():
        if query in nome_tg.lower():
            # Cerca nickname Clash associato all'id
            nick_clash = None
            for nick, uid in PLAYER_TAGS.items():
                if uid == user_id:
                    nick_clash = nick
                    break
            if nick_clash:
                risultati.append(f"Clash: {nick_clash} |TG: {nome_tg} | ID: {user_id}")
            else:
                risultati.append(f"Clash: {nick_clash} |TG: {nome_tg} | ID: {user_id}")

    # Se non ho trovato nulla nel primo ciclo, cerco nel secondo
    if not risultati:
        for nick_clash, user_id in PLAYER_TAGS.items():
            if query == nick_clash.lower():
                nome_tg = REGISTERED_USERS.get(user_id, "Nome TG non trovato")
                risultati.append(f"Clash: {nick_clash} |TG: {nome_tg} | ID: {user_id}")

    if risultati:
        await update.message.reply_text("🔍 Risultati ricerca:\n" + "\n".join(risultati))
    else:
        await update.message.reply_text("❌ Nessun risultato trovato per: " + query)



# list_players
async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != str(ADMIN_USER_ID):
        await update.message.reply_text("⛔ Solo l'amministratore può usare questo comando.")
        return

    if not REGISTERED_USERS:
        await update.message.reply_text("❌ Nessun utente registrato.")
        return

    lines = []
    for user_id, nome_tg in REGISTERED_USERS.items():
        # Cerca il nick Clash associato
        nick_clash = next((nick for nick, uid in PLAYER_TAGS.items() if uid == user_id), "(non assegnato)")
        lines.append(f"Clash: {nick_clash} |TG: {nome_tg} | ID: {user_id}")

    risposta = "📋 Lista utenti registrati:\n" + "\n".join(lines)
    await update.message.reply_text(risposta)



if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handler comandi
    app.add_handler(CommandHandler("register", register))
    app.add_handler(CommandHandler("link", link))
    app.add_handler(CommandHandler("tagga", check_mentions))
    app.add_handler(CommandHandler("syncname", sync_name))
    app.add_handler(CommandHandler("update", update))
    app.add_handler(CommandHandler("remove", remove))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("listplayers", list_players))

    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), auto_register_user))
 
    print("Bot in esecuzione...")
    app.run_polling()
