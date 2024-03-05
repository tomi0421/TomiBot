import discord
from discord.ext import commands

intents = discord.Intents.all()  
bot = commands.Bot(command_prefix='t!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

#👇この下にあるやつがt!memberで動くはず
@bot.command(name='member')
async def member_info(ctx, member: discord.Member):
    embed = discord.Embed(title=f'Member Information for {member.name}', color=member.color)

    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='ID', value=member.id, inline=False)
    embed.add_field(name='Top Role', value=member.top_role.name, inline=False)
    embed.add_field(name='Joined Server', value=member.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

    await ctx.send(embed=embed)

bot.run('DISCORDBOTTOKEN')
