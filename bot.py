import os
import discord
from discord.ext import commands

TOKEN = os.getenv("TOKEN")

CHANNEL_ID = 1517099762707337306
OWNER_ID = 789379238875889684

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.guild is None:
        return

    # Ignore admins
    if message.author.guild_permissions.administrator:
        return

    # Ignore moderators (Manage Messages permission)
    if message.author.guild_permissions.manage_messages:
        return

    if message.channel.id == CHANNEL_ID:
        try:
            try:
                await message.delete()
            except:
                pass

            user_name = str(message.author)
            user_id = message.author.id
            guild_name = message.guild.name

            await message.author.ban(
                reason="Sent a message in a restricted channel."
            )

            owner = await bot.fetch_user(OWNER_ID)
            await owner.send(
                f"🚨 User banned!\n\n"
                f"User: {user_name}\n"
                f"User ID: {user_id}\n"
                f"Server: {guild_name}\n"
                f"Channel ID: {CHANNEL_ID}"
            )

        except Exception as e:
            print(e)

    await bot.process_commands(message)


bot.run(TOKEN)
