from accounts.models import Investor

from referral.models import ReferralTree




# ============================================================
# AADHAR RE-USE RULE (applies from investor #4 onward only -
# the first 3 "seed"/company accounts - CEO + 2 employees - are
# exempt, since they log in via a plain username, not their Aadhar)
# ============================================================
#
#   - An Aadhar not used before is always allowed.
#   - An Aadhar already used can be used again ONLY if:
#       a) the existing position's downline has fully completed
#          all 6 levels, AND
#       b) it has not already been reused 3 times (max 4 total
#          investor positions per Aadhar: the original + 3 reuses).
#   - Once an Aadhar has been used 4 times total, it is
#     permanently blocked from any further registration.

MAX_TOTAL_USES_PER_AADHAR = 4  # original + 3 reuses


def is_downline_fully_complete(investor, max_depth=6, _current_depth=0):

    if _current_depth >= max_depth:
        return True

    left = ReferralTree.objects.filter(sponsor=investor, position="LEFT").first()
    right = ReferralTree.objects.filter(sponsor=investor, position="RIGHT").first()

    if not left or not right:
        return False

    return (
        is_downline_fully_complete(left.investor, max_depth, _current_depth + 1)
        and
        is_downline_fully_complete(right.investor, max_depth, _current_depth + 1)
    )


def check_aadhar_allowed(aadhar):

    existing = Investor.objects.filter(aadhar=aadhar).order_by("-created")

    if not existing.exists():
        return True, None

    if existing.count() >= MAX_TOTAL_USES_PER_AADHAR:
        return False, "This Aadhar number has reached its maximum of 3 re-registrations and can no longer be used."

    latest_position = existing.first()

    if not is_downline_fully_complete(latest_position):
        return False, "This Aadhar's existing position has not yet completed all 6 levels, so it cannot be reused yet."

    return True, None


def get_current_level(investor, max_depth=6):
    """
    Real pair-completion level (0..max_depth), computed live:
    Level 1 = own LEFT+RIGHT both filled; Level N = both children
    have themselves reached level N-1, recursively.
    """

    level = 0
    current_row = [investor]

    while level < max_depth:

        next_row = []
        row_fully_paired = True

        for node in current_row:

            left = ReferralTree.objects.filter(sponsor=node, position="LEFT").first()
            right = ReferralTree.objects.filter(sponsor=node, position="RIGHT").first()

            if not left or not right:
                row_fully_paired = False
                break

            next_row.append(left.investor)
            next_row.append(right.investor)

        if not row_fully_paired:
            break

        level += 1
        current_row = next_row

    return level




def validate_sponsor(sponsor_id,position):


    sponsor_id=sponsor_id.strip().upper()


    sponsor=Investor.objects.filter(

        investor_id=sponsor_id,

        status="ACTIVE"

    ).first()



    if not sponsor:


        return None,"Sponsor is not active"




    exists=ReferralTree.objects.filter(

        sponsor=sponsor,

        position=position

    ).exists()



    if exists:


        return None,"Position already occupied"




    return sponsor,None






def calculate_level(sponsor):
    """
    STRUCTURAL DEPTH only (root=1, children=2...), used to cap tree
    rendering at 6 levels. NOT the pairs-completed level - use
    get_current_level() for that.
    """

    if sponsor is None:

        return 1



    node=ReferralTree.objects.filter(

        investor=sponsor

    ).first()



    if node:

        return node.level+1



    return 1




def sync_weekly_activity(new_investor):
    """
    Call right after creating a new ReferralTree node for new_investor.
    Updates the direct sponsor's weekly referral count and refreshes
    `level` for every ancestor up to the root.
    """

    from referral.models import WeeklyActivity
    from referral.utils import get_current_week_dates, get_week_number

    node = ReferralTree.objects.filter(investor=new_investor).first()

    if not node or not node.sponsor:
        return

    week_start, week_end = get_current_week_dates()

    ancestor = node.sponsor
    is_direct_sponsor = True

    while ancestor is not None:

        week_number = get_week_number(ancestor.created.date())

        WeeklyActivity.objects.filter(
            investor=ancestor, status="CURRENT"
        ).exclude(week_number=week_number).update(status="PREVIOUS")

        activity, _ = WeeklyActivity.objects.get_or_create(
            investor=ancestor,
            week_number=week_number,
            defaults={"monday": week_start, "saturday": week_end}
        )

        if is_direct_sponsor:
            activity.total_referrals = (activity.total_referrals or 0) + 1

        activity.level = get_current_level(ancestor)
        activity.status = "CURRENT"
        activity.save()

        ancestor_node = ReferralTree.objects.filter(investor=ancestor).first()
        ancestor = ancestor_node.sponsor if ancestor_node else None
        is_direct_sponsor = False