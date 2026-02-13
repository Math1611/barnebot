from services.translations.es import TEXTS as ES
from services.translations.en import TEXTS as EN

LANGS = {
    "es": ES,
    "en": EN,
}


def t(key: str, lang: str = "es"):
    return LANGS.get(lang, ES).get(key, key)
