# status_encomenda/__init__.py

from .statusEncomenda import StatusEncomenda
from .statusEncomendaRepository import StatusEncomendaRepository
from .statusEncomendaService import StatusEncomendaService
from .statusEncomendaViews import *
from .schemas import *


def status_encomenda_blueprints(app, BASE_API_URL):
    staus_encomenda_views = StatusEncomendaApi.as_view("status_encomenda_api")

    app.add_url_rule(
        f"{BASE_API_URL}/status-encomendas",
        view_func=staus_encomenda_views,
        methods=["GET"],
    )
