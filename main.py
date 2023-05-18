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
    # Get the chat member object for the bot
    chat_member = await client.get_chat_member(message.chat.id, "me")

    # Check if the bot is an admin
    if chat_member.status == "administrator":
        # The bot is an admin
        await message.reply("I am an admin in this chat.")

        # List all the admin rights that the bot has
        for right in chat_member.admin_rights:
            await message.reply(right)

    else:
        # The bot is not an admin
        await message.reply("I am not an admin in this chat.")

# Start the bot
bot.run()
