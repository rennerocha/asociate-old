class Association:
    def __init__(self, code, name, slug):
        self._code = code
        self.name = name
        self.slug = slug

        self._members = []

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return f"<Association: {self.name}>"

    @property
    def members(self):
        return self._members

    @property
    def code(self):
        return str(self._code)

    def add_as_member(self, member):
        from asociate.entities.member import Member

        if not isinstance(member, Member):
            raise ValueError("Expected Member instance.")

        if member not in self._members:
            self._members.append(member)
