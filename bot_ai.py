import telebot
from openai import OpenAI
import traceback

TOKEN = 'YOUR_BOT_TOKEN'
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"
bot = telebot.TeleBot(TOKEN)
client = OpenAI(api_key=OPENAI_API_KEY)

def local_fallback_response(text):
    text = text.lower()
    if "hello" in text:
        return "Hey there! How can I help you?"
    elif "how are you" in text:
        return "I'm just code, but feeling helpful!"
    else:
        return "AI is currently unavailable or API key is missing. Please try again later."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    try:
        if not OPENAI_API_KEY:
            raise ValueError("Missing OpenAI API key.")

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            max_tokens=150,
            temperature=0.7,
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        print("OpenAI API error:")
        traceback.print_exc()
        answer = local_fallback_response(user_text)

    bot.reply_to(message, answer)

bot.polling(none_stop=True)