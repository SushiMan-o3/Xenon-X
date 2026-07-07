# Overview
**⚠️ This is an outdated, unmaintained Discord bot.** It runs on discord.py v1.7.3, which is several major versions behind and no longer supported. It's kept here for reference/archival purposes only.

It has a currency system, a logging system, various moderation commands, and various other commands.

This bot was made for the ThIng servers made for me and my friends, but feel free to use it for your own personal use. Ensure that you change the user ids, channel ids,
and various others things that has been personalized for the server. 

# Note:
This project is no longer actively updated. discord.py has changed significantly since v1.7.3 (including the move to v2.x with breaking API changes), so expect this bot to require substantial rework before it runs on a current version.

# Setup
1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Open `config.py` and fill in:
   - `token` — your bot's token from the Bot tab at discord.com/developers/applications
   - `prefix` — the command prefix (e.g. `!`)
   - The Reddit API credentials (`client_id`, `client_secret`, `username`, `password`, `user_agent`) from reddit.com/prefs/apps
3. Update the hardcoded IDs personalized for the original server (e.g. the error log channel ID in `main.py`) to match your own server.
4. Run the bot:
   ```
   python main.py
   ```
