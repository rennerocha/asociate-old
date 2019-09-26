from flask import Blueprint, current_app, render_template
from asociate.dto.association import ListMembersRequestObject
from asociate.interactors.association import AssociationListMembers
from asociate.repository.postgresrepo import AssociationPostgresRepo

blueprint = Blueprint("association", __name__)


@blueprint.route("/association/<association_code>/members", methods=["GET"])
def association_members(association_code):
    repo = AssociationPostgresRepo(
        current_app.config["DB_CONNECTION_STRING"], current_app.engine
    )
    interactor = AssociationListMembers(repo)

    request = ListMembersRequestObject.from_dict({"association_code": association_code})
    response = interactor.execute(request)

    if not response:
        context = {"message": response.value["message"]}

        return render_template("error.html", **context), 404
    else:
        context = {"members": response.value}

        return render_template("members_list.html", **context)
