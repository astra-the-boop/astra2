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
tz = 7

app = App(
    token = os.getenv("SLACK_TOKEN"),
    signing_secret = os.getenv("SLACK_SECRET")
)

timzeone = timezone(timedelta(hours=tz))
scheduler = BackgroundScheduler(timezone=timzeone)

@scheduler.scheduled_job("cron", hour=20, minute=0) #8pm
def drugsEvening():
    _drugsReminder()

@scheduler.scheduled_job("cron", hour=7, minute=0)
def drugsMorning():
    _drugsReminder()

def _drugsReminder():
    global reminderTs
    res = app.client.chat_postMessage(
        channel="C08F4R7HVS8",
        blocks=[
            {
                "type": "section",
                "text": {
                    "text":"<!subteam^S0A31QEU15W> FORCE ASTRA TO TAKE DRUGS!!!!! <@U089924LMK8> TAKE DRUGS!!!\nI will continue to show the 'poke astra' button until she takes her drugs. Please annoy her until she takes them!",
                    "type": "mrkdwn"}
            },
            {
            "type":"actions",
            "block_id": "reminderPing",
            "elements":[{
                "type": "button",
                "text": {"type": "plain_text", "text": "poke astra"},
                "style": "primary",
                "action_id": "pokeAstra"
            }]
        }]
    )
    reminderTs = res["ts"]

    app.client.chat_postEphemeral(
        channel="C08F4R7HVS8",
        user="U089924LMK8",
        blocks=[{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Remember to take them!"
            }

        },{
            "type": "actions",
            "block_id": "reminderCheck",
            "elements":[{
                "type": "button",
                "action_id": "reminderCheck",
                "text": {"type": "plain_text", "text": "I took them!"},
                "style": "danger"
            }]

        }]
    )

scheduler.start()

@app.action("pokeAstra")
def pokeAstra(ack, body, client):
    ack()
    client.chat_postMessage(
        channel="C08F4R7HVS8",
        text=f"<@{body["user"]["id"]}> poked <@U089924LMK8>!! TAKE YOUR DRUGS!"
    )


@app.action("reminderCheck")
def tookDrugs(ack, respond, client):
    ack()
    client.chat_update(
        channel="C08F4R7HVS8",
        ts=reminderTs,
        text="astra took her drugs!",
        blocks=[]
    )
    client.chat_postMessage(
        channel="C08F4R7HVS8",
        text="astra took her drugs! yall can stop now",
    )
    respond(text="yum", replace_original=True)

# @app.message("astra2_test")
# def test(message, say, client):
#     say("hi there!")
#     client.chat_postMessage(
#         channel="C097PNFQK24",
#         text="test"
#     )

@app.message(re.compile(r"\.wikipedia\.org/wiki/"))
def wikipedia(message, client):
    if message["user"] in mediaTargetUser and message["channel"] in mediaTargetFromChannel:
        remaining = re.sub(r"<https?://\S+>", "", message["text"]).strip()

        if remaining or app.client.conversations_info(channel=message["channel"])["channel"].get("is_private"):
            formatted = f"""<https://hackclub.slack.com/archives/{message["channel"]}/p{message["ts"].replace(".","")}|:wikipedia:>
{'\n'.join(f"> {line}" for line in message["text"].splitlines())}"""
        else:
            formatted = f"<https://hackclub.slack.com/archives/{message["channel"]}/p{message['ts'].replace('.','')}|:wikipedia:>"

        client.chat_postEphemeral(
            channel=message["channel"],
            user=message["user"],
            text=message["text"],
            blocks=[{
                "type": "actions",
                "block_id": "wikipediaApproval",
                "elements": [{
                    "type": "button",
                    "text": {"type":"plain_text","text":"Send to #astras-media-spam"},
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

        if remaining or app.client.conversations_info(channel=message["channel"])["channel"].get("is_private"):
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
        if remaining or app.client.conversations_info(channel=message["channel"])["channel"].get("is_private"):
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
        text = f"<!subteam^S0AR5M3UVV1>\n{value}",
        unfurl_links = True,
        unfurl_media = True,)
    respond(replace_original=True, delete_original=True)

@app.action("rejectMedia")
def rejectYoutube(ack, respond):
    ack()
    respond(replace_original=True, delete_original=True)

if __name__ == "__main__":
    app.start(3000)