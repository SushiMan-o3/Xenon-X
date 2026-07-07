import praw

# Discord bot token, from the Bot tab of your application at discord.com/developers/applications
token = ''

# Prefix used to invoke commands in chat, e.g. '!' lets users run '!help'
prefix = ''

# Reddit API credentials, from your app at reddit.com/prefs/apps
reddit = praw.Reddit(
        client_id = 'bot id',           # the ID string under your app's name on reddit.com/prefs/apps
        client_secret = 'client sercert',  # the 'secret' string shown next to your app
        username = 'Account username',  # Reddit account the app is registered under
        password = 'Account password',  # password for that Reddit account
        user_agent = 'Reddit bot name by account username')  # descriptive string, e.g. 'XenonX bot by u/yourname'
