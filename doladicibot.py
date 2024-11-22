import logging
import re
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Bot token
API_TOKEN = '7096528299:AAGetLzc8YYZ9jnhm7UPKLShq_PZYtnaJcE'

# Bot için logging ayarları
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Şüpheli kelimeler listesi
suspicious_keywords = [
    "şifre", "para", "yatırım", "hediye", "acil", "sahtelik", "scam", "dolandırıcı", "bilgini", "yönetim",
    "gönder", "acil yardım", "kart", "kazan", "yurtdışı", "belge", "ödül", "artık", "fırsat", "ödeme"
]

# Basit yapay zeka ile mesaj analizi
def simple_ai_analysis(message: str) -> bool:
    """
    Mesajda şüpheli kelimeleri kontrol eder ve şüpheli olup olmadığına karar verir.
    """
    for keyword in suspicious_keywords:
        if re.search(rf"\b{keyword}\b", message, re.IGNORECASE):  # Kelime tam eşleşmesi arıyoruz
            return True
    return False

# Kullanıcı mesajını alıp analiz etme fonksiyonu
async def handle_message(update: Update, context: CallbackContext) -> None:
    if update.message is None:
        return  # Mesaj yoksa işleme

    message = update.message.text
    user = update.message.from_user
    user_name = user.username if user.username else "No Username"
    user_id = user.id  # Kullanıcı ID'si
    user_first_name = user.first_name  # Kullanıcı adı
    user_last_name = user.last_name if user.last_name else "No Last Name"

    # Şüpheli mesajı analiz et ve tespit et
    if simple_ai_analysis(message):
        # Dolandırıcı mesajı tespit etme
        text = f"**Dolandırıcı Tespiti**\n\n@{user_name} ({user_first_name} {user_last_name}) tespit edildi.\n\n" \
               f"Mesaj: {message}\n\nKullanıcı ID: {user_id}\n\nCezası: **Kontrol Ediliyor...**"

        # Kullanıcıyı uyar
        await update.message.reply_text(f"{user_name} adlı kullanıcı şüpheli olarak tespit edildi. ")

        # Grupta mesaj gönder
        await update.message.reply_text("Bu kullanıcı hakkında adminler işlem yapacaktır eğer dolandırıcı değilse kaldırılacaktır. Dolandırıcı olarak şikayet edilen kişi burada @VirtualScammers")

        # @VirtualScammers kanalına bildirim gönder
        channel_id = "@VirtualScammers"
        await context.bot.send_message(chat_id=channel_id, text=text)

        # Gruptan mesajları silme
        await update.message.delete()

        # Grupta "Dolandırıcı Burada @VirtualScammers" mesajını gönder
        await context.bot.send_message(chat_id=update.message.chat_id, text="")

# Yardım komutu
async def help_command(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Bu bot, şüpheli mesajları analiz eder ve dolandırıcıları raporlar.")

# Hata işleyici
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning(f"Update {update} caused error {context.error}")

def main():
    # Telegram API ile bağlanma
    application = Application.builder().token(API_TOKEN).build()

    # Dispatcher ve handler'ları ayarlama
    application.add_handler(CommandHandler("help", help_command))  # Yardım komutunu ekledik
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Botu çalıştırma
    application.run_polling()

if __name__ == '__main__':
    main()
