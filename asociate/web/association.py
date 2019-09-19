import json
from flask import Blueprint, current_app, Response, render_template
from asociate.interactors.association import AssociationListMembers
from asociate.repository.postgresrepo import AssociationPostgresRepo

blueprint = Blueprint('association', __name__)


@blueprint.route('/association/<association_code>/members', methods=['GET'])
def association_members(association_code):
    repo = AssociationPostgresRepo(current_app.config["DB_CONNECTION_DATA"])
    interactor = AssociationListMembers(repo)
    
    response = interactor.execute(association_code)    

    context = {'members': response.value}

    return render_template(
        "members_list.html",
        **context,
    )