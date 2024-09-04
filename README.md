# Discord Guild Bot
A versatile bot offering moderation tools, activity features, and enhancing the overall chat atmosphere.

## About This Project
This bot is designed to serve a community of around 100 people. The original intention was to log the leaving messages that cannot be accessed directly in Discord. Through extensive user feedback and requirement gathering, the project evolved to include a variety of features tailored to the community's needs.

I engaged with users to understand their points and desires, conducting surveys and discussions to gather detailed requirements. This collaborative approach ensured that the bot not only met but exceeded user expectations.

The bot primarily uses `commands.Cog` to modularize every function, ensuring a clean and maintainable codebase. This modular design allows for hot fixes, easy updates, testing, prototyping, and the addition of new features based on user feedback. By prioritizing user experience and maintaining a flexible architecture, the bot continues to adapt and grow with the community it serves.

## Features
- **Moderation Tools**:
    - Log messages, joins, and leaves

- **Activity Features**:
    - Custom commands for games and fun activities
    - Schedule gatherings and events

- **Chat Enhancement**:
    - Welcome messages for new members
    - Responses to specific keywords
    - Customizable chat commands to enhance interaction

## Working On
- **Keyword-Based Notifications**: Implementing a system to notify users based on specific keywords in messages.
- **Personal Leave Record**: Developing a feature to track and log personal leave records for users.
- **Appointment Booking**: Creating a scheduling system for booking appointments within the community.
- **Text-To-Speech (TTS) Features**: Adding TTS capabilities to enhance accessibility and user experience.
- **ChatGPT Conversations**: Integrating ChatGPT for more interactive and intelligent conversations.

## Getting Started
### Prerequisites
- Python 3.8 or higher
- `discord.py` library
- Other dependencies listed in `requirements.txt`

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/discord-guild-bot.git <<<<<<<<<<<<<<<<
    cd discord-guild-bot
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    - Create a `.env` file in the root directory
    - Reference the `.env.example` and fill in the necessary information
    - Check `config.py` and make any adjustments if needed

4. Customize the messages:
    - Check json files under `messages/<language>` and make adjustments to meet requirements

### Running the Bot
To start the bot, run the run.bat

## Project Structure
```
GuildBot/
│
├─ cogs/
│  ├─ bot_manager.py
│  ├─ extension_manager.py
│  ├─ member_event.py
│  └─ message_handler.py
│
├─ messages/
│  ├─ en/
│  │  ├─ all.json
│  │  ├─ any.json
│  │  ├─ bot.json
│  │  ├─ event.json
│  │  └─ vip.json
│  │
│  └─ zh-tw/
│     ├─ all.json
│     ├─ any.json
│     ├─ bot.json
│     ├─ event.json
│     └─ vip.json
│
├─ .env
├─ config.py
├─ guild_bot.py
├─ main.py
├─ README.md
├─ requirements.txt
├─ run.bat
└─ utilities.py
```

## References
- discord.py Documentation [Link](https://discordpy.readthedocs.io/en/latest/index.html)
- NumPy Style Docstrings [Link](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html)
