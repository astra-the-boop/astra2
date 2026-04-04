import os
from slack_bolt import App
from dotenv import load_dotenv

import re

load_dotenv()

app = App(
    token = os.getenv("SLACK_TOKEN"),
    signing_secret = os.getenv("SLACK_SECRET")
)

mediaTargetUser = ["U089924LMK8"]
mediaTargetChannel = "C097PNFQK24"
mediaTargetFromChannel = ["C08F4R7HVS8", "C098USWAN9K"]

@app.message("astra2_test")
def test(message, say, client):
    say("hi there!")
    client.chat_postMessage(
        channel="C097PNFQK24",
        text="test"
    )

@app.message(re.compile(r"youtube\.com/watch\?v=|youtu\.be/"))
def youtube(message, say, client):
    # say("implodes")
    if message["user"] in mediaTargetUser and message["channel"] in mediaTargetFromChannel:
        client.chat_postEmphemeral(
            channel=message["channel"],
            user=message["user"],
            text=message["text"],
            blocks=[{
                "type": "action",
                "block_id": "youtubeApproval",
                "elements": [{
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Send to #astras-media-spam"},
                    "style": "primary",
                    "action_id": "approveYoutube",
                    "value": f"""<https://hackclub.slack.com/archives/{message["channel"]}/p{message["ts"].replace(".","")}|:youtube:>
{message["text"]}
"""
                },
                    {
                        "type": "button",
                        "text": {"type": "plain_text","text":"Reject"},
                        "style": "primary",
                        "action_id": "rejectYoutube",
                    }]
            }]
        )

@app.action("approveYoutube")
def approveYoutube(ack, body, client):
    ack()
    value = body["value"][0]["value"]
    client.chat_postMessage(
        channel = mediaTargetChannel,
        text = value)
    
if __name__ == "__main__":
    app.start(3000)