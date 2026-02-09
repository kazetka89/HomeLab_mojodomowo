import discord
import random
import asyncio
import aiohttp
import cloudscraper
import sys
import json
import os
import dashboard  # Twój moduł dashboardu
from discord.ext import commands, tasks

# ==================================================
# KONFIGURACJA BOTA
# ==================================================
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# Dane dla dashboardu
bot.twitch_name_val = 'btown'
bot.twitch_name_val1 = 'buli'
bot.twitch_online_val = False
bot.twitch_online_val1 = False # Dodano drugą flagę Twitch
bot.kick_data_val = {
    'takuu': {'is_online': False},
    'pisicelarp': {'is_online': False},
    'paprycjusz': {'is_online': False},
    'rudaninja': {'is_online': False}
}

# --- NOWA FUNKCJA: ZAPIS DO PLIKU (Naprawia błąd 500 ze zdjęcia) ---
def save_status_to_file():
    try:
        data = {
            "twitch": {
                bot.twitch_name_val: bot.twitch_online_val,
                bot.twitch_name_val1: bot.twitch_online_val1
            },
            "kick": {user: info['is_online'] for user, info in bot.kick_data_val.items()}
        }
        # Ścieżka absolutna gwarantuje, że Dashboard zawsze znajdzie plik
        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, 'status.json')
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"💾 Zapisano status do: {file_path}")
    except Exception as e:
        print(f"❌ Błąd zapisu: {e}")

# ==================================================
# 🔒 KANAŁY I KONFIGURACJA API
# ==================================================
KANAL_KOMEND_ID = 1467309972240072828 
KANAL_LOSOWANIA_NAZWA = 1467556458613964890
KANAL_POWIADOMIEN_ID = 1469077717176811800
KANAL_PINGI_ID = 1103321323616346143

TWITCH_CLIENT_ID = 'krt5ejcxtvguxho0ez58k48zccl118'
TWITCH_CLIENT_SECRET = '66pu3m4ezc3whn27t06glpt93yb41x'
STREAMER_NAME = bot.twitch_name_val

try:
    scraper = cloudscraper.create_scraper()
    print("✅ Scraper Kick zainicjalizowany.")
except Exception as e:
    print(f"❌ Krytyczny błąd scrapera: {e}")
    sys.exit(1)

# ==================================================
# --- SYSTEM POWIADOMIEN TWITCH ---
# ==================================================
async def get_twitch_access_token():
    url = f'https://id.twitch.tv/oauth2/token?client_id={TWITCH_CLIENT_ID}&client_secret={TWITCH_CLIENT_SECRET}&grant_type=client_credentials'
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url) as resp:
                data = await resp.json()
                return data.get('access_token')
    except Exception as e:
        print(f"⚠️ Błąd tokenu Twitch: {e}")
        return None

@tasks.loop(minutes=2)
async def check_twitch_status():
    token = await get_twitch_access_token()
    if not token: return

    headers = {'Client-ID': TWITCH_CLIENT_ID, 'Authorization': f'Bearer {token}'}
    url = f'https://api.twitch.tv/helix/streams?user_login={STREAMER_NAME}'

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                data = await resp.json()
                currently_live = data.get('data') and len(data['data']) > 0
                
                if currently_live:
                    if not bot.twitch_online_val:
                        bot.twitch_online_val = True
                        stream_data = data['data'][0]
                        channel = bot.get_channel(KANAL_POWIADOMIEN_ID)
                        if channel:
                            embed = discord.Embed(
                                title=f"🔴 {STREAMER_NAME} rozpoczął stream na Twitchu!",
                                description=f"**Tytuł:** {stream_data['title']}\n**Gra:** {stream_data['game_name']}",
                                url=f"https://twitch.tv/{STREAMER_NAME}",
                                color=discord.Color.purple()
                            )
                            thumb = stream_data['thumbnail_url'].replace('{width}', '1280').replace('{height}', '720')
                            embed.set_image(url=thumb)
                            await channel.send(f"📢 @everyone **{STREAMER_NAME}** właśnie odpalił live!", embed=embed)
                else:
                    bot.twitch_online_val = False
        save_status_to_file() # <--- KLUCZOWE: Odśwież stronę WWW
    except Exception as e:
        print(f"⚠️ Błąd sprawdzania Twitch: {e}")

# ==================================================
# --- SYSTEM POWIADOMIEN KICK ---
# ==================================================
async def check_kick_live_status(username):
    url = f"https://kick.com/api/v1/channels/{username}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}
    loop = asyncio.get_event_loop()
    try:
        response = await loop.run_in_executor(None, lambda: scraper.get(url, headers=headers, timeout=10))
        if response.status_code == 200:
            data = response.json()
            livestream = data.get('livestream')
            if livestream:
                return {"is_live": True, "title": livestream.get('session_title', 'Brak tytułu'), "category": livestream.get('categories', [{}])[0].get('name', 'Inne'), "thumbnail": livestream.get('thumbnail', {}).get('url'), "viewers": livestream.get('viewer_count', 0)}
        return {"is_live": False}
    except:
        return {"is_live": False}

@tasks.loop(minutes=2)
async def check_kick_loop():
    for username, data in bot.kick_data_val.items():
        status = await check_kick_live_status(username)
        if status["is_live"]:
            if not data['is_online']:
                bot.kick_data_val[username]['is_online'] = True
                channel = bot.get_channel(KANAL_POWIADOMIEN_ID)
                if channel:
                    embed = discord.Embed(title=f"🟢 {username} na Kicku!", description=f"**Tytuł:** {status['title']}", url=f"https://kick.com/{username}", color=0x53fc18)
                    if status['thumbnail']: embed.set_image(url=status['thumbnail'])
                    await channel.send(f"📢 @everyone **{username}** odpalił live na Kicku!", embed=embed)
        else:
            bot.kick_data_val[username]['is_online'] = False
        await asyncio.sleep(2)
    save_status_to_file() # <--- KLUCZOWE: Odśwież stronę WWW

# ==================================================
# --- EVENTY I KOMENDY ---
# ==================================================
@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} jest online!')
    save_status_to_file() # Wymuś stworzenie pliku przy starcie
    if not check_twitch_status.is_running(): check_twitch_status.start()
    if not check_kick_loop.is_running(): check_kick_loop.start()

if __name__ == "__main__":
    dashboard.start_dashboard(bot)
    bot.run('TOKEN')
