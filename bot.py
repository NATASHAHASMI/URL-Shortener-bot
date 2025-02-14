import os
import aiohttp
from telegram import InputMediaPhoto
from pyrogram import Client, filters

API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')
BOT_TOKEN = os.environ.get('BOT_TOKEN')
API_KEY = os.environ.get('API_KEY')
WEBSITE = os.environ.get('WEBSITE')


try:
    bot = Client('shortener bot',
                 api_id=int(API_ID),
                 api_hash=API_HASH,
                 plugins = dict(root="plugins"),
                 bot_token=BOT_TOKEN,
                 workers=50,
                 sleep_threshold=10)
except Exception:
    print("Add var values properly. Read readme.md once")


@bot.on_message(filters.command('start'))
async def start(bot, message):
    start_msg = f"""
<b>Hi {message.from_user.mention}!</b>

<i>I'ᴍ {WEBSITE} Bᴏᴛ. Jᴜꜱᴛ Sᴇɴᴅ Mᴇ Lɪɴᴋ Aɴᴅ Gᴇᴛ Sʜᴏʀᴛ Lɪɴᴋ!</i>

<i>Fᴏʀ Cᴜꜱᴛᴏᴍ Aʟɪᴀꜱ, <code>[link] | [custom_alias]</code>, Sᴇɴᴅ Iɴ Tʜɪꜱ Fᴏʀᴍᴀᴛ</i>\n
<b>Ex: https://t.me/xayoonara | Xayonara</b>

<spoiler><b>🔋 ᴍᴀɪɴᴛᴀɪɴᴇᴅ ʙʏ - <a href='https://telegram.me/xayonara_contact_bot'>✘ 𝐚 𝐲 𝐨 𝐧 𝐚 𝐫 𝐚.</a></b></spoiler>
    """
    await message.reply_photo(
        photo="https://envs.sh/aL3.jpg",
        caption=start_msg,
        parse_mode="markdown",
        quote=True,
        has_spoiler=True
    )

@bot.on_message(filters.regex(r'https?://[^\s]+') & filters.private)
async def link_handler(bot, message):
    if "|" in message.text:
        link_parts = message.text.split("|")
        link = link_parts[0]
        aliases = link_parts[1:len(message.text) + 1]
        alias1 = ""
        for alias in aliases:
            alias1 += alias
        x = alias1.replace(" ", "")
    else:
        link = message.matches[0].group(0)
        x= ""
    short_link = await get_shortlink(link, x)
    await message.reply(short_link, quote=True)


async def get_shortlink(link, x):
    url = f'https://{WEBSITE}/api'
    params = {'api': API_KEY,
              'url': link,
              'alias': x
              }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params, raise_for_status=True, ssl=False) as response:
            data = await response.json()
            print(data["status"])
            if data["status"] == "success":
                return f"<code>{data['shortenedUrl']}</code>\n\nHere is your Link:\n{data['shortenedUrl']}"
            else:
                return f"Error: {data['message']}"

bot.run()
