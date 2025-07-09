import json
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

TOKEN = "8135909690:AAGMgtdO6w71UyCewgSc3qnMxC_0RAqTdMU"
FILE_PLAYERS = "players.json"

# Carica i dati dal file JSON
def load_player_tags():
    try:
        with open(FILE_PLAYERS, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Salva i dati nel file JSON
def save_player_tags(tags):
    with open(FILE_PLAYERS, "w", encoding="utf-8") as f:
        json.dump(tags, f, indent=2, ensure_ascii=False)

# carica i tag all'avvio
PLAYER_TAGS = load_player_tags()

# ascolto dei messaggi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    message_text = update.message.text.lower()
    mentioned = []

    for name, tag in PLAYER_TAGS.items():
        if name in message_text:
            mentioned.append(tag)

    if mentioned:
        response = "Sono stati nominati in chat i seguenti giocatori: " + ", ".join(set(mentioned))
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


# comando /tagga
async def check_mentions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❗ Usa il comando così: /tagga messaggio_da_controllare")
        return

    message_text = " ".join(context.args).lower()
    mentioned = []

    for name, tag in PLAYER_TAGS.items():
        if name in message_text:
            mentioned.append(tag)

    if mentioned:
        response = "👀 Sono stati nominati in chat i seguenti giocatori: " + ", ".join(set(mentioned))
    else:
        response = "✅ Nessun giocatore menzionato nel messaggio."

    await update.message.reply_text(response)


def add_new_player(name: str, tag: str) -> bool:
    """
    Aggiunge un nuovo giocatore se non esiste.
    Ritorna True se aggiunto, False se già esiste.
    """
    if name in PLAYER_TAGS:
        return False
    PLAYER_TAGS[name] = tag
    save_player_tags(PLAYER_TAGS)
    return True

def update_existing_player(name: str, tag: str) -> bool:
    """
    Aggiorna il tag di un giocatore esistente.
    Ritorna True se aggiornato, False se non esiste.
    """
    if name not in PLAYER_TAGS:
        return False
    PLAYER_TAGS[name] = tag
    save_player_tags(PLAYER_TAGS)
    return True


# aggiungi tag
async def add_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("❌ Usa il comando così: /addplayer nome tag (es: /addplayer marco @marco123)")
        return

    name = context.args[0].lower()
    tag = context.args[1]

    if not tag.startswith("@"):
        await update.message.reply_text("⚠️ Il tag deve iniziare con '@' (es: @marco123).")
        return

    # Se il giocatore è già presente blocchiamo l'aggiunta
    if not add_new_player(name, tag):
        await update.message.reply_text(f"❌ Giocatore '{name}' è già presente con tag '{PLAYER_TAGS[name]}'. Usa /updateplayer per modificarlo.")
        return

    await update.message.reply_text(f"✅ Giocatore '{name}' aggiunto con tag '{tag}'!")

#aggiorna tag
async def update_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("❌ Usa il comando così: /updateplayer nome tag (es: /updateplayer marco @marco123)")
        return

    name = context.args[0].lower()
    tag = context.args[1]

    if not tag.startswith("@"):
        await update.message.reply_text("⚠️ Il tag deve iniziare con '@' (es: @marco123).")
        return

    # Proviamo ad aggiornare
    if update_existing_player(name, tag):
        await update.message.reply_text(f"🔁 Giocatore '{name}' aggiornato con nuovo tag '{tag}'!")
    else:
        await update.message.reply_text(f"❌ Giocatore '{name}' non trovato. Usa /addplayer per aggiungerlo.")


# rimuovi tag
async def remove_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ Usa il comando così: /removeplayer nome")
        return

    name = context.args[0].lower()

    if name in PLAYER_TAGS:
        removed_tag = PLAYER_TAGS.pop(name)
        save_player_tags(PLAYER_TAGS)
        await update.message.reply_text(f"🗑️ Giocatore '{name}' con tag '{removed_tag}' è stato rimosso!")
    else:
        await update.message.reply_text(f"⚠️ Nessun giocatore con nome '{name}' trovato.")

        

# lista dei giocatori
async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not PLAYER_TAGS:
        await update.message.reply_text("📭 Nessun giocatore registrato al momento.")
        return

    lines = ["📋 Giocatori registrati:"]
    for name, tag in PLAYER_TAGS.items():
        lines.append(f"- {name}: {tag}")

    await update.message.reply_text("\n".join(lines))



if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Handler comandi
    app.add_handler(CommandHandler("addplayer", add_player))
    app.add_handler(CommandHandler("tagga", check_mentions))
    app.add_handler(CommandHandler("removeplayer", remove_player))
    app.add_handler(CommandHandler("listplayers", list_players))
    app.add_handler(CommandHandler("updateplayer", update_player))



    
    #app.add_handler(MessageHandler(filters.TEXT, handle_message))
    #app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
     
    print("Bot in esecuzione...")
    app.run_polling()
