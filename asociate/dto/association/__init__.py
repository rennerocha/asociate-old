from asociate.dto.request import InvalidRequestObject


class ListMembersRequestObject:
    def __init__(self, association_code):
        self.association_code = association_code

    @classmethod
    def from_dict(cls, adict):
        request = InvalidRequestObject()

        if "association_code" not in adict:
            request.add_error(parameter="association_code", message="Required")

        for key, value in adict.items():
            if key != "association_code":
                request.add_error(parameter=key, message="Unexpected parameter")

        if request.has_errors():
            return request

        return cls(**adict)