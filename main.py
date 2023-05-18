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

# Add a command handler for /adminrights
@bot.on_message(filters.command("adminrights"))
async def adminrights(client, message):
    # Get all chat members
    chat_members = await client.get_chat_members(message.chat.id)

    # Check if the bot is an admin
    for member in chat_members:
        if member.user.id == bot.get_me().id:
            # The bot is an admin
            await message.reply("I am an admin in this chat.")
            return

    # The bot is not an admin
    await message.reply("I am not an admin in this chat.")

# Start the bot
bot.run()
