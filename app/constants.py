REDIRECT_URL_LOGIN = "logged_in"
DOMAIN_NAME = "cc-portal"
API_GATEWAY_ID = "8yelnv0oqk"

# COGNITO
AWS_DEFAULT_REGION = "us-east-1"
AWS_COGNITO_DOMAIN = f"""{DOMAIN_NAME}.auth.us-east-1.amazoncognito.com/"""
AWS_COGNITO_USER_POOL_ID = "us-east-1_ItZtGEAjd"
AWS_COGNITO_USER_POOL_CLIENT_ID = "75o48smknv32v7ndl43diesjjj"
AWS_COGNITO_USER_POOL_CLIENT_SECRET = (
    "9ig013v4ste04ad0dlpd6vnrr93i29c4lkong18sppi2us8o8gq"
)
AWS_COGNITO_REDIRECT_URL = f"""https://{API_GATEWAY_ID}.execute-api.us-east-1.amazonaws.com/dev/{REDIRECT_URL_LOGIN}"""
#AWS_COGNITO_REDIRECT_URL = f"""https://localhost:5000/{REDIRECT_URL_LOGIN}"""


def get_sign_in_url() -> str:
    return (
        f"""https://{DOMAIN_NAME}.auth.us-east-1.amazoncognito.com/"""
        + f"""login?client_id={AWS_COGNITO_USER_POOL_CLIENT_ID}"""
        + """&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile"""
        + f"""&redirect_uri={AWS_COGNITO_REDIRECT_URL}"""
    )
