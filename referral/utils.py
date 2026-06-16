from datetime import date, timedelta

from django.conf import settings
from django.utils import timezone

from referral.models import ReferralTree


def get_current_week_dates(today=None):
    today = today or timezone.localdate()
    monday = today - timedelta(days=today.weekday())
    saturday = monday + timedelta(days=5)
    return monday, saturday


def get_previous_week_dates(today=None):
    monday, saturday = get_current_week_dates(today)
    return monday - timedelta(days=7), saturday - timedelta(days=7)


def get_week_status():
    return get_current_week_dates()


def get_week_number(start_date, today=None):
    current_monday, _ = get_current_week_dates(today)
    return ((current_monday - start_date).days // 7) + 1


def get_referral_week_summaries(investor):
    current_monday, current_saturday = get_current_week_dates()
    bonus_amount = getattr(settings, "REFERRAL_BONUS_AMOUNT", 0)

    referrals = (
        ReferralTree.objects.filter(sponsor=investor)
        .only("id", "created")
        .order_by("-created")
    )

    grouped_counts = {}
    for referral in referrals:
        created_date = timezone.localtime(referral.created).date()
        week_start, _ = get_current_week_dates(created_date)
        grouped_counts[week_start] = grouped_counts.get(week_start, 0) + 1

    summaries = []
    for week_start, total_referrals in sorted(grouped_counts.items(), reverse=True):
        week_end = week_start + timedelta(days=5)
        is_current = week_start == current_monday
        summaries.append(
            {
                "week_number": get_week_number(week_start),
                "monday": week_start,
                "saturday": week_end,
                "total_referrals": total_referrals,
                "bonus": total_referrals * bonus_amount,
                "status": "CURRENT" if is_current else "PREVIOUS",
            }
        )

    if not any(item["status"] == "CURRENT" for item in summaries):
        summaries.insert(
            0,
            {
                "week_number": get_week_number(current_monday),
                "monday": current_monday,
                "saturday": current_saturday,
                "total_referrals": 0,
                "bonus": 0,
                "status": "CURRENT",
            },
        )

    return summaries
