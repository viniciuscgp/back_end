from pydantic import BaseModel, validator
from typing import List
from model.pet import Pet


class PetSchema(BaseModel):
    """ Define como um novo pet a ser inserido deve ser representado
    """
    nome = "Miuxa"
    raca = "Lhasa"
    idade = 12
    tutor_telefone =  "24-99999999"
    tutor_email = "responsavel.contato@gmuil.com"

    @validator('idade')
    def validate_idade(cls, idade):
        if idade < 0:
            raise ValueError("A idade do pet deve ser maior ou igual a 0")
        return idade    



class PetBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do pet.
    """
    nome: str = "Miuxa"


class ListagemPetsSchema(BaseModel):
    """ Define como uma listagem de pets será retornada.
    """
    pets: List[PetSchema]

class PetViewSchema(BaseModel):
    """ Define como um pet será retornado: pet
    """
    id: int = 1
    nome: str = "Miuxa"
    raca: str = "Lhasa"
    idade: int = 12
    tutor_telefone: str =  "24-99999999"
    tutor_email: str = "responsavel.contato@gmuil.com"



class PetDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str


def apresenta_pets(pets: List[Pet]):
    """ Retorna uma representação do pet seguindo o schema definido em
        PetViewSchema.
    """
    result = []
    for pet in pets:
        result.append({
            "id": pet.id,
            "nome": pet.nome,
            "raca": pet.raca,
            "idade": pet.idade,
            "tutor_telefone":pet.tutor_telefone,
            "tutor_email":pet.tutor_email
        })

    return {"pets": result}


def apresenta_pet(pet: Pet):
    """ Retorna uma representação do pet seguindo o schema definido em
        PetViewSchema.
    """
    return {
        "id": pet.id,
        "nome": pet.nome,
        "raca": pet.raca,
        "idade": pet.idade,
        "tutor_telefone": pet.tutor_telefone,
        "tutor_email": pet.tutor_email
    }
