import discord
from discord.ext import commands

# Your Discord user token (self-bot usage is against Discord ToS; proceed at your own risk)
TOKEN = "MTAMDA.GQp708.bzMEHTGOVLhMc7Pk1xEeA9TMNbcmVaMBygyZ5Y"

# Target user's ID to monitor (the bot's ID)
TARGET_USER_ID = 1175575988390866976

# List of channel IDs to monitor
MONITOR_CHANNEL_IDS = [
    983748856506351616,
    742610029168951347,
    737394785135886346,
    750151448465113118,
    948449801165484052
]

# Notification channel ID
NOTIFICATION_CHANNEL_ID = 1330943553911787560

# Role ID to ping (Rain role)
RAIN_ROLE_ID = 1330943326773313717

# Initialize the bot client as a self-bot
client = commands.Bot(command_prefix="!", self_bot=True)

@client.event
async def on_ready():
    """Triggered when the bot successfully logs in."""
    print(f"Self-bot is online as {client.user}")

@client.event
async def on_message(message):
    """Triggered when a message is sent in a monitored channel."""
    # Ignore the bot's own messages
    if message.author == client.user:
        return

    # Check if the message is from the target bot and in monitored channels
    if message.author.id == TARGET_USER_ID and message.channel.id in MONITOR_CHANNEL_IDS:
        # Fetch the notification channel
        notification_channel = client.get_channel(NOTIFICATION_CHANNEL_ID)

        if notification_channel:  # Ensure the notification channel exists
            try:
                # Forward the message content to the notification channel with the Rain role ping
                await notification_channel.send(
                    f"<@&{RAIN_ROLE_ID}>\n"  # Ping the Rain role
                    f"Message: {message.content}\n"
                    f"Original Channel: {message.channel.mention}\n"
                    f"Jump to Message: {message.jump_url}"
                )
                print("Message forwarded successfully with Rain role ping!")

                # Automatically click the 💵 button if present
                for component in message.components:
                    for button in component.children:
                        if button.emoji.name == "💵":
                            await button.click()
                            print("💵 button clicked!")
                            break

            except Exception as e:
                print(f"Error while sending notification or interacting with button: {e}")

# Run the self-bot with your user token
try:
    client.run(TOKEN)  # No 'bot=False' needed here for self-bots
except discord.LoginFailure:
    print("Invalid token provided. Please check your user token.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
