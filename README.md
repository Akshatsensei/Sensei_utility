# Sensei Utility Bot

A Discord bot utility for server management with moderation features.

## Features
- Auto-welcome messages for new members
- Profanity filtering
- Moderation commands (kick, ban, timeout)
- User immunity system
- Slash commands support

## Requirements
- Python 3.8+
- discord.py
- python-dotenv

## Setup

1. Clone the repository:
```bash
git clone https://github.com/Akshatsensei/Sensei_utility.git
cd Sensei_utility
```

2. Create a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Add your Discord bot token to `.env`:
```
DISCORD_TOKEN=your_token_here
```

6. Run the bot:
```bash
python main.py
```

## Deployment

### Render
1. Connect your GitHub repository to Render
2. Create a new "Background Worker" service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `python main.py`
5. Add environment variable: `DISCORD_TOKEN=your_token`

### Termux
```bash
pip install -r requirements.txt
python main.py
```

## Commands
- `/ping` - Check bot response
- `/hello` - Say hello
- `/clear [amount]` - Delete messages (Manage Messages required)
- `/immune [member]` - Make user immune (Administrator only)
- `/unimmune [member]` - Remove immunity (Administrator only)
- `/kick [member] [reason]` - Kick a member
- `/ban [member] [reason]` - Ban a member
- `/timeout [member] [minutes]` - Timeout a member

## License
MIT License
