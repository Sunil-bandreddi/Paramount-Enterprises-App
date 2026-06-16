from django.db import transaction

from accounts.models import Investor, InvestorSequence



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



        return f"PME{sequence.current_number:06d}"