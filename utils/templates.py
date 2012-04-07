# -*- coding: utf-8 -*-

from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('templates', '.'))

def render(tmpl, *arg, **argk):
    return env.get_template(tmpl).render(*arg, **argk)

