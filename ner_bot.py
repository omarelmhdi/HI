from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from yt_dlp import YoutubeDL
import os
import logging

# توكن البوت الخاص بك
API_TOKEN = "8001632324:AAGCqAdx54omoZeEywnvLcbGKvOd_PUOaGk"

# إعداد تسجيل الأخطاء
logging.basicConfig(level=logging.DEBUG)
logging.debug("تشغيل البوت...")

# وظيفة البحث وتحويل الأغنية إلى MP3
async def yt_search_mp3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("يرجى كتابة yt + اسم الأغنية (مثل: yt Despacito).")
        return

    # البحث عن الأغنية
    search_query = ' '.join(context.args)
    try:
        # إعداد yt-dlp لتحميل الصوت فقط
        options = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookiefile': 'youtube_cookies.txt',  # ملف الكوكيز
            'ffmpeg_location': 'D:\\ffmpeg-2025-03-27-git-114fccc4a5-essentials_build\\bin'  # مسار FFmpeg
        }
        
        logging.debug(f"بدء البحث عن: {search_query}")
        
        with YoutubeDL(options) as ydl:
            info = ydl.extract_info(f"ytsearch:{search_query}", download=True)
            video_title = info['entries'][0]['title']
            mp3_file = ydl.prepare_filename(info['entries'][0]).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        logging.debug(f"تم التحميل بنجاح: {video_title} -> {mp3_file}")

        # إرسال الملف
        await update.message.reply_text("تم تحويل الأغنية إلى MP3! جاري الإرسال...")
        await update.message.reply_document(document=open(mp3_file, "rb"))

        # تنظيف الملفات
        os.remove(mp3_file)
        logging.debug(f"تم حذف الملف: {mp3_file}")

    except Exception as e:
        logging.error(f"خطأ أثناء البحث أو التحويل: {e}")
        await update.message.reply_text("حدث خطأ أثناء البحث أو التحويل. يرجى المحاولة مرة أخرى لاحقًا.")

# وظيفة بدء البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! اكتب yt + اسم الأغنية لتحميلها بصيغة MP3.")

# إعداد البوت
def main():
    application = ApplicationBuilder().token(API_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("yt", yt_search_mp3))

    logging.debug("البوت جاهز لاستقبال الأوامر...")
    application.run_polling()

if __name__ == '__main__':
    main()
