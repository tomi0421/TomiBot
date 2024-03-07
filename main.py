# プレフィックスは/でいきます。 byとみー
import discord
from discord.ext import commands
# keep_aliveを追加 by M
from keep_alive import keep_alive
# osを追加by M
import os

intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# この下にあるやつが/userinfoで動くはず by とみー
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
    
@client.event #あいさつのやつ
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content == 'おはよう':
        await message.reply("おはようございます！今日もいい天気ですね（?）")
    elif message.content == 'こんにちは':
        await message.reply("こんにちは！")
    elif message.content == 'こんばんは':
        await message.reply("こんばんは！")

    await client.process_commands(message)
@tree.command(name="embed", description="埋め込みメッセージを送信します")
async def embed_command(interaction: discord.Interaction,title:str,description:str):
    embed = discord.Embed(title=title,description=description,color=0xD1FAFF)
    await interaction.response.send_message(embed=embed)


# keep_aliveを使用 by M
keep_alive()
# envファイルでtokenを指定するように変更　by M
client.run(os.getenv('token'))
