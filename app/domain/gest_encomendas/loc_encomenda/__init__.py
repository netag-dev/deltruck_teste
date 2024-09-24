# loc_encomenda/__init__.py

from .locEncomenda import LocEncomenda
from .locEncomendaRepository import LocEncomendaRepository
from .locEncomendaService import LocEncomendaService
from .locEncomendaViews import *
from .schemas import *


def loc_encomenda_blueprints(app, BASE_API_URL):
    loc_encomenda_views = LocEncomendaApi.as_view("loc_encomenda_api")

    app.add_url_rule(
        f"{BASE_API_URL}/loc-encomendas/encomenda/<encomenda_id>",
        view_func=loc_encomenda_views,
        methods=["POST"],
    )
