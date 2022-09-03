import logging
from flask import Flask, render_template, redirect

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.route("/")
def index(event=None, context=None):
    logger.debug("Lambda function invoked index()")
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    return redirect(
        "https://cc-portal.auth.us-east-1.amazoncognito.com/login?client_id=7l99vut98tvvqp2v78icthncuv&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=https://www.google.com"
    )


# For local runs, set flask to use debug mode
if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    app.run(debug=True)
