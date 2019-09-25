from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from asociate.entities.member import Member as MemberEntity
from asociate.repository.exceptions import AssociationNotFoundError
from asociate.repository.models import Association, Base


class PostgresRepo:
    def __init__(self, connection_data):
        connection_string = "postgresql+psycopg2://{}:{}@{}/{}".format(
            connection_data["user"],
            connection_data["password"],
            connection_data["host"],
            connection_data["dbname"],
        )
        self.engine = create_engine(connection_string)
        Base.metadata.bind = self.engine


class AssociationPostgresRepo(PostgresRepo):
    def _create_association_members_objects_list(self, association):
        results = []
        for member in association.members:
            results.append(
                MemberEntity.from_dict(
                    {
                        "first_name": member.first_name,
                        "last_name": member.last_name,
                        "email": member.email,
                        "phone": member.phone,
                        "active": member.active,
                    }
                )
            )
        return results

    def list_members(self, association_code):
        DBSession = sessionmaker(bind=self.engine)
        session = DBSession()
        query = session.query(Association).filter(Association.code == association_code)
        association = query.first()

        if association is None:
            raise AssociationNotFoundError(
                f"Unable to find association with code {association_code}"
            )

        return self._create_association_members_objects_list(association)
