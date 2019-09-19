from asociate.response_objects import ResponseFailure, ResponseSuccess
from asociate.repository.exceptions import AssociationNotFoundError


class AssociationListMembers:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, association_code):
        try:
            return ResponseSuccess(
                value=self.repo.list_members(association_code)
            )
        except Exception as exc:
            return ResponseFailure(exc)