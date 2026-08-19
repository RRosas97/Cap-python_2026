from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models.base import Base
from src.models.character import Character

server = "Hijo_del_Trueno"
db_name = "Users"
username = "sa"
password = "abcd123"

# query = "SELECT * FROM users;"

engine = create_engine(
    f"mssql+pyodbc://{username}:{password}@{server}/{db_name}?driver=ODBC+Driver+17+for+SQL+Server"
)

Session = sessionmaker(engine)
session = Session()

if __name__ == "__main__":
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    dr_Brown = Character(movie="Volver al futuro", name="Dr. Brown")
    clayton = Character(movie="Tarzan", name="Clayton", live=False)
    optimus_prime = Character(movie="Transformers", name="Optimus Prime")
    rocky = Character(movie="Terminator", name="Rocky Balboa")
    sr_arrow = Character(movie="???", name="Sr. Arrow")

    session.add(dr_Brown)
    session.add(clayton)
    session.add(optimus_prime)
    session.add(rocky)
    session.add(sr_arrow)

    session.commit()

    # SELECT * FROM characters

    # characters = session.query(Character).all()

    # characters = session.query(Character).filter(Character.id >=2).filter(Character.live)  # noqa: E501
    # characters = session.query(Character.id, Character.name, Character.movie)  # noqa: E501
    character = session.query(Character).filter(Character.movie == "Terminator").first()
    character.movie = "Rocky"
    session.add(character)

    characters = session.query(
        Character.id, Character.name, Character.movie
    )  # noqa: E501

    character = (
        session.query(Character)
        .filter(Character.movie == "???")
        .update(
            {
                Character.movie: "El planeta del tesoro",  # noqa: E501
                Character.live: False,
            }
        )
    )

    character = session.query(Character).filter(Character.id == 1).delete()

    session.commit()

    for character in characters:
        print(character)
