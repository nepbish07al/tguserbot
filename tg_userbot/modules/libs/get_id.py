from telethon.tl.functions.users import GetFullUserRequest


async def get_id(event, userid):
    try:
        replied_user = await event.client(GetFullUserRequest(userid))
    except (TypeError, ValueError) as err:
        return str(err)
    return replied_user
