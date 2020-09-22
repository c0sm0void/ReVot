# ReVot
Reverse Image Search Telegram Bot Using MS Azure

<!-- toc -->

- [How to use me](#how-to-use-me)
- [Features:](#features)
- [Commands:](#commands)

  * [Local installation](#local-installation)

<!-- tocstop -->

## How to use me
Send me images or stickers and I will send you direct reverse image search links for IQDB, Google, TinEye, Yandex and
Bing. For anime images I recommend IQDB and TinEye, for other images I recommend to use Google Yandex, or TinEye.

## Features:
- Give you image reverse search links
- Supports IQDB, Google, TinEye, Yandex and Bing
- Supports normal images like JPG, PNG, WEBP
- Supports stickers
- Supports GIFs (can take some time till the GIFs are ready)
- Supports Videos (will be searched as GIFs)
- Best Match information by TinEye
- Best Match information by IQDB as fallback

## Commands:
- /help, /start: show a help message with information about the bot and it's usage.
- /best_match URL: Search for the best match on TinEye (and IQDB when nothing is found on TinEye). The `URL` is a link
    to an image

### Local installation
With this info we now install our virtualenv with:
```bash
pip install pipenv  # Install pipenv
pipenv --three      # Create virtualeenv from your python3 installation
pipenv install      # Install all requirements
pipenv shell        # Spawn shell for your pipenv virtualenv
```

After this is complete, you have to get an API Token from Telegram. You can easily get one via the
[@BotFather](https://t.me/BotFather).

Now that you have your API Token copy the `settings.example.py` to `settings.py` and paste in your API Token.
Finally you can use this to start your bot.
```bash
python run_bot.py
```

Thank you for using
