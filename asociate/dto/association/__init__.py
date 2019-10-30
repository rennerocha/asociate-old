from asociate.dto.request import InvalidRequestObject


class ListMembersRequestObject:
    def __init__(self, association_code):
        self.association_code = association_code

    @classmethod
    def from_dict(cls, adict):
        request = InvalidRequestObject()

        if "association_code" not in adict:
            request.add_error(parameter="association_code", message="Required")

        for key in adict.keys():
            if key != "association_code":
                request.add_error(parameter=key, message="Unexpected parameter")

        if request.has_errors():
            return request

        return cls(**adict)


class AddMemberRequestObject:
    def __init__(self, association_code, member):
        self.association_code = association_code
        self.member = member

    @classmethod
    def from_dict(cls, adict):
        request = InvalidRequestObject()

        if "association_code" not in adict:
            request.add_error(parameter="association_code", message="Required")
        if "member" not in adict:
            request.add_error(parameter="member", message="Required")

        for key in adict.keys():
            if key not in ("association_code", "member"):
                request.add_error(parameter=key, message="Unexpected parameter")

        if request.has_errors():
            return request

        return cls(**adict)

    def __eq__(self, other):
        return all(
            [
                self.association_code == other.association_code,
                self.member == other.member,
            ]
        )
