# Discord Bot
A versatile bot offering moderation tools, enhancing the overall chat atmosphere, and retrieving real-time information by calling external APIs.

## About This Project
This bot is designed to serve a community of around 100 people. The original intention was to log the leaving messages that cannot be accessed directly in the Discord client. Through extensive user feedback and requirement gathering, the project evolved to include a variety of features tailored to the community's needs.

The bot primarily uses `discord.commands.Cog` to modularize every group of functions as plugins, ensuring a clean and maintainable codebase. This modular design allows hot fixes & hot plugging, easy updates, testing, prototyping, and the addition of new features based on user feedback. By prioritizing user experience and maintaining a flexible architecture, the bot continues to adapt and grow with the community it serves.

## Features
- **Core functions**:
    - Bot control
    - Plugins management
    - Commands management

- **Moderation Tools**:
    - Log messages 
    - Onboard guidance
    - Reaction roles

- **Chat Enhancement**:
    - Keyword trigger interactions
    - User-based interactions

- **Community Applications**:
    - Game market reports

## Deployment Guide
### Prerequisites
1. Discord client, download from [Discord](https://discord.com/)
2. Discord server, create in Discord client following these steps:
    1. Add a server 
    2. Create My Own
    3. For a club or community
    4. Enter server name
    5. Create
3. Discord application, create at [Discord Developer Portal](https://discord.com/developers/applications)
4. After creation, configure the access rights of the Bot following these steps:
    1. Click on OAuth2 tab
    2. Check `bot` box under Scopes of OAuth2 URL Generator
    3. Check `Administrator` box under Bot Permissions (development only)
    4. Scroll down to the generated URL and add the bot to the Discord server
    5. Click on Bot tab
    6. Enable `Server Members Intent`, `Message Content Intent` and check `Administrator` under Bot Permissions

Choose to use Docker for containerized deployment or set up locally.

## Method 1: Deploying with Docker
1. Ensure Docker is installed
    ```bash
    docker version
    ```
2. Clone the repository and navigate into the project directory
    ```bash
    git clone https://github.com/RyanYCT/discord-bot.git
    cd discord-bot
    ```
3. Setting Up Environment Variables and Discord Community Server
    <details>

    ### Setting Up Environment Variables
    1. Locate the `.env.example` in the root of the project
    2. Create a new `.env` file in the root of the project
    3. Copy contents from `.env.example` to `.env`
    4. Replace the placeholders in `.env` with the actual information and credentials

    ### Setting Up Community Server
    All the channel and role settings must be registered in `settings.py` to take effect.

    A few channels are required for the bot to function well:
    1. A `log channel` for moderator functions and log messages
    2. A `welcome channel` for welcome messages and guidance

    Some functions perform better and are managed easier if assigned a channel for them (Optional):
    1. A `role channel` for member self-assign role function
    2. A `conference channel` for undisturbed discussion

    Some commands can only be executed by specific roles:
    1. `admin role` has permission to execute moderator commands and access the log channel
    2. `tester role` has permission to execute moderator commands
    3. `member role` has restricted permission to execute commands and access channels
    4. `subscriber role` has permission to execute get report commands

    Other roles' permissions and access rights are fully customizable depending on the use case.
    </details>
4. Build and run the Docker container
    ```bash
    docker-compose up --build
    ```

## Method 2: Local Setup
### Installation
1. Ensure Python 3.10 or higher is installed
    ```bash
    python --version
    ```
2. Clone the repository and navigate into the project directory
    ```bash
    git clone https://github.com/RyanYCT/discord-bot.git
    cd discord-bot
    ```
3. Create a virtual environment
    ```bash
    python -m venv .venv
    ```
4. Activate the virtual environment
    ```bash
    .venv\Scripts\activate
    ```
5. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```
6. Setting Up Environment Variables and Discord Community Server
    <details>

    ### Setting Up Environment Variables
    1. Locate the `.env.example` in the root of the project
    2. Create a new `.env` file in the root of the project
    3. Copy contents from `.env.example` to `.env`
    4. Replace the placeholders in `.env` with the actual information and credentials

    ### Setting Up Community Server
    All the channel and role settings must be registered in `settings.py` to take effect.

    A few channels are required for the bot to function well:
    1. A `log channel` for moderator functions and log messages
    2. A `welcome channel` for welcome messages and guidance

    Some functions perform better and are managed easier if assigned a channel for them (Optional):
    1. A `role channel` for member self-assign role function
    2. A `conference channel` for undisturbed discussion

    Some commands can only be executed by specific roles:
    1. `admin role` has permission to execute moderator commands and access the log channel
    2. `tester role` has permission to execute moderator commands
    3. `member role` has restricted permission to execute commands and access channels
    4. `subscriber role` has permission to execute get report commands

    Other roles' permissions and access rights are fully customizable depending on the use case.
    </details>
7. Start the Bot
    After initialization, choose to start:
    - by running the command
        ```bash
        python main.py
        ```
    - or by running the `run.bat` script

## Core functions
In general, the cogs listed in `settings.cogs` will be loaded when the bot is started. Some of the following functions provide hot plugging features to partially update, hot fix without shutting down or rebooting the bot.

In `bot_manager` that contains some top-level control functions:
- `sync`: for manually syncing the commands to Discord if new commands do not show in the Discord client.
- `shutdown`: shut down the bot from the Discord client.
- `loaded_cogs`: show all cogs that are loaded in the bot.
- `set_activity`: change the online status and customize the activity of the bot.

In `extension_manager` that contains hot plugging features:
- `load`: load an extension into the bot.
- `unload`: unload an extension from the bot.
- `reload`: reload an extension in the bot.

## Moderation Tools
Handy tools for community moderators, providing advanced logging which cannot be accessed directly in the Discord client, sending on behalf of moderators, and offering self-assigned roles.

In `member_event` that contains monitoring tools and reactions to activities:
- `on_member_join`: send a log message and welcome message to guide the new member to complete the onboarding procedures.
- `on_member_update`: send a log message recording the rename history of that member.
- `on_raw_member_remove`: send a log message when detecting a member leaves the community.
- `on_raw_reaction_add`: assign a role to a member when they react to the self-assign post.
- `on_raw_reaction_remove`: remove a role from a member when they intend to remove their self-assigned role.

In `message_handler` that contains message handling and interaction tools:
- `forward`: send a message by the bot on behalf of a moderator.
- `react_emoji`: add emojis to a message by the bot on behalf of a moderator.
- `announce`: send a predefined embed announcement by the bot on behalf of a moderator.
- `edit_embed`: edit a specified embed message sent by the bot.

## Chat Enhancement
Basically, the bot would react to messages sent in all channels within the community.

For handling inquiries, all match wording is set to have the highest response priority. The second is set for the VIP users, and the last is for any keywords.

In some situations, the bot could be triggered and interrupt the conversation unexpectedly. For example, in the conference channel. So, in `settings.py` there are some configurations to exclude channels which are "Do Not Disturb".

In `message_handler` that contains message handlers:
- `on_message`: respond to messages based on the conditions and settings.

## Community Applications
The bot offers commands to call from the Discord client to retrieve data from an external API server and present it in a Discord embed format message.

The external API server is configured in `settings.py`.

In `report_manager` that contains format tools and request commands:
- `generate_report`: generate a Discord embed message based on the provided data and report template.
- `report`: fetch the latest report from the API server, construct the report with tools, and present it.

## Customize the Bot
### Log and Informational Messages
The predefined log, informational messages, and report templates are under `languages/<lan>/templates`.

They are classified into `bot`, `event`, `embed`, `item_report`, and `overall_report` in JSON format.

### Reaction Role / Self Assign Role
To enable reaction role, follow these steps:
1. Choose or send a message as a reaction container
2. Copy that message id to `ROLE_MESSAGE_ID` in `.env`
    - Everyone react to that message with 🔔 will be assigned a subscriber role

To customize reaction role, follow these steps:
1. Create a new role in community
2. Add the role id to `<ROLENAME>_ROLE_ID` in `.env`
3. Add the role id and corresponded emoji to guild information under `settings.py`

### Keyword Based Messages
The trigger keywords, chances, and reply messages are under `languages/<lan>/keywords`.

They are classified into `all`, `any`, and `vip` in JSON format.

This bot supports three types of replies to enhance its interaction capabilities and provide more customized responses.

1. All keywords
    - Defined in `all.json`
    - Responds only when **all** specified keywords are present in the user's message.
    - Ensures that the reply is highly relevant to specific inquiries.
2. Any keywords
    - Defined in `any.json`
    - Responds when **any** specified keywords are present in the user's message.
    - Provides a more flexible and responsive interaction for broader topics.
3. User specific
    - Defined in `vip.json`
    - Responds to specific users, including but not limited to messages sent by the user, being mentioned, mentioning others, specified keywords, etc.
    - Provides tailored replies based on their preferences, past interactions, or predefined settings.
