import os
from slack_bolt import App
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import timezone, timedelta, datetime
import re

load_dotenv()

mediaTargetUser = os.getenv("MEDIA_TARGET_USER").split(",")
mediaTargetChannel = os.getenv("MEDIA_TARGET_CHANNEL")
mediaTargetFromChannel = os.getenv("MEDIA_FROM_CHANNELS").split(",")
reminderChannel = os.getenv("REMINDER_CHANNEL")
tz = 7

reminderTs = ""
takenDrugs = False

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
    global reminderTs, takenDrugs

    takenDrugs = False

    res = app.client.chat_postMessage(
        channel=reminderChannel,
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

    scheduler.add_job(
        expireReminder,
        "date",
        run_date=datetime.now(timzeone) + timedelta(hours=10)
    )

    app.client.chat_postEphemeral(
        channel=reminderChannel,
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

def expireReminder():
    global takenDrugs, reminderTs
    if not takenDrugs and reminderTs:
        app.client.chat_update(
            channel=reminderChannel,
            ts=reminderTs,
            text="this is expired! make sure that astra takes her drugs next time around..",
            blocks=[]
        )

@app.action("pokeAstra")
def pokeAstra(ack, body, client):
    ack()
    client.chat_postMessage(
        channel=reminderChannel,
        text=f"<@{body["user"]["id"]}> poked <@U089924LMK8>!! TAKE YOUR DRUGS!"
    )


@app.action("reminderCheck")
def tookDrugs(ack, respond, client):
    global takenDrugs

    ack()
    takenDrugs = True

    client.chat_update(
        channel=reminderChannel,
        ts=reminderTs,
        text="astra took her drugs!",
        blocks=[]
    )
    client.chat_postMessage(
        channel=reminderChannel,
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

@app.message(re.compile(r"reddit\.com/r/.*/comments/"))
def reddit(message, client):
    if message["user"] in mediaTargetUser and message["channel"] in mediaTargetFromChannel:
        remaining = re.sub(r"<https?://\S+>", "", message["text"]).strip()

        if remaining or app.client.conversations_info(channel=message["channel"])["channel"]:
            formatted = f"""<https://hackclub.slack.com/archives/{message['channel']}/p{message['ts'].replace(".","")}|:reddit:>
{'\n'.join(f"> {line}" for line in message["text"].splitlines())}"""
        else:
            formatted = f"<https://hackclub.slack.com/archives/{message["channel"]}/p{message["ts"].replace(".","")}|:reddit:>"

        client.chat_postEphemeral(
            channel = message["channel"],
            user=message["user"],
            text = message["text"],
            blocks=[{
                "type": "actions",
                "block_id": "redditApproval",
                "elements":[{
                    "type":"button",
                    "text": {"type": "plain_text", "text": "Send to #astras-media-spam"},
                    "style":"primary",
                    "action_id": "approveMedia",
                    "value": formatted
                },
                    {
                        "type": "button",
                        "text": {"type":"plain_text", "text": "reject"},
                        "style":"danger",
                        "action_id": "rejectMedia",
                    }]
            }]
        )


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


@app.message(re.compile(r"x\.com/.*/status/|twitter\.com/.*/status/"))
def twitter(message, client):
    if message["user"] in mediaTargetUser and message["channel"] in mediaTargetFromChannel:
        remaining = re.sub(r"<https?://\S+>", "", message["text"]).strip()

        if remaining or app.client.conversations_info(channel=message["channel"])["channel"].get("is_private"):
            formatted = f"""<https://hackclub.slack.com/archives/{message["channel"]}/p{message["ts"].replace(".","")}|:twitter:>
{'\n'.join(f"> {line}" for line in message["text"].splitlines())}"""

        else:
            formatted = f"<https://hackclub.slack.com/archives/{message["channel"]}/p{message['ts'].replace('.','')}|:twitter:>"

        client.chat_postEphemeral(
            channel=message["channel"],
            user=message["user"],
            text=message["text"],
            blocks=[{
                "type": "actions",
                "block_id": "twitterApproval",
                "elements": [{
                    "type": "button",
                    "text": {"type": "plain_text","text": "Send to #astras-media-spam"},
                    "style": "primary",
                    "action_id": "approveMedia",
                    "value": formatted
                },
                    {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "reject"},
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
        text = f"<!subteam^S0AR5M3UVV1>\n{value.replace("<!subteam^", ":pingfest: subteam^ ")}",
        unfurl_links = True,
        unfurl_media = True,)
    respond(replace_original=True, delete_original=True)

@app.action("rejectMedia")
def rejectYoutube(ack, respond):
    ack()
    respond(replace_original=True, delete_original=True)

@app.command("/astra-t2")
def joinT2(ack, body, client, respond):
    ack()
    reason = f"`{body["text"].strip()}`" if body["text"].strip() else "_No reason provided._"
    try:
        res = client.conversations_open(users="U089924LMK8")
        channelId = res["channel"]["id"]
        respond("Sending request!")
        client.chat_postMessage(
            channel = channelId,
            text=f"<@{body["user_id"]}> would like to join <#C098USWAN9K>",
            blocks = [
                {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{body["user_id"]}> would like to join <#C098USWAN9K>\n>*Reason:* {reason}"
                }
                },
                {
                "type": "actions",
                "block_id": "joinT2",
                "elements": [
                        {
                        "type": "button",
                        "text": {"type": "plain_text","text": "Let them in"},
                        "style": "primary",
                        "action_id": "allow",
                        "value": f"{body["user_id"]},C098USWAN9K"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text","text": "ignore"},
                        "action_id": "ignoreInvite",
                    }
                ]
            }]
        )
    except Exception as err:
        respond(f"Failed:\n{err}")

@app.command("/astra-tπ")
def joinTπ(ack, body, client, respond):
    ack()
    reason = f"`{body["text"].strip()}`" if body["text"] else "_No reason provided._"

    try:
        res = client.conversations_open(users="U089924LMK8")
        channelId = res["channel"]["id"]
        respond("Sending request!")
        client.chat_postMessage(
            channel = channelId,
            text = f"<@{body["user_id"]}> would like to join <#C09U89GGZLL>",
            blocks = [{
                "type": "section",
                "text":{
                    "type": "mrkdwn",
                    "text": f"<@{body["user_id"]}> would like to join <#C09U89GGZLL>\n>*Reason:* {reason}",
                }
            },
                {
                    "type": "actions",
                    "block_id": "joinTπ",
                    "elements": [{
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Let them in"},
                        "style": "primary",
                        "action_id": "allow",
                        "value": f"{body["user_id"]},C09U89GGZLL"
                    },
                    {
                        "type": "button",
                        "text": {"type": "plain_text","text": "ignore"},
                        "action_id": "ignoreInvite",
                    }]
                }
            ]
        )
    except Exception as err:
        respond(f"Failed:\n{err}")

@app.action("allow")
def allow(ack, body, client):
    ack()
    id, channel = body["actions"][0]["value"].split(",")

    client.conversations_invite(
        channel = channel,
        users=id
    )

    client.chat_update(
        channel = body["container"]["channel_id"],
        ts = body["container"]["message_ts"],
        text = f"i added <@{id}> to <#{channel}>!",
        blocks=[{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"i added <@{id}> to <#{channel}>!"
            }
        },
            {
                "type": "actions",
                "block_id": "undoInvite",
                "elements": [{
                    "type": "button",
                    "style": "danger",
                    "text": {
                        "type": "plain_text",
                        "text": "Undo invite"
                        },
                    "action_id": "undoInvite",
                    "value": f"{id},{channel}"
                }]

            }]
    )

@app.action("ignoreInvite")
def ignoreInvite(ack, body, client):
    client.chat_update(
        channel = body["container"]["channel_id"],
        ts = body["container"]["message_ts"],
        text = "Ignored invite request"
    )
    ack()

@app.action("undoInvite")
def undoInvite(ack, body, client):
    ack()
    id, channel = body["actions"][0]["value"].split(",")
    client.conversations_kick(
        channel=channel,
        user=id
    )

    client.chat_update(
        channel=body["container"]["channel_id"],
        ts = body["container"]["message_ts"],
        text = f"Kicked <@{id}> from <#{channel}>!",
    )



if __name__ == "__main__":
    app.start(3000)