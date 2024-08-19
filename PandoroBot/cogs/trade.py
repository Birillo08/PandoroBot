import discord
from discord.ext import commands
import json
import asyncio

class Trade(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='trade')
    async def trade_pokemon(self, ctx, user: discord.User):
        if user == ctx.author:
            await ctx.send("Non puoi scambiare Pokémon con te stesso.")
            return

        user_id = str(ctx.author.id)
        other_user_id = str(user.id)

        user_data = self.load_user_data(user_id)
        other_user_data = self.load_user_data(other_user_id)

        if not user_data or not other_user_data:
            await ctx.send("Non è stato possibile caricare i dati degli utenti.")
            return

        if 'pokemon' not in user_data or not user_data['pokemon']:
            await ctx.send("Non hai Pokémon nel tuo PC.")
            return
        if 'pokemon' not in other_user_data or not other_user_data['pokemon']:
            await ctx.send(f"{user.name} non ha Pokémon nel suo PC.")
            return

        user_pokemon_list = "\n".join([f"{i+1}. {p['nome']}" for i, p in enumerate(user_data['pokemon'])])
        other_user_pokemon_list = "\n".join([f"{i+1}. {p['nome']}" for i, p in enumerate(other_user_data['pokemon'])])

        await ctx.send(
            f"**I tuoi Pokémon:**\n{user_pokemon_list}\n\n**Pokémon di {user.name}:**\n{other_user_pokemon_list}\n\nPer favore, rispondi con il numero del Pokémon che vuoi scambiare e il numero del Pokémon che desideri ricevere da {user.name}."
        )

        def check(msg):
            return msg.author == ctx.author or msg.author == user

        try:
            response = await self.bot.wait_for('message', timeout=60.0, check=check)
            user_choice, other_user_choice = map(int, response.content.split())

            if user_choice < 1 or user_choice > len(user_data['pokemon']) or other_user_choice < 1 or other_user_choice > len(other_user_data['pokemon']):
                await ctx.send("Scelte non valide.")
                return

            user_pokemon_to_give = user_data['pokemon'][user_choice - 1]
            other_user_pokemon_to_give = other_user_data['pokemon'][other_user_choice - 1]

            user_data['pokemon'].remove(user_pokemon_to_give)
            other_user_data['pokemon'].remove(other_user_pokemon_to_give)

            user_data['pokemon'].append(other_user_pokemon_to_give)
            other_user_data['pokemon'].append(user_pokemon_to_give)

            self.save_user_data(user_id, user_data)
            self.save_user_data(other_user_id, other_user_data)

            await ctx.send(f"Scambio completato! Hai ricevuto {other_user_pokemon_to_give['nome']}, mentre {user.name} ha ricevuto {user_pokemon_to_give['nome']}.")
        except asyncio.TimeoutError:
            await ctx.send("Tempo scaduto per la scelta dei Pokémon.")

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

    def save_user_data(self, user_id, data):
        user_data_path = 'data/user_data.json'
        try:
            with open(user_data_path, 'r') as f:
                user_data = json.load(f)
        except FileNotFoundError:
            user_data = {}
        except json.JSONDecodeError:
            user_data = {}

        user_data[user_id] = data

        try:
            with open(user_data_path, 'w') as f:
                json.dump(user_data, f, indent=4)
        except IOError:
            print("Errore nella scrittura del file user_data.json.")

def setup(bot):
    bot.add_cog(Trade(bot))
