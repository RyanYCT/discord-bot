# Discord Guild Bot
A versatile bot offering moderation tools, activity features, and enhancing the overall chat atmosphere.

## About This Project
This bot is designed to serve a community of around 100 people. The original intention was to log the leaving messages that cannot be accessed directly in Discord. Through extensive user feedback and requirement gathering, the project evolved to include a variety of features tailored to the community's needs.

I engaged with users to understand their points and desires, conducting surveys and discussions to gather detailed requirements. This collaborative approach ensured that the bot not only met but exceeded user expectations.

The bot primarily uses `discord.commands.Cog` to modularize every function as plug in, ensuring a clean and maintainable codebase. This modular design allows hot fixes, easy updates, testing, prototyping, and the addition of new features based on user feedback. By prioritizing user experience and maintaining a flexible architecture, the bot continues to adapt and grow with the community it serves.

## Features
- **Core functions**:
    - Bot control
    - Cogs management
    - Commands management

- **Moderation Tools**:
    - Log messages 
    - Reaction roles

- **Community Applications**:
    - Get game information reports
    - Make appointments

- **Chat Enhancement**:
    - Welcome messages
    - Keyword trigger interactions

## Working On
- **Event reminder**: A system for users to register notifications for upcoming events.
- **Notifications**: Implementing a system to notify users based on specific keywords in messages.
- **Appointment Booking**: Creating a scheduling system for booking appointments within the community.
- **Personal Leave Record**: Developing a feature to track and log personal leave records for users.
- **Text-To-Speech (TTS) Features**: Adding TTS capabilities to enhance accessibility and user experience.
- **ChatGPT Conversations**: Integrating ChatGPT for more interactive and intelligent conversations.

## Getting Started
### Prerequisites
- Python 3.10 or higher
- Other dependencies listed in `requirements.txt`
- Discord application

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/RyanYCT/discord-guild-bot.git
    git clone https://github.com/RyanYCT/discord-guild-bot.git
    cd discord-guild-bot
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your environment variables:
    - Create a `.env` file in the root directory
    - Reference the `.env.example` and fill in the necessary information
    - Check `settings.py` fill in your guild information and make any adjustments if needed

4. Customize the messages:
    - Check json files under `languages/<language>` and make adjustments to meet requirements


### Running the Bot
1. Create a discord application
    - Create at https://discord.com/developers/applications
    - Invite the bot to your guild

2. Prepare the bot working environment
    - Create a guild / server / group whatever you call
    - Create channels and record them at settings.guild

3. To start the bot, simply run the run.bat

## Project Structure
```
discord-guild-bot/
├─ cogs/
│  ├─ bot_manager.py
│  ├─ extension_manager.py
│  ├─ member_event.py
│  └─ message_handler.py
├─ languages/
│  ├─ en/
│  │  ├─ keywords/
│  │  │  ├─ all.json
│  │  │  ├─ any.json
│  │  │  └─ vip.json
│  │  └─ templates/
│  │     ├─ bot.json
│  │     ├─ embed.json
│  │     └─ event.json
│  └─ zh-tw/
│     ├─ keywords/
│     │  ├─ all.json
│     │  ├─ any.json
│     │  └─ vip.json
│     └─ templates/
│        ├─ bot.json
│        ├─ embed.json
│        └─ event.json
├─ .env
├─ guild_bot.py
├─ main.py
├─ README.md
├─ requirements.txt
├─ run.bat
├─ settings.py
└─ utilities.py
```
