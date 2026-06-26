import discord
from discord.ext import commands
from bot_token import TOKEN
import requests
import pyttsx3

engine = pyttsx3.init()# object creation

# RATE
rate = engine.getProperty('rate')   # getting details of current speaking rate
print(rate)                        # printing current voice rate
engine.setProperty('rate', 125)     # setting up new voice rate

# VOLUME
volume = engine.getProperty('volume')   # getting to know current volume level (min=0 and max=1)
print(volume)                          # printing current volume level
engine.setProperty('volume', 1.0)        # setting up volume level  between 0 and 1

voices = engine.getProperty('voices')    # getting details of current voice
# engine.setProperty('voice', voices[0].id)  # changing index, changes voices. o for male
engine.setProperty('voice', voices[1].id) 

intents = discord.Intents.default()
intents.message_content = True 
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    # Bot açıldığında terminalde göreceğin mesaj
    print(f"🤖 CK_Bot başarıyla aktif edildi ve göreve hazır!")


@bot.command()
async def katil(ctx):
    # Komutu yazan kişi bir sesli kanalda mı?
    if ctx.author.voice:
        kanal = ctx.author.voice.channel
        await kanal.connect()
        # Discord kanalına CK_Bot olarak havalı bir giriş mesajı atıyoruz
        await ctx.send(f"🤖 **CK_Bot**, **Kodland** sunucusunun **{kanal.name}** sesli kanalına başarıyla giriş yaptı! 🚀")
    else:
        await ctx.send("Kanka önce senin bir sesli kanala katılman gerekiyor, CK_Bot olarak yanına gelemem! ❌")

# Buraya kendi bot tokenini yapıştırmayı unutma


@bot.command()
async def start(ctx):
    await ctx.send("Selam, sana nasıl yardımcı olabilirim?")
    engine.say("Selam, sana nasıl yardımcı olabilirim?")
    engine.runAndWait()


@bot.command()
async def fact(ctx):
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    if response.status_code == 200:
        data = response.json()
        await ctx.send(data['text'])
        engine.say(data['text'])
        engine.runAndWait()

    else:
        await ctx.send("Faktı alırken bir hata oluştu.")

@bot.command()
async def weather(ctx, city):
    await ctx.send(f"{city} için hava durumunu kontrol ediliyor...")
    w = requests.get(f"https://wttr.in/{city}?format=3")
    if w.status_code == 200: 
        await ctx.send(w.text)
        engine.say(w.text)
        engine.runAndWait()
        engine.stop()

    else:
        await ctx.send("Hava durumunu alırken bir hata oluştu. Lütfen şehir adını kontrol edin ve tekrar deneyin.")
        engine.say("Hava durumunu alırken bir hata oluştu. Lütfen şehir adını kontrol edin ve tekrar deneyin.")
bot.run(TOKEN)
