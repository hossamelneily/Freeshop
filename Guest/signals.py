from django.dispatch import Signal


User_logged_in = Signal(providing_args=['instance','request'])