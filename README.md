# ReVot🤖 
Reverse Image Search Telegram Bot Using MS Azure (server maybe off)
[@ReVngx_bot](https://t.me/ReVngx_bot)

![](https://badgen.net/badge/icon/azure?icon=azure&label)
![](https://img.shields.io/badge/OS-Linux-informational?style=flat&logo=linux&logoColor=white&color=2bbc8a)
![](https://badgen.net/badge/icon/terminal?icon=terminal&label)
![](https://badgen.net/badge/icon/telegram?icon=telegram&label)
![](https://badgen.net/badge/icon/pypi?icon=pypi&label)

<!-- toc -->

- [How To Use Me❓](#how-to-use-me)
- [Features:✨](#features)
- [Commands:🧩](#commands)
  * [Local installation💻](#local-installation)
- [Errors and Fixes❌](#errors-and-fixes)

<!-- tocstop -->

## How To Use Me❓
Send me images, gif or stickers(non-animated), I will send you direct reverse image search links of IQDB, Google, TinEye, Yandex and
Bing. For anime images IQDB and TinEye, for other images I recommend to use Google, Bing and Yandex.

## Features:✨
- Give you image reverse search links
- Supports normal images like JPG, PNG, WEBP
- Supports stickers
- Supports GIFs (can take some time till the GIFs are ready)

## Commands:🧩
- /help, /start: show a help message with information about the bot and it's usage.
- /best_match URL: Search for the best match on TinEye (and IQDB when nothing is found on TinEye). The `URL` is a link
    to an image

### Local installation💻
With this info we now install our virtualenv with:
```bash
pip install pipenv  # Install pipenv
pipenv --three      # Create virtualeenv from your python3 installation
pipenv install      # Install all requirements
pipenv shell        # Spawn shell for your pipenv virtualenv
```

You have to get an API Token from Telegram. You can easily get one via the [@BotFather](https://t.me/BotFather).

Now that you have your API Token copy the `settings.example.py` to `settings.py` and paste in your API Token.
Finally you can use this to start your bot.
```bash
python run_bot.py
```
## Errors and Fixes❌
- Use [Python v3.6](https://www.python.org/downloads/release/python-360/) as default
- ssh-keyscan -H <IP address/Hostname> >> ~/.shh/known_hosts
- sudo -H pip install -U pipenv
