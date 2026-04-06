# astra2

---

hi! i'm astra, the creator of astra2. astra2 is my bot, it does bot stuff; here's a neat list of features:

- asks and forwards any youtube and spotify link i send to another bulletin like channel

---

how to host this yourself:

1. install dependencies in `requirements.txt`

2. make a slack bot and fill in this .env template
```dotenv
SLACK_TOKEN=
SLACK_SECRET=
```

3. go to `app.py` and fill these in with your own things
```python
mediaTargetUser = ["Users the bot forwards from"]
mediaTargetChannel = "Channel bot sends to"
mediaTargetFromChannel = ["Channels bot forwards from"]
```

4. run `app.py`