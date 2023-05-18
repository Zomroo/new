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

# Define the ban command
@bot.on_message(filters.command("ban"))
async def ban(message):
    # Get the user ID of the user who sent the command
    user_id = message.from_user.id

    # Check if the bot is an admin
    if not bot.is_admin(message.chat.id):
        # The bot is not an admin, so send an error message
        await message.reply("I am not an admin in this chat.")
        return

    # Check if the user who sent the command has ban rights
    if not bot.get_chat_member(message.chat.id, user_id).status in ("administrator", "creator"):
        # The user does not have ban rights, so send an error message
        await message.reply("You do not have permission to ban users.")
        return

    # Get the user ID of the user to ban
    user_to_ban_id = message.text.split()[1]

    # Ban the user
    await bot.ban_chat_member(message.chat.id, user_to_ban_id)

    # Send a confirmation message
    await message.reply(f"User {user_to_ban_id} has been banned.")

# Start the bot
bot.run()
