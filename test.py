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
  try:   
    embed = discord.Embed(title=title,description=description,color=0xD1FAFF)
    await interaction.response.send_message(embed=embed)
  except Exception as e:
    print(e)
    await interaction.response.send_message("エラーが発生しました",ephemeral=True)

@tree.command(name="userinfo", description="指定したユーザーの情報を表示する")
async def user_info(interaction: discord.Interaction,user:discord.User):
  try:
    embed = discord.Embed(title=user.display_name)
    embed.set_thumbnail(
        url=user.avatar.url if user.avatar else discord.Embed.Empty)

    embed.add_field(name="user name",value=user.name,inline=False)
    embed.add_field(name="account create",value=user.created_at.strftime("%Y-%m-%d %H:%M:%S"),inline=False)

    guild = interaction.guild
    member = guild.get_member(user.id)
    if member:
      roles = [role.mention for role in member.roles[1:]]
      if roles:
        embed.add_field(name="role",value=" ".join(roles),inline=False)
      else:
        embed.add_field(name="role",value="none",inline=False)
    else:
      embed.add_field(name="role",value="none",inline=False)

    await interaction.response.send_message(embed=embed)
  except Exception as e:
    print(e)
    await interaction.response.send_message("エラーが発生しました",ephemeral=True)

keep_alive()
client.run(os.getenv('token'))
