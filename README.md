# astra2

---

hi! i'm astra, the creator of astra2. astra2 is my bot, it does bot stuff; here's a neat list of features:

- asks and forwards any youtube, spotify, reddit, twitter, and wikipedia link i send to another bulletin like channel
- reminders for taking drugs
- channel join requests

---

how to host this yourself:

1. install dependencies in `requirements.txt`

2. make a slack bot and fill in this .env template
```dotenv
SLACK_TOKEN=
SLACK_SECRET=

MEDIA_TARGET_USER=
MEDIA_TARGET_CHANNEL=
MEDIA_FROM_CHANNELS=

TIMEZONES=
REMINDER_CHANNEL=
```

**Media forwarding:**
`MEDIA_TARGET_USER` are the Slack IDs of users who the bot will target forwarding from; list separated by commas (e.g. `MEDIA_TARGET_USER=U123456789,U098765432`)
`MEDIA_TARGET_CHANNEL` is the Slack ID of the channel which the bot will forward the messages to
`MEDIA_FROM_CHANNELS` are the Slack IDs of the channels in which the bot will check. The bot must be invited to said channel for this to work. List separated by commas

**Annoying-ass timed reminder thing**
`REMINDER_CHANNEL` is the channel where you'll be reminded in.

3. go to `app.py` and fill these in with your own things
```python
mediaTargetUser = ["Users the bot forwards from"]
mediaTargetChannel = "Channel bot sends to"
mediaTargetFromChannel = ["Channels bot forwards from"]
```

4. run `app.py`