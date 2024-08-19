import discord
from discord.ext import commands
from utils.pokemon_utils import get_random_pokemon
import json

class DailyPokemon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='dailypokemon')
    async def daily_pokemon(self, ctx):
        pokemon = get_random_pokemon()
        embed = discord.Embed(
            title=f"Un {pokemon['nome']} è apparso!",
            description=f"Livello: {pokemon['level']}\n{pokemon['description']}",
            color=discord.Color.blue()
        )
        embed.set_image(url=pokemon['image_url'])
        await ctx.send(embed=embed, view=CatchButton(pokemon))

class CatchButton(discord.ui.View):
    def __init__(self, pokemon):
        super().__init__()
        self.pokemon = pokemon

    @discord.ui.button(label="Lancia una Pokéball!", style=discord.ButtonStyle.green)
    async def catch(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = str(interaction.user.id)
        user_data = self.load_user_data(user_id)
        if 'pokemon' not in user_data:
            user_data['pokemon'] = []
        if self.pokemon not in user_data['pokemon']:
            user_data['pokemon'].append(self.pokemon)
            self.save_user_data(user_id, user_data)
            await interaction.response.send_message(f"Hai catturato {self.pokemon['nome']}!")
        else:
            await interaction.response.send_message(f"Hai già catturato {self.pokemon['nome']}.")

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
    bot.add_cog(DailyPokemon(bot))
