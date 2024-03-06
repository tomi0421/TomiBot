import discord
import os
from keep_alive import keep_alive

intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await client.change_presence(activity=discord. Activity(type=discord.ActivityType.competing, name=f'{len(client.guilds)}servers'))
    print(f'{client.user} is online!')
    await tree.sync()

@tree.command(name="embed", description="embed command")
async def embed_command(interaction:discord.Interaction,title:str,description:str):
    embed = discord.Embed(title=title,description=description,color=0xD1FAFF)
    await interaction.response.send_message(embed=embed)

@tree.command(name="userinfo", description="userinfo command")
async def userinfo_command(interaction: discord.Interaction, user:discord.User)
    embed = discord.Embed(title=user.name, description=user.tag)

keep_alive()
client.run(os.getenv('token'))
