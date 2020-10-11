import click
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
from decouple import config


@click.command()
def teladduser():
    """Log in on a Telegram account and list all super group of it."""
    # Login on a Telegram account
    api_id = config('API_ID')
    api_hash = config('API_HASH')
    phone = config('PHONE')
    client = TelegramClient(phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        login_code = click.prompt('Enter the Login Code that was send to yor Telegram app: ', type=int)
        client.sign_in(phone, login_code)
    # Get all Groups of the logged user
    chats = []
    last_date = None
    chunk_size = 100
    groups = []
    result = client(
        GetDialogsRequest(
            offset_date=last_date,
            offset_id=0,
            offset_peer=InputPeerEmpty(),
            limit=chunk_size,
            hash=0
        )
    )
    # Get only the super group of the logged user
    chats.extend(result.chats)
    for chat in chats:
        try:
            if chat.megagroup:
                groups.append(chat)
        except:
            continue
    # Select a group to add users
    for i, g in enumerate(groups):
        print(f"{i} - {g.title}")
    g_index = click.prompt("Enter Number of Group you want add users: ", type=int)
    target_group = groups[int(g_index)]
    print(f'The selected group was: {target_group.title}')
