import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    teclado = [
        ["Educação", "Saúde"],
        ["Atendimentos Especializados", "Documentos e Regras"],
        ["Local e Contato"]
    ]
    
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    
    await update.message.reply_text(
        "Olá! 👋 Bem-vindo ao assistente virtual do *Instituto Semeador*.\n"
        "Aqui você encontra saúde, educação e cidadania de graça.\n\n"
        "Escolha uma opção abaixo para saber mais:",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    texto = update.message.text.strip()
    resposta = ""

    # Opção: EDUCAÇÃO
    if texto == "Educação":
        resposta = (
            "📚 *ÁREA DE EDUCAÇÃO*\n\n"
            "Confira nossos programas educacionais:\n\n"
            "▫️ *Programa Brasil Alfabetizado*\n"
            "▫️ *Reforço Escolar* (1º ao 5º ano)\n"
            "▫️ *EJA* (Fundamental e Médio)"
        )
        
    # Opção: SAÚDE
    elif texto == "Saúde":
        resposta = (
            "🩺 *ATENDIMENTO MÉDICO*\n"
            "_(Necessário agendamento prévio e presencial)_\n\n"
            "Especialidades disponíveis:\n"
            "▫️ Cardiologista\n"
            "▫️ Clínico Geral\n"
            "▫️ Pneumologista\n"
            "▫️ Infectologista\n"
            "▫️ Pediatra\n"
            "▫️ Oftalmologista (Vagas em lista de espera)"
        )
        
    # Opção: ATENDIMENTOS ESPECIALIZADOS
    elif texto == "Atendimentos Especializados":
        resposta = (
            "⚖️ *ATENDIMENTOS ESPECIALIZADOS*\n\n"
            "Oferecemos suporte nas seguintes áreas:\n"
            "▫️ Fisioterapia\n"
            "▫️ Advocacia\n"
            "▫️ Assistência Social\n"
            "▫️ Psicologia"
        )
        
    # Opção: DOCUMENTOS E REGRAS
    elif texto == "Documentos e Regras":
        resposta = (
            "📝 *AGENDAMENTO E DOCUMENTAÇÃO*\n\n"
            "⚠️ *Regras Importantes:*\n"
            "1. A inscrição deve ser feita *pessoalmente* pelo próprio interessado.\n"
            "2. Não é permitido fazer inscrição para terceiros.\n\n"
            "📄 *Documentos Obrigatórios (Originais):*\n"
            "• Identidade (RG)\n"
            "• Comprovante de Residência\n"
            "• Cartão do SUS\n"
            "• Título de Eleitor"
        )
        
    # Opção: LOCAL E CONTATO (Corrigido)
    elif texto == "Local e Contato":
        resposta = (
            "📍 *ONDE ESTAMOS*\n\n"
            "🏢 *Instituto Semeador*\n"
            "Rua Joraci Camargo, Nº 100, Compensa 1\n\n"
            "📞 *Contato:* (92) 99192-6235\n"
            "📷 *Instagram:* @instituto_semeador"
        )
        
    else:
        resposta = (
            "Desculpe, não entendi essa opção. 🤔\n"
            "Por favor, escolha um dos botões do menu.\n"
            "Se o menu sumiu, digite /start para exibi-lo novamente."
        )

    # Envia a resposta. Se houver erro de formatação, o try/except captura para não derrubar o bot
    try:
        await update.message.reply_text(resposta, parse_mode=ParseMode.MARKDOWN)
    except Exception as e:
        logger.error(f"Erro ao enviar mensagem: {e}")
        # Tenta enviar sem formatação caso falhe
        await update.message.reply_text(resposta.replace("*", "").replace("_", ""))

def main():
    
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN não encontrado.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    logger.info("Bot Instituto Semeador rodando... Pressione Ctrl+C para parar.")

    app.run_polling()

if __name__ == "__main__":
    main()