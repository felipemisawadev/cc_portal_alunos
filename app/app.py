import logging
from flask import Flask, render_template, redirect, request, session, url_for, flash
from flask_awscognito import AWSCognitoAuthentication

import secrets
import boto3
import re
import datetime as dt

from utils import parse_user_attributes
from auth_wrapper import auth_required
import constants as constants

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
client = boto3.client("cognito-idp", constants.AWS_DEFAULT_REGION)
dynamodb = boto3.resource("dynamodb", constants.AWS_DEFAULT_REGION)
students_table = dynamodb.Table("alunos")


@app.route("/")
def index(event=None, context=None):
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
@auth_required(aws_auth)
def home():
    user = parse_user_attributes(client.get_user(AccessToken=session["token"]))
    session["userid"] = user["sub"]
    session["username"] = user["name"]
    return render_template("home.html")


@app.route("/profile")
@auth_required(aws_auth)
def profile():
    # get user data from dynamodb if available
    response = students_table.get_item(Key={"id": session["userid"]})
    if response:
        item = response.get("Item", None)
        session["user_relationship"] = item.get("relationship", None)
        session["user_entry_year"] = item.get("entry_year", None)
        session["user_linkedin"] = item.get("linkedin", None)
        session["user_whatsapp"] = item.get("whatsapp", None)
    return render_template("profile.html")


@app.route("/update", methods=["POST"])
@auth_required(aws_auth)
def update():
    relationship = request.form.get("relationship")
    entry_year = request.form.get("entry_year")
    linkedin = request.form.get("linkedin")
    whatsapp = request.form.get("whatsapp")
    accept = "accept" in request.form
    if not accept:
        flash("Por favor, aceite os termos e condições")
        return redirect(url_for("profile"))

    # test if year is in range 1900 - 2999 and less than current year
    if (not re.match("^(19|20)\d{2}$", entry_year)) or (
        int(entry_year) > dt.date.today().year
    ):
        flash("Ano inválido")
        return redirect(url_for("profile"))

    entry_year = int(entry_year)

    # sanitize whatsapp number leaving numbers only
    whatsapp = re.sub("\D", "", whatsapp)
    # check if number has enough digits
    if len(whatsapp) < 12:
        flash("Whatsapp inválido")
        return redirect(url_for("profile"))

    whatsapp = f"+{whatsapp}"

    response = students_table.put_item(
        Item={
            "id": session["userid"],
            "relationship": relationship,
            "entry_year": entry_year,
            "linkedin": linkedin,
            "whatsapp": whatsapp,
        }
    )

    status_code = response["ResponseMetadata"]["HTTPStatusCode"]

    if status_code == 200:
        flash("Dados atualizados!")
        return redirect(url_for("profile"))
    else:
        flash("Erro na atualização, por favor tente novamente")
        return redirect(url_for("profile"))


@app.route("/courses")
@auth_required(aws_auth)
def courses():
    return render_template("courses.html")


@app.route("/sign_out")
@auth_required(aws_auth)
def sign_out():
    session.pop("token", None)
    return redirect(url_for("index"))


# For local runs, set flask to use debug mode
if __name__ == "__main__":
    logger.setLevel(logging.DEBUG)
    app.run(debug=True, ssl_context="adhoc")
