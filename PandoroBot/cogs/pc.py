import discord
from discord.ext import commands
import json

class PC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='pc')
    async def show_pc(self, ctx):
        user_id = str(ctx.author.id)
        user_data = self.load_user_data(user_id)

        if 'pokemon' not in user_data or not user_data['pokemon']:
            await ctx.send("Il tuo PC è vuoto.")
            return

        pokemon_list = "\n".join([f"{p['nome']} (Livello {p['level']})" for p in user_data['pokemon']])
        await ctx.send(f"I tuoi Pokémon:\n{pokemon_list}")

    def load_user_data(self, user_id):
        user_data_path = 'data/user_data.json'
        try:
            with open(user_data_path, 'r') as f:
                data = json.load(f)
            return data.get(user_id, {})
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            print("Errore nella decodifica del file user_data.json.")
            return {}

def setup(bot):
    bot.add_cog(PC(bot))
