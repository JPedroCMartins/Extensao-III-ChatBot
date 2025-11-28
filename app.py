import logging
from telegram import Update, ReplyKeyboardMarkup
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
        ["Cursos", "Horários de Atendimento"],
        ["Agendamento", "Consultar Vagas"],
        ["Pré-inscrição", "Tira Dúvidas"]
    ]
    
    markup = ReplyKeyboardMarkup(teclado, resize_keyboard=True)
    
    await update.message.reply_text(
        "Olá! 👋 Sou seu assistente virtual. Escolha uma opção abaixo para começar:",
        reply_markup=markup
    )

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    texto = update.message.text.strip()
    resposta = ""

    if texto == "Cursos":
        resposta = (
            "Aqui estão nossos cursos disponíveis:\n\n"
            "📚 Informática Básica\n"
            "   - Domine as ferramentas fundamentais para o mercado de trabalho e uso pessoal.\n\n"
            "🌐 Informática Avançada\n"
            "   - Eleve seu nível com manutenção de computadores, configurações de rede e softwares complexos.\n\n"
        )
        
    elif texto == "Horários de Atendimento":
        resposta = (
            "Nosso horário de atendimento é:\n\n"
            "Segunda a Sexta: 07:00 às 17:00\n"
            "Sábado: 07:00 às 12:00\n"
            "Domingo: Fechado"
        )
        
    elif texto == "Agendamento":
        resposta = (
            "Para agendar um atendimento, você pode:\n\n"
            "1. Ligar para: (99) 99999-9999\n"
            "2. Acessar nosso site: DESENVOLVIMENTO"
        )
        
    elif texto == "Consultar Vagas":
        resposta = (
            "As vagas para os cursos abrem todo início de semestre.\n\n"
            "Você pode verificar a disponibilidade atual e a lista de espera "
            "diretamente na página de cada curso em nosso site: \n"
            "DESENVOLVIMENTO"
        )
        
    elif texto == "Pré-inscrição":
        resposta = (
            "Interessado em nossos cursos? Faça sua pré-inscrição "
            "para ser notificado quando novas turmas abrirem!\n\n"
            "Acesse: DESENVOLVIMENTO"
        )
        
    elif texto == "Tira Dúvidas":
        resposta = (
            "**Perguntas Frequentes:**\n\n"
            
            "**1. Os cursos são gratuitos?**\n"
            "   - Sim. Todos os cursos oferecidos são gratuitos. O que pode ser solicitado é o material de uso pessoal para aulas práticas, dependendo do curso.\n\n"
            
            "**2. Como faço para me inscrever?**\n"
            "   - As inscrições são online, através de Editais. É preciso ter um cadastro no 'Portal do Candidato' e depois usar o 'Portal de Inscrição' dentro do prazo do edital.\n\n"
            
            "**3. Posso me inscrever em mais de um curso ao mesmo tempo?**\n"
            "   - Geralmente não. A instituição costuma permitir apenas uma inscrição por pessoa em cada processo seletivo para garantir mais oportunidades a todos.\n\n"
            
            "**4. Quais são os pré-requisitos?**\n"
            "   - Os pré-requisitos (idade mínima e escolaridade) mudam para cada curso e estão sempre descritos no edital de abertura de vagas.\n\n"
            
            "**5. Como pego meu certificado ao terminar?**\n"
            "   - Você deve procurar a secretaria da unidade onde realizou o curso para obter as informações sobre a emissão e entrega do seu Certificado ou Diploma."
        )
        
    else:
        resposta = (
            "Desculpe, não entendi essa opção. 🤔\n"
            "Por favor, escolha um dos botões do menu. "
            "Se o menu sumiu, digite /start para exibi-lo novamente."
        )

    await update.message.reply_text(resposta)

def main():
    
    if not TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN não encontrado. Verifique seu arquivo .env ou variáveis de ambiente.")
        return

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

    logger.info("Bot rodando... Pressione Ctrl+C para parar.")

    app.run_polling()

if __name__ == "__main__":
    main()