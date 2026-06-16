from accounts.models import Investor

from referral.models import ReferralTree




def get_downline_count(user,level=0):


    if level>=6:

        return 0



    total=0



    children=ReferralTree.objects.filter(

        sponsor=user

    )



    for child in children:


        total+=1


        total+=get_downline_count(

            child.investor,

            level+1

        )



    return total






def check_aadhar_allowed(aadhar):


    users=Investor.objects.filter(

        aadhar=aadhar

    )



    if not users.exists():

        return True




    for user in users:


        if get_downline_count(user)<126:


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