import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from openai import OpenAI

# Cliente OpenAI
client = OpenAI()

# Função para comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Me envie termos financeiros para eu explicar de forma simples!')

# Função para traduzir mensagens
async def traduzir(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente que explica termos financeiros em uma frase curta e simples."
                },
                {
                    "role": "user",
                    "content": f"Explique em UMA frase curta e simples: {update.message.text}"
                }
            ]
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text("Desculpe, ocorreu um erro ao processar sua mensagem.")

def main():
    # Criar aplicação
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()

    # Adicionar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, traduzir))

    # Iniciar o bot
    print("Bot iniciado...")
    application.run_polling()

if __name__ == "__main__":
    main()
