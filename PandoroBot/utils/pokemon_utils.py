import json
import random

def get_random_pokemon():
    with open('data/pokemon_data.json', 'r') as f:
        pokemons = json.load(f)

    # Pesca un Pokémon con probabilità in base alla percentuale
    pokemon = random.choices(pokemons, weights=[p['percentuale'] for p in pokemons])[0]
    pokemon['level'] = random.randint(1, 100)  # Livello casuale
    return pokemon
