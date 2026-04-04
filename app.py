import os
from slack_bolt import App
from dotenv import load_dotenv

import re

load_dotenv()

app = App(
    token = os.getenv("SLACK_TOKEN"),
    signing_secret = os.getenv("SLACK_SECRET")
)

mediaTarget = ["U089924LMK8"]

@app.message("astra2_test")
def test(message, say, client):
    say("hi there!")
    client.chat_postMessage(
        channel="C097PNFQK24",
        text="test"
    )

@app.message(re.compile(r"youtube\.com/watch\?v="))
def youtube(message, say, client):
    say("implodes")
    client.chat_postMessage(
        channel = "C097PNFQK24",
        text = message["text"]
    )
    
if __name__ == "__main__":
    app.start(3000)