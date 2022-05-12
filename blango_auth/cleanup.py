# Django Registration doesn’t have support for automatically cleaning up users that have registered but not validated, but it’s fairly easy to do. You can query for the users that joined more than ACCOUNT_ACTIVATION_DAYS days ago, but are still not active, then delete them.


from datetime import timedelta

from django.conf import settings
from django.utils import timezone

from blango_auth.models import User
User.objects.filter(
    is_active=False,
    date_joined__lt=timezone.now() - timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
).delete()