from dataclasses import dataclass


class Association:
    def __init__(self, code, name, slug):
        self._code = code
        self.name = name
        self.slug = slug
        self.memberships = set()

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return f"<Association: {self.name}>"

    @property
    def members(self):
        return [membership.member for membership in self.memberships]

    @property
    def code(self):
        return str(self._code)

    def add_as_member(self, member):
        from asociate.entities.member import Member

        if not isinstance(member, Member):
            raise ValueError("Expected Member instance.")

        self.memberships.add(Membership(association=self, member=member))


@dataclass(frozen=True)
class Membership:
    from asociate.entities.member import Member

    association: Association
    member: Member
