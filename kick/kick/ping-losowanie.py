import discord
import random
from discord.ext import commands

# ==================================================
# KONFIGURACJA BOTA
# ==================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

# 🔒 KANAŁY
KANAL_KOMEND_ID = ID
KANAL_LOSOWANIA_NAZWA = ID
KANAL_PINGI_ID = ID

# ==================================================
# --- EVENTY (Automatyczna rola) ---
# ==================================================

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} jest online!')

@bot.event
async def on_member_join(member):
    try:
        role = discord.utils.get(member.guild.roles, name="h")
        channel = discord.utils.get(member.guild.text_channels, name="rangi")
        if role:
            await member.add_roles(role)
            if channel:
                await channel.send(f'🎉 Rola **{role.name}** dla {member.mention}')
    except Exception as e:
        print(f"⚠️ Błąd nadawania roli: {e}")

# ==================================================
# --- KOMENDY PINGÓW ---
# ==================================================

@bot.command(name='oliwia')
async def ping_oliwia(ctx):
    channel = bot.get_channel(KANAL_PINGI_ID)
    if channel:
        await channel.send(f'📢 Ping dla: <@ID>')
        await ctx.send("✅ Ping wysłany!")

@bot.command(name='karo')
async def ping_karo(ctx):
    channel = bot.get_channel(KANAL_PINGI_ID)
    if channel:
        await channel.send(f'📢 Ping dla: <@ID>')
        await ctx.send("✅ Ping wysłany!")

@bot.command(name='pyrpec')
async def ping_pyrpec(ctx):
    channel = bot.get_channel(KANAL_PINGI_ID)
    if channel:
        await channel.send(f'📢 Ping dla: <@ID>')
        await ctx.send("✅ Ping wysłany!")

@bot.command(name='werka')
async def ping_werka(ctx):
    channel = bot.get_channel(KANAL_PINGI_ID)
    if channel:
        await channel.send(f'📢 Ping dla: <@ID>')
        await ctx.send("✅ Ping wysłany!")

@bot.command(name='kacperrg4')
async def ping_kacper(ctx):
    channel = bot.get_channel(KANAL_PINGI_ID)
    if channel:
        await channel.send(f'📢 Ping dla: <@ID>')
        await ctx.send("✅ Ping wysłany!")

@bot.command(name='kazetka')
async def ping_kazetka(ctx):
    channel = bot.get_channel(KANAL_PINGI_ID)
    if channel:
        await channel.send(f'📢 Ping dla: <@ID>')
        await ctx.send("✅ Ping wysłany!")

# ==================================================
# --- SYSTEM LOSOWANIA ---
# ==================================================

@bot.command(name='losuj_uzytkownika')
async def losuj_cmd(ctx):
    members = [m for m in ctx.channel.members if not m.bot]
    if members:
        wylosowana = random.choice(members)
        embed = discord.Embed(title="🎲 Wynik losowania", description=f"{wylosowana.mention}", color=discord.Color.gold())
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Nie znaleziono użytkowników.")

@bot.command(name='losuj_glos')
async def losuj_glos(ctx):
    if ctx.author.voice and ctx.author.voice.channel:
        members = [m for m in ctx.author.voice.channel.members if not m.bot]
        if members:
            wylosowana = random.choice(members)
            await ctx.send(f'🎤 Wylosowano: {wylosowana.mention}')
        else:
            await ctx.send("❌ Kanał głosowy jest pusty.")
    else:
        await ctx.send("❌ Musisz być na kanale głosowym!")

# --- CHECK KANAŁÓW ---
@bot.check
async def tylko_dozwolone_kanaly(ctx):
    if ctx.channel.id in [KANAL_KOMEND_ID, KANAL_LOSOWANIA_NAZWA]: return True
    await ctx.send(f"❌ Komendy można używać tylko na dedykowanych kanałach!")
    return False

# ==================================================
# URUCHOMIENIE
# ==================================================
bot.run('TOKEN')
