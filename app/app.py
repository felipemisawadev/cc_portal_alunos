import logging
from flask import Flask, render_template, redirect, request, session, url_for
from flask_awscognito import AWSCognitoAuthentication
from auth_wrapper import auth_required
import constants as constants
import secrets

app = Flask(__name__)
logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app.secret_key = secrets.token_urlsafe(16)

app.config["AWS_DEFAULT_REGION"] = constants.AWS_DEFAULT_REGION
app.config["AWS_COGNITO_DOMAIN"] = constants.AWS_COGNITO_DOMAIN
app.config["AWS_COGNITO_USER_POOL_ID"] = constants.AWS_COGNITO_USER_POOL_ID
app.config[
    "AWS_COGNITO_USER_POOL_CLIENT_ID"
] = constants.AWS_COGNITO_USER_POOL_CLIENT_ID
app.config[
    "AWS_COGNITO_USER_POOL_CLIENT_SECRET"
] = constants.AWS_COGNITO_USER_POOL_CLIENT_SECRET
app.config["AWS_COGNITO_REDIRECT_URL"] = constants.AWS_COGNITO_REDIRECT_URL

aws_auth = AWSCognitoAuthentication(app)


@app.route("/")
def index(event=None, context=None):
    logger.debug("Lambda function invoked index()")
    return render_template("index.html")


@app.route("/sign_in")
def sign_in():
    return redirect(aws_auth.get_sign_in_url())


@app.route("/logged_in")
def logged_in():
    access_token = aws_auth.get_access_token(request.args)
    session["token"] = access_token
    return redirect(url_for("home"))


@app.route("/home")
@auth_required
def home():
    return render_template("home.html")


@app.route("/profile")
@auth_required
def profile():
    return "PROFILE PAGE"


@app.route("/courses")
@auth_required
def courses():
    return "COURSES PAGE"


@app.route("/sign_out")
@auth_required
def sign_out():
    session.pop("token", None)
    return redirect(url_for("index"))


# For local runs, set flask to use debug mode
if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    app.run(debug=True)