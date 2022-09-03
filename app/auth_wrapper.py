from flask import session, url_for, redirect


def auth_required(func):
    """Decorator that reports the execution time."""

    def auth_wrapper(*args, **kwargs):
        if "token" in session:
            result = func(*args, **kwargs)
            return result
        else:
            return redirect(url_for("sign_in"))

    # Renaming the function name:
    auth_wrapper.__name__ = func.__name__
    return auth_wrapper
