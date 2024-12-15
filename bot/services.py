
def create_auth_telegram_link(user_token: str, tg_bot_name: str):
    return f'https://t.me/{tg_bot_name}?start={user_token}'
