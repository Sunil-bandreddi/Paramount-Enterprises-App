from referral.models import ReferralTree



def build_tree(user):


    node = {


        "id": user.investor_id,


        "name": user.full_name,


        "status": user.status,


        "position": "ROOT",


        "children": []


    }



    children = ReferralTree.objects.filter(

        sponsor=user

    )



    for child in children:


        child_node = build_tree(

            child.investor

        )


        child_node["position"] = child.position


        node["children"].append(

            child_node

        )



    return node