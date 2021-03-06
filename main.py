
import discord
from time import time
from discord import guild
from discord import permissions
from discord import message
from discord.embeds import Embed
from discord.ext import commands
import os

from discord.ext.commands import context

client = commands.Bot(command_prefix=".")
token = os.getenv("DISCORD_BOT_TOKEN")
client.sniped_messages = {}


@client.event
async def on_ready() :
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("I am online")

@client.command()
async def ping(ctx) :
    await ctx.send(f"🏓 Pong with {str(round(client.latency, 2))}")

@client.command(name="whoami")
async def whoami(ctx) :
    await ctx.send(f"You are {ctx.message.author.name}")

@client.command()
async def clear(ctx, amount=3) :
    await ctx.channel.purge(limit=amount)

@client.command('role')
@commands.has_permissions(administrator=True) #permissions
async def role(ctx, user : discord.Member, *, role : discord.Role):
  if role.position > ctx.author.top_role.position: #if the role is above users top role it sends error
    return await ctx.send('**:x: | That role is above your top role!**') 
  if role in user.roles:
      await user.remove_roles(role) #removes the role if user already has
      await ctx.send(f"Removed {role} from {user.mention}")
  else:
      await user.add_roles(role) #adds role if not already has it
      await ctx.send(f"Added {role} to {user.mention}") 

@client.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_role(name="Muted", permissions=perms)
        await member.add_roles(role)
        await ctx.send(f"{member} has been muted")
    else:
       await member.add_roles(role)
       await ctx.send(f"{member} has been muted")

@client.command()
@commands.has_permissions(administrator=True)
async def unmute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_remove(name="Muted", permissions=perms)
        await member.remove_roles(role)
        await ctx.send(f"{member} has been unmuted")
    else:
       await member.remove_roles(role)
       await ctx.send(f"{member} has been unmuted")
       


@client.command()
async def kill(ctx, member:discord.Member):
    await ctx.send(f"<@{member.id}> was killed")
    await ctx.send(f"https://images-ext-1.discordapp.net/external/5gWWY_xqzhR914VnkAnRl8FCEcE29F65C-R15ffTjqM/https/cdn.weeb.sh/images/B1VnoJFDZ.gif")

@client.event
async def on_message_delete(message):
    print(f'sniped message {message}')
    client.sniped_messages[message.guild.id] = (
        message.content, message.author, message.channel.name, message.created_at)


@client.command()
async def snipe(ctx):
    try:
        contents, author, channel_name, time = client.sniped_messages[ctx.guild.id]

    except:
        await ctx.channel.send("Couldn't find a message to snipe!")
        return

    embed = discord.Embed(description=contents,
                          color=discord.Color.purple(), timestamp=time)
    embed.set_author(
        name=f"{author.name}#{author.discriminator}", icon_url=author.avatar_url)
    embed.set_footer(text=f"Deleted in : #{channel_name}")

    await ctx.channel.send(embed=embed)

@commands.has_permissions(kick_members=True)
@client.command()
async def kick(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.kick(reason=reason)
        kick = discord.Embed(title=f":boot: Kicked {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=kick)

@commands.has_permissions(ban_members=True)
@client.command()
async def ban(ctx, user: discord.Member, *, reason="No reason provided"):
        await user.ban(reason=reason)
        ban = discord.Embed(title=f":hammer: Banned {user.name}!", description=f"Reason: {reason}\nBy: {ctx.author.mention}")
        await ctx.message.delete()
        await ctx.channel.send(embed=ban)


client.run(token)
