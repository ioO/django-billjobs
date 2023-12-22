========
Settings
========

You must add those settings in your own project *settings.py* to customize the invoice and slack integration.
Have a look to `billjobs/settings`_ to see default settings and how to write them.

BILLJOBS_DEBUG_PDF
------------------

Boolean.

For development only, this settings help you to view limit of the invoice pdf document. 

By default this settings is based on *DEBUG* value in your own *settings.py*

BILLJOBS_BILL_LOGO_PATH
-----------------------

String.

Add your own logo to your invoice.

Default is a logo path to billjobs static folder.

BILLJOBS_BILL_LOGO_WIDTH and BILLJOBS_BILL_LOGO_HEIGHT
------------------------------------------------------

Integer.

Define width and height of the logo in the invoice. Do not add unit to size. It is managed by *reportlab* lib.

Default value is 100 for the width and 80 for the height. We recommand you adapt your logo to thoses sizes.

BILLJOBS_BILL_ISSUER
--------------------

Text HTML.

Add your invoice information.

BILLJOBS_BILL_PAYMENT_INFO
--------------------------

Text HTML.

Display information to user on the ways to pay you !

BILLJOBS_FORCE_SUPERUSER
------------------------

Boolean.

Force during signup the user to be set as a superuser and access.

Default is False.

BILLJOBS_FORCE_USER_GROUP
-------------------------

String.

Force during signup to add the newly user to a particular group. Only one group is possible.

Default is None.

BILLJOBS_SLACK_TOKEN
--------------------

String.

`Legacy token`_ for slack API. This token is used so send a slack invitation to the email address of the newly signup 
user. If you want to send a message to a channel after signup is successful you must add this setting.

Default is False.

BILLJOBS_SLACK_CHANNEL
----------------------

String.

Add channel name in the form of **#channel_name** or use channel id you can find in slack url for example::

   https://workspace.slack.com/messages/CHANNEL_ID

We recommand channel id to avoid errors.

Default is False.

.. _billjobs/settings: https://github.com/ioO/django-billjobs/blob/master/billjobs/settings.py
.. _Legacy token: https://api.slack.com/custom-integrations/legacy-tokens

BILLJOBS_QUOTE_EXPIRES_DAYS
----------------------

Integer.

Number of days an issued quote remains valid

Default is 30 days.