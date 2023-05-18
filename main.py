import pyrogram

# API ID, bot token, and API hash
api_id = 14091414
bot_token = 1e26ebacf23466ed6144d29496aa5d5b
api_hash = 5615528335:AAHOlk2j2TE5CWOv24mxBwpBMAx2ui3Zv1k

# Initialize Pyrogram
bot = pyrogram.Client(
    "my_bot",
    api_id=api_id,
    bot_token=bot_token,
    api_hash=api_hash,
)

# Add a command handler for /ban
@bot.on_message(command("ban"))
async def ban(message):
    # Check if the bot is an admin
    if not bot.is_admin(message.chat.id):
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
    await bot.ban_chat_member(message.chat.id, username)

    # Delete the command
    await message.delete()

# Start the bot
bot.start()

# Run the bot forever
bot.run_forever()
