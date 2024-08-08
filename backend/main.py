from TelegramBot.TelegramBot import TelegramBot

from CustomLogger.CustomLogger import log_message

def read_env(path):
    with open(path) as f:
        lines = f.readlines()
    env = {}
    for line in lines:
        key, value = line.strip().split('=')
        env[key] = value
    return env

def main_test():
    env = read_env('.env')
    t = TelegramBot(token=env['TELEGRAM_TOKEN'])
    t.start_bot()
    # t.send_message()

def main():
    t = TelegramBot()
    t.start_bot()

if __name__ == "__main__":
    log_message('Bot is running')
    main()