from datetime import date, timedelta

from django.conf import settings
from django.utils import timezone

from referral.models import ReferralTree


def get_current_week_dates(today=None):
    """
    Returns (week_start, week_end) for the Sunday-to-Saturday week that
    `today` falls in.
    """
    today = today or timezone.localdate()
    days_since_sunday = (today.weekday() + 1) % 7
    week_start = today - timedelta(days=days_since_sunday)
    week_end = week_start + timedelta(days=6)
    return week_start, week_end


def get_previous_week_dates(today=None):
    monday, saturday = get_current_week_dates(today)
    return monday - timedelta(days=7), saturday - timedelta(days=7)


def get_week_status():
    return get_current_week_dates()


def get_week_number(start_date, today=None):
    current_monday, _ = get_current_week_dates(today)
    return ((current_monday - start_date).days // 7) + 1


def get_referral_week_summaries(investor):
    """
    Reads persisted weekly history from WeeklyActivity (kept up to date
    by referral.services.sync_weekly_activity), rather than
    recomputing it live.
    """

    from referral.models import WeeklyActivity

    current_week_start, current_week_end = get_current_week_dates()

    rows = WeeklyActivity.objects.filter(investor=investor).order_by("-week_number")

    summaries = []

    for row in rows:
        summaries.append({
            "week_number": row.week_number,
            "monday": row.monday,
            "saturday": row.saturday,
            "total_referrals": row.total_referrals,
            "level": row.level,
            "status": "CURRENT" if row.monday == current_week_start else "PREVIOUS",
        })

    if not any(item["status"] == "CURRENT" for item in summaries):
        summaries.insert(0, {
            "week_number": get_week_number(investor.created.date()),
            "monday": current_week_start,
            "saturday": current_week_end,
            "total_referrals": 0,
            "level": 0,
            "status": "CURRENT",
        })

    return summaries