from flask import Blueprint


routes = Blueprint('routes', __name__, template_folder='templates')

from .user_management import *
from .subdomain_manage import *
from .subdomain_new import *
from .dev import *