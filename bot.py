# bot.py
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import sqlite3

TOKEN = "8414835179:AAEc-kgKhnsjNpxsVJiwcpTpJFTtAME0go4"
DB_FILE = "bot.db"

# Dicionário temporário para armazenar matrícula do usuário durante a sessão
usuarios_sessao = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Olá! Por favor, digite sua matrícula para acessar suas informações:")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = update.message.from_user.id
    texto = update.message.text.strip()

    if telegram_id not in usuarios_sessao:
        # Primeira mensagem após /start: matrícula
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, nome FROM usuarios WHERE matricula=?", (texto,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            usuarios_sessao[telegram_id] = resultado[0]  # salva user_id
            user_id, nome = resultado
            # Mostra menu
            teclado = [["Cursos oferecidos"], ["Minhas notas"], ["Ajuda"]]
            markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True, one_time_keyboard=True)
            await update.message.reply_text(f"Bem-vindo, {nome}! Escolha uma opção:", reply_markup=markup)
        else:
            await update.message.reply_text("Matrícula não encontrada. Por favor, tente novamente:")
    else:
        # Usuário já está logado, mostra as opções
        user_id = usuarios_sessao[telegram_id]

        if texto == "Cursos oferecidos":
            await update.message.reply_text("Cursos disponíveis:\n- Matemática\n- Física\n- Programação")
        elif texto == "Minhas notas":
            conn = sqlite3.connect(DB_FILE)
            cursor = conn.cursor()
            cursor.execute("SELECT disciplina, nota FROM notas WHERE user_id=?", (user_id,))
            notas = cursor.fetchall()
            conn.close()

            if notas:
                resposta = "\n".join([f"{disciplina}: {nota}" for disciplina, nota in notas])
            else:
                resposta = "Você ainda não tem notas cadastradas."
            await update.message.reply_text(resposta)
        elif texto == "Ajuda":
            await update.message.reply_text("Digite /start para reiniciar o menu ou contate o suporte.")
        else:
            await update.message.reply_text("Opção inválida. Escolha uma das opções do menu.")

# Inicialização do bot
app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("Bot rodando...")
app.run_polling()
