import os
from jinja2 import Template
from config import TEMPLATE_PATH
from app.constants import MESSAGE_FIELD_ONETIME_PASS, MESSAGE_TEMPLATE


def populate_template(message):

    populated_template = None

    if MESSAGE_FIELD_ONETIME_PASS in message:
        populated_template = __populate(message[MESSAGE_TEMPLATE],message)

    return populated_template


def __populate(content_template, message):

    with open(os.path.join(TEMPLATE_PATH, content_template)) as f:
        template_raw_content = f.read()

    template = Template(template_raw_content)

    return template.render(message)
