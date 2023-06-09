import pyrogram
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus

# API ID, bot token, and API hash
api_id = 14091414
bot_token = '5615528335:AAHOlk2j2TE5CWOv24mxBwpBMAx2ui3Zv1k'
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'

# Initialize Pyrogram
bot = pyrogram.Client(
    "my_bot",
    api_id=api_id,
    bot_token=bot_token,
    api_hash=api_hash,
)


# Define the ban command
@bot.on_message(filters.command("ban"))
async def ban_command(client, message):
    # Get the user ID of the user who sent the command
    user_id = message.from_user.id

    # Check if the bot is an admin
    chat_member = await client.get_chat_member(message.chat.id, "me")
    if chat_member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        # The bot is not an admin, so send an error message
        await message.reply("I am not an admin in this chat.")
        return

    # Check if the user who sent the command has ban rights
    user_member = await client.get_chat_member(message.chat.id, user_id)
    if user_member.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
        # The user does not have ban rights, so send an error message
        await message.reply("You do not have permission to ban users.")
        return

    # Ban the user
    await client.ban_chat_member(message.chat.id, user_id)

    # Send a confirmation message
    await message.reply(f"User {user_id} has been banned.")


# Start the bot
bot.run()
