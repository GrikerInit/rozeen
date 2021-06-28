import discord
from discord import guild
from discord import permissions
from discord import message
from discord.ext import commands
import os

client = commands.Bot(command_prefix=".")
token = os.getenv("DISCORD_BOT_TOKEN")

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
async def clearaaaaa(ctx, amount=3) :
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
async def mute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_role(name="Muted", permissions=perms)
        await member.add_roles(role)
        await ctx.send(f"User has been unmuted")
    else:
       await member.add_roles(role)
       await ctx.send(f"User has been unmuted")

@client.command()
async def unmute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    guild = ctx.guild
    if role not in guild.roles:
        perms = discord.Permissions(send_messages=False, speak=False)
        await guild.create_role(name="Muted", permissions=perms)
        await member.remove_roles(role)
        await ctx.send(f"User has been unmuted")
    else:
       await member.remove_roles(role)
       await ctx.send(f"User has been unmuted")

@commands.command()

@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason=None):
 await client.kick(member)
 await ctx.send(f'User {member} has been kick')

client.run(token)
