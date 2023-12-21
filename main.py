from TelegramBot.TelegramBot import TelegramBot

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

def main():
    t = TelegramBot()
    t.start_bot()

if __name__ == "__main__":
    main_test()