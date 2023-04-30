from .pet import Pet


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
