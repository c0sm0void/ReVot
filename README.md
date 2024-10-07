<div align="center">
  <h1 align="center" style="display: block; font-size: 3em; font-weight: bold; margin-block-end: 1em;"><strong>ReVot<img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Smileys/Robot.webp" alt="Robot" width="30" height="30" /></strong></h1>
  <p>Reverse Image Search Telegram Bot Using MS Azure/Local (server maybe off)
  <p>
    <img src="https://img.shields.io/github/stars/c0sm0void/ReVot?style=social"/>
    <img src="https://img.shields.io/github/forks/c0sm0void/ReVot?style=social"/>
    <img src="https://img.shields.io/github/watchers/c0sm0void/ReVot?style=social"/>
  <p>
    <a href="https://github.com/c0sm0void/ReVot/issues"><img src="https://custom-icon-badges.demolab.com/github/issues/c0sm0void/ReVot?label=Issues&labelColor=302d41&color=FF6347&logoColor=FF6347&logo=issue&style=for-the-badge" alt="GitHub Readme Profile Issues"/></a>
    <a href="https://github.com/c0sm0void/ReVot/pull"><img src="https://custom-icon-badges.demolab.com/github/issues-pr/c0sm0void/ReVot?&label=Pull%20requests&labelColor=302d41&color=98FF98&logoColor=98FF98&logo=git-pull-request&style=for-the-badge" alt="GitHub Readme Profile PRs"/></a>
    <a href="https://github.com/c0sm0void/ReVot/graphs/contributors"><img src="https://custom-icon-badges.demolab.com/github/contributors/c0sm0void/ReVot?label=Contributors&labelColor=302d41&color=c9cbff&logoColor=d9e0ee&logo=people&style=for-the-badge"/></a>
    <a href="https://t.me/ReVot_Local_Bot"><img src="https://img.shields.io/badge/Telegram%20ReVot%20Bot-blue?style=for-the-badge&logo=telegram&color=302d41&logoColor=0088CC" alt="Contact"/></a>
  <p>
    <img src="http://forthebadge.com/images/badges/made-with-python.svg"/>
    <img src="http://forthebadge.com/images/badges/license-mit.svg"/>
  <p>
    <img src="https://badgen.net/badge/icon/azure?icon=azure&label">
    <img src="https://img.shields.io/badge/OS-Linux-informational?style=flat&logo=linux&logoColor=white&color=2bbc8a">
    <img src="https://badgen.net/badge/icon/terminal?icon=terminal&label">
    <img src="https://badgen.net/badge/icon/pypi?icon=pypi&label">
    <img src="https://img.shields.io/badge/open%20source-%E2%9D%A4%EF%B8%8F-green">
</div>

---
<!-- tocstop -->

## How To Use Me: <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Telegram-Animated-Emojis/main/Smileys/Alien%20Monster.webp" alt="Alien Monster" width="25" height="25" />

Send me images, gifs or stickers(non-animated), I will send you direct reverse image search links of IQDB, Google, TinEye, Yandex and
Bing. For anime images IQDB and TinEye, for other images, I recommend using Google, Bing and Yandex.

## Features: <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Roller%20Coaster.png" alt="Roller Coaster" width="25" height="25" />

- Give you image reverse search links
- Supports normal images like JPG, PNG, WEBP
- Supports stickers
- Supports GIFs (can take some time till the GIFs are ready)

## Commands:🧩

- /help, /start: show a help message with information about the bot and its usage.
- /best_match URL: Search for the best match on TinEye (and IQDB when nothing is found on TinEye). The `URL` is a link
  to an image

## Local installation: <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/People%20with%20professions/Technologist%20Light%20Skin%20Tone.png" alt="Technologist Light Skin Tone" width="25" height="25" />

With this info, we now install our virtualenv with (check pre-installations file):

```bash
chmod +x pre-installations.sh
./pre-installations.sh
pip install pipenv  # Install pipenv
pipenv --version
git clone https://github.com/c0sm0void/ReVot.git
cd /ReVot
pipenv shell
pipenv install      # Install all requirements
```

