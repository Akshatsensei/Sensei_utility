import discord
import os
import logging
from dotenv import load_dotenv
from discord.ext import commands
from datetime import timedelta
import asyncio

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

if not token:
    raise ValueError("No DISCORD_TOKEN found in .env file")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="#", intents=intents)

IMMUNE_FILE = "immune_users.txt"
immune_users = set()

if os.path.exists(IMMUNE_FILE):
    with open(IMMUNE_FILE, "r") as file:
        immune_users = set(line.strip() for line in file)

def save_immune_users():
    with open(IMMUNE_FILE, "w") as file:
        for user_id in immune_users:
            file.write(f"{user_id}\n")

bad_words = {"fuck", "shit", "bitch", "mc", "bc", "bkl"}

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} is online and slash commands are synced!")

@bot.event
async def on_member_join(member):
    channel = member.guild.system_channel
    if channel:
        await channel.send(f"Welcome {member.mention}!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if any(word in message.content.lower() for word in bad_words):
        try:
            await message.delete()
            await message.channel.send(
                f"{message.author.mention} ye tera ghar nhi jo gnd macha rha"
            )
        except discord.Forbidden:
            pass

    await bot.process_commands(message)

@bot.tree.command(name="ping", description="Check bot response")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")

@bot.tree.command(name="hello", description="Say hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message("Hello!")

@bot.tree.command(name="clear", description="Delete messages")
@commands.has_permissions(manage_messages=True)
async def clear(interaction: discord.Interaction, amount: int):
    await interaction.channel.purge(limit=amount)
    await interaction.response.send_message(
        f"Deleted {amount} messages", ephemeral=True
    )

@bot.tree.command(name="immune", description="Make a user immune")
@commands.has_permissions(administrator=True)
async def immune(interaction: discord.Interaction, member: discord.Member):

    immune_users.add(str(member.id))
    save_immune_users()

    await interaction.response.send_message(
        f"{member.mention} is now IMMUNE 🛡️"
    )

@bot.tree.command(name="unimmune", description="Remove immunity")
@commands.has_permissions(administrator=True)
async def unimmune(interaction: discord.Interaction, member: discord.Member):

    if str(member.id) in immune_users:
        immune_users.remove(str(member.id))
        save_immune_users()
        await interaction.response.send_message(
            f"{member.mention} is no longer immune ❌"
        )
    else:
        await interaction.response.send_message(
            "User is not immune.", ephemeral=True
        )

@bot.tree.command(name="kick", description="Kick a member")
@commands.has_permissions(kick_members=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):

    if str(member.id) in immune_users:
        return await interaction.response.send_message(
            "This user is IMMUNE 🛡️", ephemeral=True
        )

    if member == interaction.user:
        return await interaction.response.send_message(
            "You can't kick yourself.", ephemeral=True
        )

    if member == interaction.guild.owner:
        return await interaction.response.send_message(
            "You can't kick the server owner.", ephemeral=True
        )

    try:
        await member.kick(reason=reason)
        await interaction.response.send_message(
            f"{member.mention} has been kicked. Reason: {reason}"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "I don't have permission.", ephemeral=True
        )

@bot.tree.command(name="ban", description="Ban a member")
@commands.has_permissions(ban_members=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):

    if str(member.id) in immune_users:
        return await interaction.response.send_message(
            "This user is IMMUNE 🛡️", ephemeral=True
        )

    if member == interaction.user:
        return await interaction.response.send_message(
            "You can't ban yourself.", ephemeral=True
        )

    if member == interaction.guild.owner:
        return await interaction.response.send_message(
            "You can't ban the owner.", ephemeral=True
        )

    try:
        await member.ban(reason=reason)
        await interaction.response.send_message(
            f"{member.mention} has been banned. Reason: {reason}"
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "I don't have permission.", ephemeral=True
        )

@bot.tree.command(name="timeout", description="Timeout a member")
@commands.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, member: discord.Member, minutes: int):

    if str(member.id) in immune_users:
        return await interaction.response.send_message(
            "This user is IMMUNE 🛡️", ephemeral=True
        )

    if member == interaction.user:
        return await interaction.response.send_message(
            "You can't timeout yourself.", ephemeral=True
        )

    if member == interaction.guild.owner:
        return await interaction.response.send_message(
            "You can't timeout the owner.", ephemeral=True
        )

    try:
        await member.timeout(timedelta(minutes=minutes))
        await interaction.response.send_message(
            f"{member.mention} timed out for {minutes} minutes."
        )
    except discord.Forbidden:
        await interaction.response.send_message(
            "I don't have permission.", ephemeral=True
        )

# Run bot with improved error handling and reconnect
if __name__ == "__main__":
    try:
        bot.run(token, log_handler=handler, log_level=logging.DEBUG, reconnect=True)
    except discord.errors.HTTPException as e:
        if e.status == 429:
            print("Rate limited (429). Waiting before retry...")
            logging.error("Discord rate limited, bot will retry after cooldown.")
        raise
    except KeyboardInterrupt:
        print("Bot shutting down...")
    except Exception as e:
        print(f"Bot error: {e}")
        logging.exception("Unexpected error in bot")