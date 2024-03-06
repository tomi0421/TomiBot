# プレフィックスはt!でいきます。 byとみー
import discord
from discord.ext import commands
# keep_aliveを追加 by M
from keep_alive import keep_alive
# osを追加
import os

intents = discord.Intents.all()
bot = discord.Bot(intents = intents)
tree = discord.app_commands.CommandTree(bot)  


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# この下にあるやつがt!memberで動くはず by とみー
@tree.command(name="test", description="test command")
async def member_info(ctx, member: discord.Member):
    embed = discord.Embed(title=f'Member Information for {member.name}', color=member.color)

    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='ID', value=member.id, inline=False)
    embed.add_field(name='Top Role', value=member.top_role.name, inline=False)
    embed.add_field(name='Joined Server', value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

    await ctx.send(embed=embed)
@bot.event # 挨拶適当に作ったbyとみー
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    if message.content == 'おはよう':
        await message.reply("おはようございます！今日もいい天気ですね（?）")
    elif message.content == 'こんにちは':
        await message.reply("こんにちは！")
    elif message.content == 'こんばんは':
        await message.reply("こんばんは！")

# keep_aliveを使用 by M
keep_alive()
# envファイルでtokenを指定するように変更　by M
bot.run(os.getenv('token'))
