from accounts.models import Investor

from referral.models import ReferralTree




def get_downline_count(user,level=0):


    if level > 6:
        return True

    left = ReferralTree.objects.filter(
        sponsor=user,
        position="LEFT"
    ).first()

    right = ReferralTree.objects.filter(
        sponsor=user,
        position="RIGHT"
    ).first()

    if not left or not right:
        return False

    return (
        get_downline_count(left.investor, level + 1)
        and
        get_downline_count(right.investor, level + 1)
    )



def check_aadhar_allowed(aadhar):

    users = Investor.objects.filter(
        aadhar=aadhar
    )

    if not users.exists():
        return True

    for user in users:

        if not get_downline_count(user):
            return False

    return True






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


    if sponsor is None:

        return 1



    node=ReferralTree.objects.filter(

        investor=sponsor

    ).first()



    if node:

        return node.level+1



    return 1