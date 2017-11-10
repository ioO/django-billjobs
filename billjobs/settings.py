# -*- coding: utf-8 -*-

from django.conf import settings
import os.path

BILLJOBS_BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BILLJOBS_DEFAULT = dict(
        DEBUG=True,
        LOGO_PATH=BILLJOBS_BASE_DIR + '/static/images/logo-default.png',
        LOGO_WIDTH=100,
        LOGO_HEIGHT=80,
        ISSUER="""
            Your Coworking Space Name<br/>Building name<br/>
            Number & Street<br/>Postal Code Town
            """,
        PAYMENT_INFO="""
            Add information about billing condition and payment information.
            <br/>
            You can use htlm in this setting.
            """,
        FORCE_SUPERUSER=False,
        FORCE_USER_GROUP=None
        )


BILLJOBS_DEBUG_PDF = getattr(settings, 'DEBUG', BILLJOBS_DEFAULT['DEBUG'])
BILLJOBS_BILL_LOGO_PATH = getattr(
        settings,
        'BILLJOBS_BILL_LOGO_PATH',
        BILLJOBS_DEFAULT['LOGO_PATH']
        )
BILLJOBS_BILL_LOGO_WIDTH = getattr(
        settings,
        'BILLJOBS_BILL_LOGO_WIDTH',
        BILLJOBS_DEFAULT['LOGO_WIDTH']
        )
BILLJOBS_BILL_LOGO_HEIGHT = getattr(
        settings,
        'BILLJOBS_BILL_LOGO_HEIGHT',
        BILLJOBS_DEFAULT['LOGO_HEIGHT']
        )
BILLJOBS_BILL_ISSUER = getattr(
        settings,
        'BILLJOBS_BILL_ISSUER',
        BILLJOBS_DEFAULT['ISSUER']
        )
BILLJOBS_BILL_PAYMENT_INFO = getattr(
        settings,
        'BILLJOBS_BILL_PAYMENT_INFO',
        BILLJOBS_DEFAULT['PAYMENT_INFO']
        )
BILLJOBS_FORCE_SUPERUSER = getattr(
        settings,
        'BILLJOBS_FORCE_SUPERUSER',
        BILLJOBS_DEFAULT['FORCE_SUPERUSER']
        )
BILLJOBS_FORCE_USER_GROUP = getattr(
        settings,
        'BILLJOBS_FORCE_USER_GROUP',
        BILLJOBS_DEFAULT['FORCE_USER_GROUP']
        )
