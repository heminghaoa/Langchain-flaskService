# router/__init__.py
from flask import Blueprint

openai_app = Blueprint('openai', __name__)
test_app = Blueprint('test', __name__)
takumi_app = Blueprint('takumi', __name__)

from .openai import *
from .test import *
from .takumi import *