You have to get an API Token from Telegram. You can easily get one via the [@BotFather](https://t.me/BotFather).

Now that you have your API Token, create a `settings.py` file and add one of the configurations below based on your preferred uploading method.

### Option 1: SSH Uploader

If you want to upload files using SSH, use the following configuration in your `settings.py`:

```python
TELEGRAM_API_TOKEN = 'Tel Bot Token By @BotFather'

UPLOADER = {
    'uploader': 'reverse_image_search_bot.uploaders.ssh.SSHUploader',
    'url': 'Host Domain Name',
    'configuration': {
        'host': 'Host IP (PUBLIC)',
        'user': 'Yourname',
        'password': 'Password',
        'upload_dir': '/path/to/ReVot/',
        'key_filename': '/path/to/.ssh/rsakey.pub (Public key)',
    }
}
```

### Option 2: File System Uploader

If you prefer to upload files from your local file system, use the following configuration in your `settings.py`:

```python
TELEGRAM_API_TOKEN = 'Tel Bot Token By @BotFather'

UPLOADER = {
    'uploader': 'reverse_image_search_bot.uploaders.file_system.FileSystemUploader',
    'url': 'Host Domain Name',
    'configuration': {
       'path': '/path/to/ReVot/',
    }
}
```

Finally, you can use this to start your bot.

```bash
python run_bot.py
```

## Errors and Fixes:❌

- Use [Python v3.12](https://www.python.org/downloads/) as default
- ssh-keyscan -H <IP address/Hostname> >> ~/.shh/known_hosts
- sudo -H pip install -U pipenv

## Techstack

### Programming Language:

- Python 3.12+

### Libraries:

- pipenv: For virtual environment and dependency management
- python-telegram-bot: For interacting with Telegram APIs
- Reverse Image Search Engines:
  - Google
  - Bing
  - Yandex
  - TinEye
  - IQDB

### Platform:

- MS Azure for hosting
- Ubuntu virtual machine for hosting

### Repository Structure: <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Activities/Crystal%20Ball.png" alt="Crystal Ball" width="25" height="25" />

```plaintext
ReVot/
│
├── .github/                  # GitHub-specific files
│   └── ISSUE_TEMPLATE/
│       ├── bug_report.md     # Template for reporting bugs
│       ├── custom.md         # Custom issue template
│       └── feature_request.md # Template for requesting features
│
├── deploy/                   # Deployment scripts and configurations
│   ├── after_push            # Post-deployment scripts
│
├── reverse_image_search_bot/ # Main bot directory
│   ├── uploaders/            # Uploader modules
│   │   ├── __init__.py       # Initialize uploaders package
│   │   ├── base_uploader.py   # Base class for uploaders
│   │   ├── file_system.py     # File system operations
│   │   └── ssh.py            # SSH related functions
│   │
│   ├── __init__.py           # Initialize bot package
│   ├── bot.py                # Main bot logic
│   ├── commands.py           # Command handling for the bot
│   ├── image_search.py       # Functions for reverse image search
│   ├── settings.example.py    # Example settings file for API tokens
│   ├── settings.example1.py   # Another example settings file
│   ├── utils.py              # Utility functions and helpers
│
├── LICENSE                   # License information
├── Pipfile                   # Pipenv dependencies
├── Pipfile.lock              # Locked dependency versions
├── README.md                 # Main project documentation
└── run_bot.py                # Script to run the bot
```

## License:📜

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
You are free to use, modify, and distribute this software as long as the original license and copyright notice are retained.

## <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Smilies/Beating%20Heart.png" alt="Beating Heart" width="25" height="25" /> Our Contributors

- We extend our heartfelt gratitude for your invaluable contribution to our project! Your efforts play a pivotal role in elevating ReVot to greater heights.
- Make sure you show some love by giving <img src="https://raw.githubusercontent.com/Tarikul-Islam-Anik/Animated-Fluent-Emojis/master/Emojis/Travel%20and%20places/Star.png" alt="Star" width="25" height="25" /> to our repository.

<div align="center">
<a href="https://github.com/c0sm0void/ReVot/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=c0sm0void/ReVot&&max=100&&anon=1" />
</a>
</div>

<!-- Made with [OSS Insight](https://ossinsight.io/) -->

<!-- toc -->
<table>
  <tr>
    <td>
      <a href="https://next.ossinsight.io/widgets/official/analyze-repo-pushes-and-commits-per-month?repo_id=297538974" target="_blank" style="display: block" align="center">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="https://next.ossinsight.io/widgets/official/analyze-repo-pushes-and-commits-per-month/thumbnail.png?repo_id=297538974&image_size=auto&color_scheme=dark" width="721" height="auto">
          <img alt="Pushes and Commits of c0sm0void/ReVot" src="https://next.ossinsight.io/widgets/official/analyze-repo-pushes-and-commits-per-month/thumbnail.png?repo_id=297538974&image_size=auto&color_scheme=light" width="721" height="auto">
        </picture>
      </a>
    </td>
    <td>
      <a href="https://next.ossinsight.io/widgets/official/compose-recent-top-contributors?repo_id=297538974" target="_blank" style="display: block" align="center">
        <picture>
          <source media="(prefers-color-scheme: dark)" srcset="https://next.ossinsight.io/widgets/official/compose-recent-top-contributors/thumbnail.png?repo_id=297538974&image_size=auto&color_scheme=dark" width="373" height="auto">
          <img alt="Top Contributors of c0sm0void/ReVot - Last 28 days" src="https://next.ossinsight.io/widgets/official/compose-recent-top-contributors/thumbnail.png?repo_id=297538974&image_size=auto&color_scheme=light" width="373" height="auto">
        </picture>
      </a>
    </td>
  </tr>
</table>
