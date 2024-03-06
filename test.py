import discord

intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await client.change_presence(activity=discord. Activity(type=discord.ActivityType.competing, name=f'{len(client.guilds)}'))
    print(f'{client.user} is online!')
    await tree.sync()

@tree.command(name="test", description="test command")
async def panel_au(interaction: discord.Interaction):
    await interaction.respons.send("test")

cliente.run(os.getenv('token'))
