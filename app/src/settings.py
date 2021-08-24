import logging

from decouple import config


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


TOKEN = config("BOT_TOKEN")
PORT = config("PORT", default=7000, cast=int)
SITE_URL = config("SITE_URL", default="http://localhost:5000/")
GROUP_ID = -570681568

API_URL = config("API_URL", default="http://localhost:5000/")
API_ENDPOINTS = {
    "create_entrada": {
        "URL": API_URL + "entrada/",
        "METHOD": "post"
    },
    "get_entradas": {
        "URL": API_URL + "entrada/",
        "METHOD": "get"
    },
    "deletar_entrada": {
        "URL": API_URL + "entrada/",
        "METHOD": "delete"
    }
}