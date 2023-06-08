import asyncio

from pywebio.output import put_text

chat_msgs = []
online_users = set()
MAX_MESSAGES_COUNT = 100


async def refresh_msg(nickname, msg_box):
    global chat_msgs
    last_idx = len(chat_msgs)

    while True:
        await asyncio.sleep(1)

        for m in chat_msgs[last_idx:]:
            if m[0] != nickname:
                put_text(f"`{m[0]}`: {m[1]}")

        if len(chat_msgs) > MAX_MESSAGES_COUNT:
            chat_msgs = chat_msgs[len(chat_msgs) // 2:]

        last_idx = len(chat_msgs)
