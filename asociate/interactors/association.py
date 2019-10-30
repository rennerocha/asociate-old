from asociate.dto.response import ResponseFailure, ResponseSuccess
from asociate.repository.exceptions import AssociationNotFoundError


class AssociationListMembers:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, request):
        try:
            return ResponseSuccess(
                value=self.repo.list_members(request.association_code)
            )
        except Exception as exc:
            return ResponseFailure(exc)


class AssociationAddMember:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, request):
        from asociate.entities.member import Member

        try:
            self.repo.add_member(request.association_code, request.member)
            return ResponseSuccess(value=Member.from_dict(request.member))
        except Exception as exc:
            return ResponseFailure(exc)
