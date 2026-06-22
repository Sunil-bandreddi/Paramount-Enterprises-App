from referral.models import ReferralTree
from accounts.models import Investor


def get_side_count(investor, position):

    count = 0


    node = ReferralTree.objects.filter(
        sponsor=investor,
        position=position
    ).first()


    if node:

        count = 1

        count += get_team_count(
            node.investor
        )


    return count





def get_team_count(investor, level=0):


    if level >= 6:

        return 0



    total = 0


    children = ReferralTree.objects.filter(
        sponsor=investor
    )


    for child in children:

        total += 1

        total += get_team_count(
            child.investor,
            level+1
        )


    return total





def get_pair_details(investor):


    left = get_side_count(
        investor,
        "LEFT"
    )


    right = get_side_count(
        investor,
        "RIGHT"
    )


    pairs = min(
        left,
        right
    )


    return {

        "left":left,

        "right":right,

        "pairs":pairs,

        "left_remaining":
        left-pairs,

        "right_remaining":
        right-pairs

    }






def build_chain(investor,level=0):


    if level>6:

        return None



    data={

        "investor":investor,

        "level":level,

        "children":[]

    }



    children=ReferralTree.objects.filter(

        sponsor=investor

    ).order_by(

        "position"

    )



    for child in children:


        node=build_chain(

            child.investor,

            level+1

        )


        if node:

            node["position"]=child.position

            data["children"].append(node)



    return data