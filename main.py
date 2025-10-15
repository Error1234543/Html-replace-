import telebot, re, os

BOT_TOKEN = "8410755411:AAHrIUXUIcCr3lOuBAwMWdfvSgGx9XOR95c"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.reply_to(message, "👋 Send me your HTML file — I'll remove old bot links & replace firephysics → LEARN X PRO ⚡")

@bot.message_handler(content_types=['document'])
def handle_file(message):
    try:
        # Download
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        filename = message.document.file_name
        cleaned_name = "cleaned_" + filename

        with open(filename, "wb") as f:
            f.write(downloaded)

        # Read content
        with open(filename, "r", encoding="utf-8", errors="ignore") as f:
            html = f.read()

        # 🔹 1️⃣ Remove the 3 <a href="..."> Telegram lines
        html = re.sub(
            r'<a href="https://t\.me/(AppxTestRobot|AppxTestSeries|TharkeExtractorRobot)".*?</a>\s*',
            "",
            html,
            flags=re.DOTALL
        )

        # 🔹 2️⃣ Replace firephysics → LEARN X PRO inside that div
        html = re.sub(
            r'(<div class="app-name-box mb-2">)\s*firephysics\s*(</div>)',
            r'\1LEARN X PRO\2',
            html,
            flags=re.IGNORECASE
        )

        # Write new cleaned file
        with open(cleaned_name, "w", encoding="utf-8") as f:
            f.write(html)

        # Send back result
        with open(cleaned_name, "rb") as f:
            bot.send_document(
                message.chat.id,
                f,
                caption="✅ Done! Old bot links removed & firephysics → LEARN X PRO replaced 🔥"
            )

        os.remove(filename)
        os.remove(cleaned_name)

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {e}")

print("🤖 Sonic HTML Replacer is running...")
bot.infinity_polling()
