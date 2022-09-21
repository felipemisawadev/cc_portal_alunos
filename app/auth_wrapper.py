from flask import session, url_for, redirect, g
import functools


# def auth_required(func):
#     """Decorator that reports the execution time."""

#     def auth_wrapper(*args, **kwargs):
#         if "token" in session:
#             result = func(*args, **kwargs)
#             return result
#         else:
#             return redirect(url_for("sign_in"))

#     # Renaming the function name:
#     auth_wrapper.__name__ = func.__name__
#     return auth_wrapper


def auth_required(aws_auth):
    def actual_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if "token" in session:
                aws_auth.token_service.verify(session["token"])
                aws_auth.claims = aws_auth.token_service.claims
                g.cognito_claims = aws_auth.claims
                result = func(*args, **kwargs)
                return result
            else:
                return redirect(url_for("sign_in"))

        return wrapper

    return actual_decorator
