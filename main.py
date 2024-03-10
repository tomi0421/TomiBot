import discord
import os
from keep_alive import keep_alive
import random
from discord import Embed, channel, Interaction, integrations
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from collections import defaultdict
from datetime import datetime, timedelta
from discord.ui import Select, View

intents = discord.Intents.all()
client = discord.Client(intents = intents)
tree = discord.app_commands.CommandTree(client)

@client.event
async def on_ready():
    await client.change_presence(activity=discord. Activity(type=discord.ActivityType.competing, name=f'{len(client.guilds)}servers'))
    print(f'{client.user} is online!')
    await tree.sync()

@tree.command(name='serverstats', description="サーバーがアクティブかがわかります")
async def server_stats(interaction):
      start_time = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

      message_count = 0

      async for message in interaction.channel.history(after=start_time, limit=None):
          if not message.author.bot:
              message_count += 1

      embed = discord.Embed(title='サーバー統計', color=discord.Color.blue())
      embed.add_field(name='今日のメッセージ数', value=message_count, inline=False)
      embed.set_footer(text=f'リクエスト by {interaction.author.name}', icon_url=interaction.author.avatar_url)

      await interaction.response.send_message(embed=embed)

@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content == 'おはよう':
        await message.reply("おはようございます！今日もいい天気ですね（?）")
    elif message.content == 'こんにちは':
        await message.reply("こんにちは！")
    elif message.content == 'こんばんは':
        await message.reply("こんばんは！")
        
@tree.command(name="embed", description="埋め込みメッセージを送信します")
async def embed_command(interaction: discord.Interaction,title:str,description:str):
    embed = discord.Embed(title=title,description=description,color=0xD1FAFF)
    await interaction.response.send_message(embed=embed)

@tree.command(name="userinfo", description="指定したユーザーの情報を表示する")
async def user_info(interaction: discord.Interaction,user:discord.User):
  try:
    embed = discord.Embed(title=user.display_name,color=discord.Color(random.randint(0,0xFFFFFF)))
    embed.set_thumbnail(
        url=user.avatar.url if user.avatar else discord.Embed.Empty)

    embed.add_field(name="user name",value=user.name,inline=False)
    embed.add_field(name="user id",value=user.id,inline=False)
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

@client.event
async def on_interaction(inter: discord.Interaction):
    try:
        if inter.data['component_type'] == 2:
            await on_button_click(inter)
    except KeyError:
        pass

async def on_button_click(interaction: discord.Interaction):
    custom_id = interaction.data["custom_id"]
    if custom_id.startswith("ticket_"):
        parts = custom_id.split('_')
        category_id, role_id = parts[1], parts[2]
        if category_id != 'None':
            category_id = int(category_id)
            category = client.get_channel(category_id)
        else:
            category = interaction.guild.categories[0]

        ticket_nameA = f'ticket-{interaction.user.name}-{interaction.user.discriminator}'
        ticket_name = remove_dots(ticket_nameA)
        existing_channel = discord.utils.get(category.channels, name=ticket_name)

        if existing_channel:
            await interaction.response.send_message('既にチケットが存在します', ephemeral=True)
            return
        else:
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
                interaction.user: discord.PermissionOverwrite(read_messages=True)
            }
            ticket_channel = await category.create_text_channel(name=ticket_name, overwrites=overwrites)
            await interaction.response.send_message(f'チャンネルが作成されました: {ticket_channel.mention}', ephemeral=True)
            embed = discord.Embed(title='チケット', description=f'担当者が来るまでお待ちください', color=discord.Colour.red())
            embed.set_footer(text="ticket")
            view = discord.ui.View(timeout=None)
            button = discord.ui.Button(label="閉じる", style=discord.ButtonStyle.primary, custom_id="tk_delete")
            view.add_item(button)
            if not role_id.startswith("userid"):
              role_id = int(role_id)
              role = interaction.guild.get_role(role_id)
              await ticket_channel.send(f'{role.mention}', embed=embed, view=view)
            else:
              parts = role_id.split('.')
              user_id = parts[1]
              await ticket_channel.send(f'<@{user_id}>', embed=embed, view=view)

    if custom_id == ("tk_delete"):
      embed = discord.Embed(title="チケットを閉じる", description="チケットを閉じますか")
      view = discord.ui.View(timeout=None)
      button1 = discord.ui.Button(label='はい', style=discord.ButtonStyle.secondary, custom_id='channel_delete_true')
      button2 = discord.ui.Button(label='いいえ', style=discord.ButtonStyle.secondary, custom_id='channel_delete_false')
      view.add_item(button1)
      view.add_item(button2)
      await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

    if custom_id.startswith("channel_delete_"):
      if custom_id == "channel_delete_true":
        channel = interaction.channel
        await channel.delete()
      if custom_id == "chanel_delete_false":
        await interaction.response.send_message("キャンセルしました", ephemeral=True)

@tree.command(name="ticket", description="チケットパネルを設置します")
@app_commands.describe(
    title='タイトル',
    description='説明',
    label='ラベル',
    category='カテゴリ',
    role='ロール'
)
@app_commands.checks.has_permissions(manage_channels=True)
async def create_ticket(interaction: discord.Interaction,
                        title: str = 'チケットパネル',
                        description: str = 'ボタンを押してチケットを作成',
                        label: str = '問い合わせ',
                        category: discord.CategoryChannel = None,
                        role: discord.Role = None):
    await interaction.response.send_message("チケットパネルを作成しました",ephemeral=True)
    embed = discord.Embed(title=title, color=discord.Colour.green())
    embed.add_field(name='', value=description)
    embed.set_footer(text="ticket")
    view = discord.ui.View(timeout=None)
    button_label = label
    user = interaction.user.id
    custom_id = f"ticket_{category.id if category else 'None'}_{role.id if role else f'userid.{user}'}"
    button = discord.ui.Button(label=button_label, style=discord.ButtonStyle.secondary, custom_id=custom_id)
    view.add_item(button)
    await interaction.channel.send(embed=embed, view=view)

banned_words = ['死ね', 'バカ', '馬鹿','アホ','ゴミカス','殺す','殺し','消え','くたばれ']

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    message_content = message.content.lower()

    for word in banned_words:
        if word in message_content:
            await message.delete()
            await message.channel.send('この単語は不適切である可能性が高いため利用できません。異議申し立ては鯖主のDMに。')
            return

keep_alive()
client.run(os.getenv('token'))
