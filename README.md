# TechCognita Discord Bot

## Description

TechCognita Discord Bot is a versatile bot designed to enhance your Discord server experience. It comes packed with various features and commands spanning different categories such as administration, fun, moderation, tech news, and utilities.

## Features

- **Administration:** Commands for managing your server, such as viewing server statistics.
- **API Integration:** Integration with various APIs to provide random facts, jokes, and quotes.
- **Events:** Automated greetings and chatbot functionality powered by OpenAI.
- **Fun Commands:** Entertaining commands like coin flips, dice rolls, and message repetition.
- **Moderation:** Commands for moderating your server, including banning, kicking, and message clearing.
- **Tech News:** Automatic fetching and posting of tech news from popular sources.
- **Utility Commands:** Handy utilities like avatar display, member count, embed creation, and nickname management.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Atharvshinde2004/TechCognita-Bot.git
   cd TechCognita-Bot
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Discord bot token:
   - Create a `bot_functions.py` file in the root directory.
   - Define your bot token in the file:

     ```python
     Token = "YOUR_BOT_TOKEN_HERE"
     ```

## Usage

1. Run the bot:

   ```bash
   python Main.py
   ```

2. Invite the bot to your Discord server:
   - Use the invite link generated by your bot to invite it to your server.
   - Make sure to grant necessary permissions for the bot to function properly.

## Configuration

- **Prefix:** The default command prefix is `!!`. You can modify it in the `Main.py` file.
- **Channel IDs:** Update the channel IDs in respective cog files to ensure commands work correctly.

## Contributors

- [Atharv Shinde](https://github.com/Atharvshinde2004)
- [Akshad Jogi](https://github.com/akshadjogi)

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Discord.py](https://github.com/Rapptz/discord.py)
- [OpenAI](https://openai.com/)
- [Feedparser](https://github.com/kurtmckee/feedparser)
- [Requests](https://github.com/psf/requests)
- [Python](https://www.python.org/)
