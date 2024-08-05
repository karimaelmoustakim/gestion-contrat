# your_app/management/commands/remove_notification_duplicates.py

from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from notifications.models import Notification

class Command(BaseCommand):
    help = 'Supprime les notifications en double.'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            duplicates = (
                Notification.objects.values('user_id', 'contract_id')
                .annotate(count=Count('id'))
                .filter(count__gt=1)
            )

            for duplicate in duplicates:
                user_id = duplicate['user_id']
                contract_id = duplicate['contract_id']
                notifications = Notification.objects.filter(user_id=user_id, contract_id=contract_id)

                # Garder la plus récente et supprimer les autres
                for notification in notifications[1:]:
                    notification.delete()

        self.stdout.write(self.style.SUCCESS('Les notifications en double ont été supprimées.'))
