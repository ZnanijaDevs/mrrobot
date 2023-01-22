## mrrobot

[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

This project is a bot specifically for use with the Znanija.com workspace in Slack.
The bot has several important features for the workspace, such as deleting messages by emoji, logging deleted messages, and forwarding messages to different channels.

### Setup
You will need a Slack workspace and a bot account to test your changes to the bot.
You can create a bot [here](https://api.slack.com/).

Here is an example configuration file (App Manifest)
```yml
display_information:
  name: MrRobot
  description: Je pense, donc je suis...
  background_color: "#0057b7"
features:
  bot_user:
    display_name: MrRobot
    always_online: true
oauth_config:
  scopes:
    user:
      - search:read
      - chat:write
      - reactions:write
    bot:
      - channels:history
      - chat:write
      - groups:read
      - im:write
      - reactions:read
      - reactions:write
      - users:read
      - groups:history
settings:
  event_subscriptions:
    bot_events:
      - message.channels
      - reaction_added
  interactivity:
    is_enabled: true
  org_deploy_enabled: false
  socket_mode_enabled: true
  token_rotation_enabled: false
```

#### Configure
Set the `ENV` environment variable.
Then you will have to create `.env` / `.env.production`.

```yml
ENV: production # or development

# Slack config
SLACK_APP_TOKEN: "xapp-..."
SLACK_BOT_TOKEN: "xoxb-..."
SLACK_ADMIN_TOKEN: "xoxp-..."
SLACK_SIGNING_SECRET: "..."
HELP_CHANNEL_ID: "C353BRQAZ"
TODELETE_CHANNEL_ID: "C2P3PR98V"
ANTISPAMERS_CHANNEL_ID: "C02DE6LKQLR"
MODERATORS_CHANNEL_ID: "C03KLBS5S94"

REDIS_DB_URL: "redis://user:pass@host.com:12957/0"
ZNANIJA_API_GATEWAY_AUTH_TOKEN: "..."
ZNANIJA_API_GATEWAY_HOST: "https://gtwy.example.com"

# Use Sentry in production mode only
SENTRY_DSN: "..."

# Logs
LOG_SHEETS_ID: "<id>"
```
Then create `secrets.py` in `mrrobot/config` directory and set the Google Service Account credentials.
```py
GOOGLE_SERVICE_ACCOUNT = {}
```

### Run the bot locally
```bash
$ export ENV=production
$ py run.py
```