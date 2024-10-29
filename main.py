import os, asyncio, datetime
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response
from glenda import Glenda

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)


# # # MESSAGE FUNCTIONALITY

async def send_message(message, user_message):
    if not user_message:
        print("Message was empty because intents were not enabled properly")
        return
    
    # if user message is empty
    if user_message[0] == "?": 
        user_message = user_message[1:]

        try:
            response = await get_response(user_message)
            await message.author.send(response) if user_message[0] == "?" else await message.channel.send(response)

        except Exception as e: 
            print(e)
    elif user_message[0] == ".":
        user_message = user_message[1:]

        try:
            response = await get_response(user_message)
            await message.channel.send(response)

        except Exception as e: 
            print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} är här nu!')
    await  morning_schedule()

@client.event
async def on_message(message:Message) -> None:
    if message.author == client.user:
        return
    
    username = str(message.author)
    user_message = message.content
    channel = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}')

    await send_message(message, user_message)


async def morning_schedule():
    channel_id = 1275784441503027202
    channel = client.get_channel(channel_id)

    while True:
        now = datetime.datetime.now()
        
        # If it's already past 7 AM today, schedule for tomorrow's 7 AM
        if now.hour >= 7:
            then = (now + datetime.timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0)
        else:
            
            then = now.replace(hour=7, minute=0, second=0, microsecond=0)
        
        wait_time = (then - now).total_seconds()
        await asyncio.sleep(wait_time)

        # Check if today is a weekday (Monday is 0, Sunday is 6)
        if now.weekday() < 5:  # 0 (Monday) to 4 (Friday) are weekdays
            # Fetch the schedule before sending the message
            todays_schedule = Glenda.summarize_schedule()
            await channel.send(todays_schedule)

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
 


