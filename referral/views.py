from django.http import JsonResponse

from django.contrib.auth.decorators import login_required

from referral.models import ReferralTree





def build_tree(user, level=0):


    # Maximum 6 Levels

    if level > 6:

        return None



    node = {


        "id":
        user.investor_id,


        "name":
        user.full_name,


        "status":
        user.status,


        "level":
        level,


        "children":[]

    }



    children = ReferralTree.objects.filter(

        sponsor=user

    ).order_by(

        "position"

    )



    for child in children:


        child_node = build_tree(

            child.investor,

            level + 1

        )


        if child_node:


            child_node["position"] = child.position


            node["children"].append(

                child_node

            )



    return node






@login_required

def tree_api(request):


    try:


        investor=request.user.investor



    except:


        return JsonResponse(

            {

            "error":
            "Investor profile not found"

            },

            status=400

        )



    data=build_tree(

        investor

    )



    return JsonResponse(

        data

    )