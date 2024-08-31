## Installation
`pip install -r /path/to/requirements.txt`

## Design
Make use of discord.ext.commands.Cog to modularize everything.

## File Structure
GuildBotII/
│
├─ assets/
│   ├─ img/
│
├─ cogs/
│   ├─ bot_manager.py
│   ├─ extension_manager.py
│   ├─ member_event.py
│   ├─ message_handler.py
│   └─ music.py (Pending)
│
├─ config/
│   └─ settings.py
│
├─ data/
│
├─ logs/
│   └─ discord.log
│
├─ messages/
│   ├─ chat/
│   │   ├─ keyword.json
│   │   └─ reply.json
│   │
│   ├─ bot_message.json
│   ├─ event_message.json
│   ├─ extension_message.json
│   └─ woof_message.json
│
├─ src/
│   └─ utilities.py
│
├─ .env
├─ guild_bot.py
└─ main.py

## Working on
- Update docstrings to NumPy style

## To do
- cogs/message_handler (normal keyword)

## To test
- cogs/woof.echo_i
- cogs/woof.list_commands
- cogs/woof.activity
- cogs/extension_manager.

###
─ │ ├─ └─ ┐ ┌

### Example NumPy Style Python Docstrings
reference: https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_numpy.html
