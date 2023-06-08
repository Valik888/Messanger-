from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import run_async, run_js

from authentication import authenticate_user
from chat import chat_msgs, online_users, refresh_msg
from registration import register_user


def registration_form():
    user_data = input_group("Реєстрація", [
        input("Username", name="username", required=True),
        input("First Name", name="first_name", required=True),
        input("Last Name", name="last_name", required=True),
    ])

    username = user_data["username"]
    first_name = user_data["first_name"]
    last_name = user_data["last_name"]

    put_text(f"Реєстрація успішна!\n\nUsername: {username}\nFirst Name: {first_name}\nLast Name: {last_name}")


async def main():
    put_markdown("Ви потрапили в онлайн чат!")

    user_id = user.id
    user = authenticate_user(user_id)

    if user is None:
        username = "username"
        first_name = "first_name"
        last_name = "last_name"

        register_user(user_id, username, first_name, last_name)
        user = authenticate_user(user_id)

    nickname = user.username
    online_users.add(nickname)

    msg_box = put_scope(name="chat_box")
    put_scrollable(msg_box, height=300, keep_bottom=True)

    nickname = await input("Войти в чат", required=True, placeholder="Ваш нік",
                           validate=lambda
                               n: "Такий нік вже використовується!" if n in online_users or n == '📢' else None)
    online_users.add(nickname)

    chat_msgs.append(('📢', f'`{nickname}` приєднався до чату!'))
    put_text(f'📢 `{nickname}` приєднався до чату')

    refresh_task = run_async(refresh_msg(nickname, msg_box))

    while True:
        data = await input_group("💭 Нове повідомлення", [
            input(placeholder="Текст повідомлення ...", name="msg"),
            actions(name="cmd", buttons=["Відправити", {'label': "Вийти з чату", 'type': 'cancel'}])
        ], validate=lambda m: ('msg', "Введіть текст повідомлення!") if m["cmd"] == "Відправити" and not m[
            'msg'] else None)

        if data is None:
            break

        put_text(f"`{nickname}`: {data['msg']}")
        chat_msgs.append((nickname, data['msg']))

    refresh_task.close()

    online_users.remove(nickname)
    toast("Ви вишйли з чату!")
    put_text(f'📢 Користувач `{nickname}` покинув чат!')
    chat_msgs.append(('📢', f'Користувач `{nickname}` покинув чат!'))

    put_buttons(['Перезайти'], onclick=lambda btn: run_js('window.location.reload()'))


if __name__ == "__main__":
    start_server(main, debug=True, port=8080, cdn=False)
