# Configurando tokens
import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

import re
import ast
from io import BytesIO
import matplotlib
matplotlib.use("Agg")  # backend headless para servidores
import matplotlib.pyplot as plt
#----





import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$plot'):
        try:
            matches = re.findall(r'\[.*?\]', message.content)
            if len(matches) < 2:
                await message.channel.send("Formato: `$plot [x1,x2,...] [y1,y2,...]`")
                return

            x_list = ast.literal_eval(matches[0])
            y_list = ast.literal_eval(matches[1])

            if not (isinstance(x_list, list) and isinstance(y_list, list)):
                await message.channel.send("Use listas entre colchetes, ex: `$plot [1,2,3] [3,2,1]`.")
                return

            x = [float(v) for v in x_list]
            y = [float(v) for v in y_list]

            if len(x) != len(y):
                await message.channel.send("As listas precisam ter o **mesmo tamanho**.")
                return

            plt.figure()
            plt.plot(x, y, marker='o')
            plt.title("Plot")
            plt.xlabel("x")
            plt.ylabel("y")
            plt.grid(True)
            plt.tight_layout()

            buf = BytesIO()
            plt.savefig(buf, format='png', dpi=150)
            plt.close()
            buf.seek(0)

            await message.channel.send(file=discord.File(buf, filename="plot.png"))

        except (ValueError, SyntaxError):
            await message.channel.send("Não consegui interpretar as listas. Tente algo como: `$plot [1,2,3] [3,2,1]`.")
        except Exception as e:
            await message.channel.send(f"Deu ruim ao gerar o gráfico: `{e}`")

client.run(os.getenv("DISCORD_TOKEN"))
