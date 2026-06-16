from urllib import request

from django.shortcuts import render,redirect

from django.contrib.auth.decorators import login_required


from referral.models import ReferralTree
from referral.utils import get_referral_week_summaries, get_week_status


from referral.views import build_tree

from accounts.models import Investor



@login_required
def dashboard(request):


    # investor = request.user.investor


    investor = Investor.objects.filter(user=request.user).first()

    if not investor:
       return redirect("administrator:admin_dashboard")

    # -----------------------------
    # Complete Referral Tree
    # -----------------------------

    tree_data = build_tree(

        investor

    )



    # -----------------------------
    # Direct Referrals
    # -----------------------------

    direct_children = ReferralTree.objects.filter(

        sponsor=investor

    )



    monday, saturday = get_week_status()
    week_summaries = get_referral_week_summaries(investor)
    current_week = [week for week in week_summaries if week["status"] == "CURRENT"]
    previous_weeks = [week for week in week_summaries if week["status"] == "PREVIOUS"]



    # -----------------------------
    # Total Team Count
    # -----------------------------

    total_team = 0



    node = ReferralTree.objects.filter(

        investor=investor

    ).first()



    if node:

        total_team = node.team_count()



    return render(

        request,

        "dashboard.html",

        {


        "investor": investor,


        "tree_data": tree_data,


        "children": direct_children,


        "current_week": current_week,


        "previous_weeks": previous_weeks,


        "monday": monday,


        "saturday": saturday,


        "total_team": total_team,


        "can_refer":

            investor.status == "ACTIVE",


        "direct_count": direct_children.count(),


        }

    )
