import os
from slack_bolt import App
from dotenv import load_dotenv

load_dotenv()

app = App(
    token = os.getenv("SLACK_TOKEN"),
    signing_secret = os.getenv("SLACK_SECRET")
)

@app.message("test")
def blegh(message, say):
    say(f"test {message["user"]}")
    
if __name__ == "__main__":
    app.start(3000)