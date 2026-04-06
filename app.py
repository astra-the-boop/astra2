import os
from slack_bolt import App
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timezone, timedelta
import re

load_dotenv()

mediaTargetUser = os.getenv("MEDIA_TARGET_USER").split(",")
mediaTargetChannel = os.getenv("MEDIA_TARGET_CHANNEL")
mediaTargetFromChannel = os.getenv("MEDIA_FROM_CHANNELS").split(",")
tz = float(os.getenv("TIMEZONE"))

app = App(
    token = os.getenv("SLACK_TOKEN"),
    signing_secret = os.getenv("SLACK_SECRET")
)

timzeone = timezone(timedelta(hours=tz))
scheduler = BackgroundScheduler(timezone=timzeone)

@scheduler.scheduled_job("cron", hour=20, minute=0) #8pm
def drugsMorning():
    pass

scheduler.start()

# @app.message("astra2_test")
# def test(message, say, client):
#     say("hi there!")
#     client.chat_postMessage(
#         channel="C097PNFQK24",
#         text="test"
#     )

@app.message(re.compile(r"\.wikipedia\.org/wiki/"))
def wikipedia(message, client):
    if message["user"] in mediaTargetUser and message["channel"] in mediaTargetChannel:
        remaining = re.sub(r"<https?://\S+]", "", message["text"]).strip()

        if remaining:
            formatted = f"""<https://hackclub.slack.com/archives/{message["channel"]}/p{message["ts"].replace(".","")}|:wikipedia:>
{'\n'.join(f"> {line}" for line in message["text"].splitlines())}"""
        else:
            formatted = f"<https://hackclub.slack.com/archives/{message["channel"]}/p{message['ts'].replace('.','')}|:wikipedia:>"

        client.chat_postMessage(
            channel=message["channel"],
            user=message["user"],
            text=message["text"],
            blocks=[{
                "type": "actions",
                "block_id": "wikipediaApproval",
                "elements": [{
                    "type": "button",
                    "text": {"type":"plain_text","text":"Send to #astras-media-spam"}
                    "style": "primary",
                    "action_id": "approveMedia",
                    "value": formatted
               }, {
                    "type": "button",
                    "text": {"type":"plain_text", "text": "reject"},
                    "style": "danger",
                    "action_id": "rejectMedia"
                }]
            }]
        )


@app.message(re.compile(r"youtube\.com/watch\?v=|youtu\.be/"))
def youtube(message, client):
    # say("implodes")
    if message["user"] in mediaTargetUser and message["channel"] in mediaTargetFromChannel:
        remaining = re.sub(r"<https?://\S+>", "", message["text"]).strip()

        if remaining:
            formatted = f"""<https://hackclub.slack.com/archives/{message["channel"]}/p{message["ts"].replace(".","")}|:youtube:>
{'\n'.join(f"> {line}" for line in message["text"].splitlines())}"""
           
        else:
            formatted = f"<https://hackclub.slack.com/archives/{message["channel"]}/p{message["ts"].replace(".","")}|:youtube:>"
        client.chat_postEphemeral(
            channel=message["channel"],
            user=message["user"],
            text=message["text"],
            blocks=[{
                "type": "actions",
                "block_id": "youtubeApproval",
                "elements": [{
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Send to #astras-media-spam"},
                    "style": "primary",
                    "action_id": "approveMedia",
                    "value": formatted
                },
                    {
                        "type": "button",
                        "text": {"type": "plain_text","text":"Reject"},
                        "style": "danger",
                        "action_id": "rejectMedia",
                    }]
            }]
        )

@app.message(re.compile(r"open\.spotify\.com/track/"))
def spotify(message, client):
    if message["user"] in mediaTargetUser and message["channel"] in mediaTargetFromChannel:
        remaining = re.sub(r"<https?://\S+>", "", message["text"]).strip()
        if remaining:
            formatted = f"""<https://hackclub.slack.com/archives/{message["channel"]}/p{message["ts"].replace(".","")}|:spotify_logo:>
{'\n'.join(f"> {line}" for line in message["text"].splitlines())}"""
        else:
            formatted = f"<https://hackclub.slack.com/archives/{message["channel"]}/p{message['ts'].replace(".","")}|:spotify_logo:>"
        client.chat_postEphemeral(
            channel=message["channel"],
            text=message["text"],
            user=message["user"],
            blocks=[{
                "type": "actions",
                "block_id": "spotifyApproval",
                "elements": [{
                    "type": "button",
                    "text": {"type": "plain_text","text": "Send to #astras-media-spam"},
                    "style": "primary",
                    "action_id": "approveMedia",
                    "value": formatted
                },
                    {
                        "type": "button",
                        "text": {"type": "plain_text","text":"Reject"},
                        "style": "danger",
                        "action_id": "rejectMedia",
                        "value": formatted
                    }]
            }]
        )

@app.action("approveMedia")
def approveYoutube(ack, body, client, respond):
    ack()
    value = body["actions"][0]["value"]
    client.chat_postMessage(
        channel = mediaTargetChannel,
        text = value)
    respond(replace_original=True, delete_original=True)

@app.action("rejectMedia")
def rejectYoutube(ack, respond):
    ack()
    respond(replace_original=True, delete_original=True)

if __name__ == "__main__":
    app.start(3000)