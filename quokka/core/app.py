# coding: utf-8
from flask import Blueprint, Flask


def _endpoint_from_view_func(view_func):
    """Internal helper that returns the default endpoint for a given
    function.  This always is the function name.
    """
    assert view_func is not None, "expected view func if endpoint is not provided."
    return view_func.__name__


class QuokkaApp(Flask):
    """
    Implements customizations on Flask
    - custom add_quokka_url_rule
    - properties to access db and admin
    """

    def add_quokka_url_rule(self, rule, endpoint=None,
                            view_func=None, **options):
        """Builds urls using quokka. prefix to avoid conflicts
        with external modules urls."""
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        if not endpoint.startswith('quokka.'):
            endpoint = 'quokka.' + endpoint
        self.add_url_rule(rule, endpoint, view_func, **options)

    def register_module(self, module):
        self.register_blueprint(module)

    @property
    def db(self):
        return self.extensions['db']

    @property
    def admin(self):
        ext = self.extensions['admin']
        adm = ext[0] if isinstance(ext, list) else ext
        adm.app = self  # cross reference
        return adm


class QuokkaModule(Blueprint):
    """Overwrite blueprint namespace to quokka.modules.name
    to avoid conflicts with external Blueprints use same name"""

    def __init__(self, name, *args, **kwargs):
        kwargs.setdefault('import_name', name)
        kwargs.setdefault('template_folder', 'templates')
        super(QuokkaModule, self).__init__(name, *args, **kwargs)
