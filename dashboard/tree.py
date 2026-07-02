from referral.models import ReferralTree


def build_tree(user):
    """
    Recursively build referral tree.
    """

    node = {
        "investor": user,
        "position": "ROOT",
        "level": 0,
        "children": []
    }

    def add_children(parent_node, sponsor, level):
        referrals = ReferralTree.objects.filter(sponsor=sponsor)

        for referral in referrals:

            child_node = {
                "investor": referral.investor,
                "position": referral.position,
                "level": level,
                "children": []
            }

            add_children(
                child_node,
                referral.investor,
                level + 1
            )

            parent_node["children"].append(child_node)

    add_children(
        node,
        user,
        1
    )

    return node