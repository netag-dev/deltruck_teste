# domain/__init__.py
from .gest_usuarios import *
from .gest_pessoas import *
from .gest_encomendas import *


def register_domain_blueprints(app):
    BASE_API_URL = app.config["BASE_API_URL"]

    role_blueprints(app, BASE_API_URL)
    sexo_blueprints(app, BASE_API_URL)
    cidade_blueprints(app, BASE_API_URL)

    user_blueprints(app, BASE_API_URL)
    users_profile_blueprints(app, BASE_API_URL)
    transportadora_blueprints(app, BASE_API_URL)
    status_encomenda_blueprints(app, BASE_API_URL)
    encomenda_blueprints(app, BASE_API_URL)
    loc_encomenda_blueprints(app, BASE_API_URL)
