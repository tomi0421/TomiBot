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
