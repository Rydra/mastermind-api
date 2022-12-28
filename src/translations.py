from babel.support import Translations

# NOTE: Putting here the underscore translation to avoid clutering the global
# namespace.
# ref: https://stackoverflow.com/questions/3834457/python-using-gettext-everywhere-with-init-py
# ref: https://phrase.com/blog/posts/i18n-advantages-babel-python/
translations = Translations.load("locale", ["es_ES", "en_GB"])
_ = translations.gettext
