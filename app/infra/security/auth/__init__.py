# auth/__init__.py


from .auth_code import *

from .authService import AuthService
from .authViews import *
from .shemas import *


def auth_blueprints(app, BASE_API_URL):
    login_view = AuthApi.as_view("auth_api")

    app.add_url_rule(
        f"{BASE_API_URL}/auth/login",
        view_func=login_view,
        methods=["POST"],
    )

    #
    app.add_url_rule(
        f"{BASE_API_URL}/auth/login/final-user",
        view_func=login_view,
        methods=["POST"],
    )

    app.add_url_rule(
        f"{BASE_API_URL}/auth/login/final-user/send-email-verification",
        view_func=login_view,
        methods=["POST"],
    )

    app.add_url_rule(
        f"{BASE_API_URL}/auth/login/final-user/auth-code-verification",
        view_func=login_view,
        methods=["GET"],
    )
