from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# importando os elementos definidos no modelo
from model.base import Base
from model.pet import Pet

db_path = "database/"
# Verifica se o diretorio não existe
if not os.path.exists(db_path):
    # então cria o diretorio
    os.makedirs(db_path)

# url de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/pets.sqlite3' % db_path

# cria a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instancia um criador de seção com o banco
Session = sessionmaker(bind=engine)

# cria o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url)

# cria as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
def popula_base(session):
    """
    Popula a base de dados com alguns doguinhos de exemplo. 
    É importante para testar a API. 

    Args:
        Nada.
        
    Returns:
        Nada.
    """    
    nomes = [
        "Miuxa", "Meg", "Espeto", "Lola", "Frida", "Thor", "Mia", "Simba", "Nina", "Oscar",
        "Bella", "Toby", "Leo", "Luna", "Daisy", "Zeus", "Sadie", "Molly", "Cacau", "Buddy",
        "Rocky", "Bailey", "Coca", "Ginger", "Rex"
    ]

    racas = ["Lhasa", "Poodle", "Buldogue", "Golden Retriever", "Pastor Alemão", "Dálmata", "Beagle", "Boxer", "Rottweiler", "Pug"]
    idades = [12, 6, 11, 7, 8, 9, 1, 2, 3, 4, 12, 6, 11, 7, 8, 9, 1, 2, 3, 4, 4, 5, 6, 7, 8]
    telefones = ["(11) 91234-5678", "(21) 98765-4321", "(31) 97654-3210", "(41) 99876-5432", "(51) 98712-3456"]
    emails = ["email1@example.com", "email2@example.com", "email3@example.com", "email4@example.com", "email5@example.com"]

    for i in range(25):
        pet = Pet(
            nome=f"{nomes[i]}",
            raca=f"{racas[i % 10]}",
            idade= idades[i],
            tutor_telefone=f"{telefones[i % 5]}",
            tutor_email=f"{emails[i % 5]}"
        )
        session.add(pet)

    session.commit()
    session.close()    

with engine.connect() as connection:
    if not engine.dialect.has_table(connection, "pet"):
        print("Tabela 'pet' não existe.")
    else:
        session = Session()
        if session.query(Pet).count() == 0:
            print("Tabela 'pet' está vazia. Populando os dados.")
            popula_base(session)

