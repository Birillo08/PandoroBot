import os
from dotenv import load_dotenv

# Carica le variabili d'ambiente dal file .env
load_dotenv()

# Ottieni il token dalla variabile d'ambiente
TOKEN = os.getenv('DISCORD_TOKEN')
