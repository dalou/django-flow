
import django.dispatch

# USERS
flow_user_disconnected = django.dispatch.Signal(providing_args=["user_pk", "data", "kwargs"])