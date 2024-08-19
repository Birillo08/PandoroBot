import discord
from discord.ext import commands
from config import TOKEN

# Crea un oggetto Intents
intents = discord.Intents.default()
intents.message_content = True  # Abilita la ricezione dei contenuti dei messaggi

# Imposta il prefisso del bot e gli intents
bot = commands.Bot(command_prefix=['!', '/'], intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} è online!')

# Carica le cogs in modo corretto
async def load_cogs():
    initial_extensions = ['cogs.daily_pokemon', 'cogs.pc', 'cogs.trade']
    for extension in initial_extensions:
        try:
            await bot.load_extension(extension)
            print(f'Extension {extension} loaded successfully.')
        except Exception as e:
            print(f'Failed to load extension {extension}.', e)

# Avvia il bot e carica le cogs
async def main():
    async with bot:
        await load_cogs()
        await bot.start(TOKEN)

# Avvia il loop principale
if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
