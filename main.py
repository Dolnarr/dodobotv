import discord
import random
from discord.ext import commands, tasks
from itertools import cycle
import datetime

client = commands.Bot(command_prefix = 'do.')
client.remove_command("help")
status = cycle(["le peuple | do.help", "l'ennuie dans les yeux | do.help", "des cookies | do.help"])

#connection au bot et statut
@client.event
async def on_ready():
    change_status.start()
    print("Bot connecté.")

@tasks.loop(seconds=600)
async def change_status():
    activity = discord.Activity(name=(next(status)), type=discord.ActivityType.watching)
    await client.change_presence(activity=activity)
#event (bienvenue au revoir)
@client.event
async def on_member_join(member):
    embed = discord.Embed(colour=0x7289da, description=f"Salut {member.name}, Bienvenue sur ce serveur discord. T\'es le/la {len(list(member.guild.members))}e arrivé\(e\). 😀")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
    embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcfromtimestamp(1553629094)

    channel = client.get_channel(id=613860269944471552)

    await channel.send(embed=embed)

@client.event
async def on_member_rezmove(member):
    embed = discord.Embed(colour=0x7289da, description=f"{member.name} nous a quitté... 😔")
    embed.set_thumbnail(url=f"{member.avatar_url}")
    embed.set_author(name=f"{member.name}", icon_url=f"{member.avatar_url}")
    embed.set_footer(text=f"{member.guild}", icon_url=f"{member.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcfromtimestamp(1553629094)

    channel = client.get_channel(id=613860269944471552)

    await channel.send(embed=embed)

#fun
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong ! {round(client.latency * 1000)}ms")
    print("commande do.ping utilisée.")

@client.command(aliases=["8ball"])
async def _8ball(ctx, *, question):
    responses = ["Oui ! Biensûr !",
                "Non.. Je ne penses pas.",
                "Hum, pourrais tu répéter la question ?",
                "Je sais pas, demandes au dieu tout puissant <@232942700083544065>",
                "Peut-être",
                "Pas du tout",
                "Je sais pas",
                "Je penses pas",
                "Bah oue, logique"]
    await ctx.send(f"Question: {question}\nRéponse: {random.choice(responses)}")
    print("commande do.8ball utilisée.")

@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Merci de poser ta question.")

#modération (kick, ban, unban, purge/clear)
@client.command()
@commands.has_permissions(kick_members=True, administrator=True)
async def kick(ctx, member: discord.Member = None, *, reason=None):
    await member.send(f"tu as été kick de {ctx.guild.name} pour la raison : {reason}")
    await ctx.channel.send(f"<@{ctx.author.id}> a exclu {member}")
    await member.kick(reason=reason)
    print(f"commande do.kick utilisée. Pseudo du membre kick : {member}. Raison : {reason}. ID : {member.id};")

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.channel.send("Merci de dire l'utilisateur à expulser.")

@client.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def ban(ctx, member: discord.Member = None, *, reason=None):
    await member.send(f"tu as été ban de {ctx.guild.name} pour la raison : {reason}")
    await ctx.channel.send(f"<@{ctx.author.id}> a banni {member}")
    await member.ban(reason=reason)
    print(f"commande do.ban utilisée. Pseudo du membre ban : {member}. Raison : {reason}. ID : {member.id};")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Merci de dire l'utilisateur à bannir.")

@client.command()
@commands.has_permissions(ban_members=True, administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} a été débanni !")
            print(f"commande do.unban utilisée. Pseudo du membre unban : {member}. ID : {member.id};")
            return

@client.command(aliases=["purge"])
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount + 1)
    await ctx.channel.send(f'deleted {amount} messages', delete_after=5.0)
    print("commande dodo.clear utilisée.")

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Merci de dire le nombre de message à supprimer.")

client.run("NDQ0NTMwNTU3NTg2NjM2ODAy.XSUqhA.GBmP5yuzcM7Ev7kwEkd4Ilg1ZjI")
