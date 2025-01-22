import discord

# Your Discord bot token
TOKEN = "MTMyzM2ODQ4MTg0Mg.GcSHTG.RayztstvXklEkbK8qQ0df1j7DO02kh1Sq90J0w"  # Replace with your bot's token

# Target user's ID to monitor
TARGET_USER_ID = 294882584201003009

# List of channel IDs to monitor
MONITOR_CHANNEL_IDS = [
    1327683294309126164, 1321860148360122519, 1321854177546207286
]

# Notification channel ID
NOTIFICATION_CHANNEL_ID = 1331221307920093270

# Configure bot intents
intents = discord.Intents.default()
intents.message_content = True  # Enable the message content intent
intents.reactions = True  # Enable reactions intent

# Initialize the bot client
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    """Triggered when the bot successfully logs in."""
    print(f"Bot is online as {client.user}")

@client.event
async def on_message(message):
    """Triggered when a message is sent in a channel."""
    # Ignore the bot's own messages
    if message.author == client.user:
        return

    # Check if the message is from the target user and in monitored channels
    if message.author.id == TARGET_USER_ID and message.channel.id in MONITOR_CHANNEL_IDS:
        # Fetch the notification channel
        notification_channel = client.get_channel(NOTIFICATION_CHANNEL_ID)

        if notification_channel:  # Ensure the notification channel exists
            try:
                # Forward the message content to the notification channel with @everyone
                await notification_channel.send(
                    f"@everyone {message.author.mention} posted:\n"
                    f"Message: {message.content}\n"
                    f"Original Channel: {message.channel.mention}\n"
                    f"Jump to Message: {message.jump_url}"
                )
                print("Message forwarded successfully!")
            except Exception as e:
                print(f"Error while sending notification: {e}")

@client.event
async def on_reaction_add(reaction, user):
    """Triggered when a reaction is added to a message."""
    if user.id == TARGET_USER_ID and reaction.emoji == "✅":
        try:
            # React with ✅ to the same message the target user reacted to
            await reaction.message.add_reaction("✅")
            print("Bot added ✅ reaction!")
        except Exception as e:
            print(f"Error while adding reaction: {e}")

# Run the bot
try:
    client.run(TOKEN)
except discord.LoginFailure:
    print("Logined succesfully to your self bot .")
except Exception as e:
    print(f"An unexpected error occurred: {e}"
