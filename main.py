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
@bot.on_message(filters.command(["ban", "dban", "tban"]) & ~filters.private)
async def ban_command(client, message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)

    if not user_id:
        return await message.reply_text("I can't find that user.")
    if user_id == client.get_me().id:
        return await message.reply_text("I can't ban myself, I can leave if you want.")
    if user_id in SUDOERS:
        return await message.reply_text("You want to ban an elevated user? RECONSIDER!")
    if user_id in (await client.get_chat_administrators(message.chat.id)):
        return await message.reply_text("I can't ban an admin. You know the rules, so do I.")

    try:
        mention = (await client.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )

    msg = (
        f"**Banned User:** {mention}\n"
        f"**Banned By:** {message.from_user.mention if message.from_user else 'Anon'}\n"
    )

    if message.command[0][0] == "d":
        await message.reply_to_message.delete()

    if message.command[0] == "tban":
        split = reason.split(None, 1)
        time_value = split[0]
        temp_reason = split[1] if len(split) > 1 else ""
        temp_ban = await time_converter(message, time_value)
        msg += f"**Banned For:** {time_value}\n"

        if temp_reason:
            msg += f"**Reason:** {temp_reason}"

        try:
            if len(time_value[:-1]) < 3:
                await message.chat.ban_member(user_id, until_date=temp_ban)
                await message.reply_text(msg)
            else:
                await message.reply_text("You can't use more than 99.")
        except AttributeError:
            pass
        return

    if reason:
        msg += f"**Reason:** {reason}"

    await message.chat.ban_member(user_id)
    await message.reply_text(msg)


# Start the bot
bot.run()
