from pyrogram import Client, filters
from pyrogram.raw import functions
from pyrogram.raw.types import ChatAdminRights

# Add your API ID and bot token here
api_id = 14091414
api_hash = '1e26ebacf23466ed6144d29496aa5d5b'
bot_token = '5615528335:AAHOlk2j2TE5CWOv24mxBwpBMAx2ui3Zv1k'

# Create a Pyrogram client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Check if the user is an admin and has rights to ban users
async def check_ban_rights(user, chat):
    admin_rights = await app.send(functions.channels.GetParticipant(
        channel=chat.id,
        participant=user.id
    ))
    if isinstance(admin_rights.participant, ChatAdminRights):
        return True
    else:
        return False

# Check if the bot is an admin in the group
def check_bot_admin(chat_id):
    bot_member = app.get_chat_member(chat_id, "me")
    if not bot_member.status == "administrator":
        raise Exception("I don't have enough rights to perform this action.")

# Handle the /ban command
@app.on_message(filters.command("ban") & filters.group)
async def ban_user(client, message):
    try:
        # Check if the user issuing the command has the right to ban users
        if await check_ban_rights(message.from_user, message.chat):

            # Check if the bot is an admin in the group
            check_bot_admin(message.chat.id)

            # Check if the command has a reply message or a mentioned username
            if message.reply_to_message:
                user_id = message.reply_to_message.from_user.id
            elif len(message.command) > 1:
                user_id = message.command[1]
            else:
                await message.reply_text("Please reply to a message or provide a username to ban.")
                return

            # Ban the user
            await client.kick_chat_member(message.chat.id, user_id)
            await message.reply_text("User has been banned.")
            await message.delete()

        else:
            await message.reply_text("You are not allowed to ban users in this chat.")

    except Exception as e:
        await message.reply_text(str(e))

# Add more command handlers for other functionalities...

# Start the bot
app.run()
