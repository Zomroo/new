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
async def ban_command(client, message):
    # Get the user ID of the user who sent the command
    user_id = message.from_user.id

    # Check if the bot is an admin
    chat_member = await client.get_chat_member(message.chat.id, "me")
    if chat_member.status not in ("administrator", "creator"):
        # The bot is not an admin, so send an error message
        await message.reply("I am not an admin in this chat.")
        return

    # Check if the user who sent the command has ban rights
    user_member = await client.get_chat_member(message.chat.id, user_id)
    if user_member.status not in ("administrator", "creator"):
        # The user does not have ban rights, so send an error message
        await message.reply("You do not have permission to ban users.")
        return

    # Extract the user ID and reason from the message
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    # Check if a valid user ID is extracted
    if not user_id:
        await message.reply("I can't find that user.")
        return

    # Check if the user is trying to ban the bot itself
    if user_id == bot.get_me().id:
        await message.reply("I can't ban myself, I can leave if you want.")
        return

    # Check if the user is trying to ban an admin
    chat_admins = await client.get_chat_members(message.chat.id, filter="administrators")
    admin_ids = [admin.user.id for admin in chat_admins]
    if user_id in admin_ids:
        await message.reply("I can't ban an admin.")
        return

    # Ban the user
    await client.ban_chat_member(message.chat.id, user_id)

    # Send a confirmation message
    await message.reply(f"User {user_id} has been banned.")

# Start the bot
bot.run()
