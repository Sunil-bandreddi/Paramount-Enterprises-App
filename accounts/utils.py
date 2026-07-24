from django.db import transaction

from accounts.models import Investor, InvestorSequence


def is_admin(user):
    """
    Shared admin check. Only staff/superuser accounts (the company's
    admin login) may enter new investors into the system.
    """
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def generate_investor_id():

    with transaction.atomic():

        sequence, created = InvestorSequence.objects.get_or_create(
            id=1,
            defaults={
                "current_number":0
            }
        )

        sequence.current_number += 1

        sequence.save()

        return f"PME{sequence.current_number:07d}"