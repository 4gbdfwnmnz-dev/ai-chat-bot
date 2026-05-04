import discord
from discord.ext import commands
import google.generativeai as genai
import json
import os

# 1. โหลดการตั้งค่าจากไฟล์ config.json
try:
    with open('config.json') as f:
        config = json.load(f)
except FileNotFoundError:
    print("❌ ไม่พบไฟล์ config.json พี่ต้องสร้างไฟล์ก่อนนะครับ!")
    exit()

# 2. ตั้งค่าสมอง AI (Gemini)
genai.configure(api_key=config['GEMINI_API_KEY'])
model = genai.GenerativeModel('gemini-pro')

# 3. ตั้งค่าการเชื่อมต่อ Discord
intents = discord.Intents.default()
intents.message_content = True  # สำคัญมาก: ต้องเปิดใน Discord Dev Portal ด้วย
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ บอทตัวที่สอง {bot.user} ออนไลน์แล้วครับพี่!')

@bot.event
async def on_message(message):
    # ป้องกันบอทคุยกับตัวเอง
    if message.author == bot.user:
        return

    # ถ้าใครทักมา บอทจะเอาไปถาม Gemini แล้วตอบกลับออโต้
    try:
        async with message.channel.typing():  # แสดงว่าบอทกำลังพิมพ์...
            response = model.generate_content(message.content)
            await message.reply(response.text)
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")

# 4. เริ่มทำงาน
bot.run(config['MTUwMDc4NDg2ODA3NjgxNDMzNg.G3rgeR.QLyyW-o0FjXUwGhY7_AnWv82IxtNebcv8rkpzI'])
