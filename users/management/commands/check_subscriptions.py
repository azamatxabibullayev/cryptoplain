from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import PremiumUser


class Command(BaseCommand):
    help = 'Checks and updates user subscriptions'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        expired_subscriptions = PremiumUser.objects.filter(subscription_end__lte=now)

        for premium_user in expired_subscriptions:
            premium_user.user.is_premium = False
            premium_user.user.save()
            premium_user.delete()

        self.stdout.write(self.style.SUCCESS('Successfully updated expired subscriptions.'))
