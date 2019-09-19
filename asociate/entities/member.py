from dataclasses import dataclass


@dataclass(frozen=True)
class Member:
    first_name: str
    last_name: str
    email: str
    phone: str
    active: bool = False

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __repr__(self):
        return f"<Member: {self.first_name} {self.last_name}>"

    @property
    def full_name(self):
        return " ".join([self.first_name, self.last_name])

    def to_dict(self):
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "active": self.active,
        }

    def join(self, association):
        from asociate.entities.association import Association

        if not isinstance(association, Association):
            raise ValueError("Expected Association instance.")

        association.add_as_member(self)
