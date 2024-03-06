import discord
import os

intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await client.change_presence(activity=discord. Activity(type=discord.ActivityType.competing, name=f'{len(client.guilds)}'))
    print(f'{client.user} is online!')
    await tree.sync()

@tree.command(name="test", description="test command")
async def test_command(interaction: discord.Interaction):
    await interaction.response.send_message("test")

client.run(os.getenv('token'))
