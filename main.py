import pyrogram
from pyrogram import filters

# API ID, bot token, and API hash
api_id = 14091414
bot_token = '1e26ebacf23466ed6144d29496aa5d5b'
api_hash = '5615528335:AAHOlk2j2TE5CWOv24mxBwpBMAx2ui3Zv1k'

# Initialize Pyrogram
bot = pyrogram.Client(
    "my_bot",
    api_id=api_id,
    bot_token=bot_token,
    api_hash=api_hash,
)

# Add a command handler for /ban
@bot.on_message(filters.command("ban"))
async def ban(client, message):
    # Check if the bot is an admin
    chat_member = await client.get_chat_member(message.chat.id, "me")
    if not chat_member.status == "administrator" or not chat_member.can_restrict_members:
        await message.reply("I don't have enough rights to ban users.")
        return

    # Get the user who sent the command
    user = message.from_user

    # Check if the user is an admin
    if not user.is_admin:
        await message.reply("You are not allowed to ban users.")
        return

    # Get the username of the user to be banned
    username = message.text.split(" ")[1]

    # Ban the user
    try:
        await bot.kick_chat_member(message.chat.id, username)
        await message.reply("User has been banned.")
    except pyrogram.errors.FloodWait as e:
        # Handle the case when the bot is being rate-limited
        await message.reply(f"Rate-limited. Try again in {e.x} seconds.")

    # Delete the command
    await message.delete()

# Start the bot
bot.run()
