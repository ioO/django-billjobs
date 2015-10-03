# -*- coding: utf-8 -*-

from core import settings
import os.path

DEBUG_PDF = True
# Set app base dir
BILLING_BASE_DIR = os.path.abspath(os.path.dirname(__file__))

LOGO_PATH = BILLING_BASE_DIR + '/static/images/logo-default.jpg'

BILLING_ISSUER = """Your Coworking Space Name<br/>Building name<br/>
                    21 Jump Street<br/>34000 Montpellier"""

BILLING_PAYMENT_INFO = """
    <b>Conditions de règlement:</b> à réception de la facture<br /><br/>
    Règlement par chèque à l'ordre de <b>Cowork'in Montpellier</b> envoyé à<br/><br/>
    Cowork'in Montpellier<br/>
    19 rue de l'école de droit<br/>
    34000 Montpellier<br/><br/>
    Règlement par virement<br/><br/>
    Code IBAN: FR76 4255 9000 3441 0200 2895 736<br/>
    Code BIC/SWIFT: CCOPFRPPXXX
    """

