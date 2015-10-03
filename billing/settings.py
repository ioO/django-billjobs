# -*- coding: utf-8 -*-

from core import settings
import os.path

DEBUG_PDF = True
# Set app base dir
BILLING_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOGO_PATH = BILLING_BASE_DIR + '/static/images/logo-default.jpg'

BILLING_ISSUER = """Your Coworking Space Name<br/>Building name<br/>
                    21 Jump Street<br/>34000 Montpellier"""
