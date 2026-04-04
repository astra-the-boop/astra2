import os
from slack_bolt import App
from dotenv import load_dotenv

load_dotenv()

app = App(
    token = os.getenv("SLACK_TOKEN"),
    signing_secret = os.getenv("SLACK_SECRET")
)

@app.message("astra2_test")
def test(message, say):
    say("hi there!")

@app.message("https://youtube.com/watch?")
def youtube(message, say, client):
    client.chat.postMessage(
        channel = "C097PNFQK24",
        text = message["text"]
    )
    
if __name__ == "__main__":
    app.start(3000)