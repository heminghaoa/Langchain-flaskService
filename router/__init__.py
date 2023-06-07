# router/__init__.py
from flask import Blueprint

openai_app = Blueprint('openai', __name__)
test_app = Blueprint('test', __name__)

from .openai import *
from .test import *
