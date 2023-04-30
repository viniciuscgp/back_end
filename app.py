from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from pydantic import BaseModel, Field, ValidationError

from sqlalchemy.exc import IntegrityError

from model import Session
from model.pet import Pet
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Pets API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pet_tag = Tag(name="Pet", description="Adição, visualização e remoção de pets à base")


#---------- JEITO BIZZARO PARA PODER OBTER PARAMETROS DE URL :-|
class PetPath(BaseModel):
    pet_id: int = Field(..., description='pet id')


#-----------MOSTRA A DOCUMENTAÇÃO DA API 
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

#-----------ADICIONA UM NOVO PET À BASE DE DADOS 
@app.post('/pets', tags=[pet_tag], responses={"200": PetViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pet(form: PetSchema):
    """Adiciona um novo Pet à base de dados

    Retorna uma representação dos produtos e comentários associados.
    """
    pet = Pet(nome=form.nome, raca=form.raca, idade=form.idade, tutor_telefone=form.tutor_telefone, tutor_email=form.tutor_email)

    logger.debug(f"Adicionando pet de nome: '{pet.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando produto
        session.add(pet)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado produto de nome: '{pet.nome}'")
        return apresenta_pet(pet), 200
    
    except ValidationError as e:
        error_msg = "Erro de validação: " + str(e)
        logger.warning(f"Erro ao adicionar pet '{pet.nome}', {error_msg}")
        return {"message": error_msg}, 400    

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo pet :/"
        logger.warning(f"Erro ao adicionar o pet '{pet.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


#-----------ALTERA UM PET JÁ CASDASTRADO
@app.put('/pets/<int:pet_id>', tags=[pet_tag], responses={"200": PetViewSchema, "404": ErrorSchema, "400": ErrorSchema})
def update_pet(path: PetPath, form: PetSchema):
    """Atualiza um Pet baseado em seu ID

    Retorna uma representação do Pet alterado.
    """
    
    session = Session()

    pet = session.query(Pet).get(path.pet_id)

    if not pet:
        return {"Pet não encontrado": error_msg}, 404  

    # atualizando os campos do pet com os valores do formulário
    pet.nome = form.nome
    pet.raca = form.raca
    pet.idade = form.idade
    pet.tutor_telefone = form.tutor_telefone
    pet.tutor_email = form.tutor_email    

    logger.debug(f"Alterando o pet: '{pet.nome}'")
    try:
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Atualizado o pet: '{pet.nome}'")
        return apresenta_pet(pet), 200
    
    except ValidationError as e:
        error_msg = "Erro de validação: " + str(e)
        logger.warning(f"Erro ao atualizar pet de ID '{path.pet_id}', {error_msg}")
        return {"message": error_msg}, 400 

    except Exception as e:
        error_msg = "Não foi possível atualizar o pet :/"
        logger.warning(f"Erro ao atualizar o pet de ID '{path.pet_id}', {error_msg}")
        return {"mesage": error_msg}, 400


#-----------RETORNA TODOS OS PETS CADASTRADOS
@app.get('/pets', tags=[pet_tag], responses={"200": ListagemPetsSchema, "404": ErrorSchema})
def get_all_pets():
    """Faz a busca por todos os Pets cadastrados

    Retorna uma representação da listagem de Pets.
    """
    logger.debug(f"Coletando Pets ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pets = session.query(Pet).all()

    if not pets:
        # se não há produtos cadastrados
        return {"pets": []}, 200
    else:
        logger.debug(f"%d pets econtrados" % len(pets))
        # retorna a representação de produto
        print(pets)
        return apresenta_pets(pets), 200

#-----------RETORNA DADOS DO PET PELO ID, VER class PetPath ACIMA (bizarro)
@app.get('/pets/<int:pet_id>', tags=[pet_tag], responses={"200": PetViewSchema, "404": ErrorSchema})        
def get_pet_id(path: PetPath):
    """Faz a busca por um pet a partir do id

    Retorna uma representação JSON do pet encontrado.
    """
    logger.debug(f"Coletando dados sobre o pet #{path.pet_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pet = session.query(Pet).filter(Pet.id == path.pet_id).first()

    if not pet:
        # se o produto não foi encontrado
        error_msg = "Pet não encontrado na base :/"
        logger.warning(f"Erro ao buscar pet '{path.pet_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"pet econtrado: '{pet.nome}'")
        # retorna a representação de produto
        return apresenta_pet(pet), 200


#------------EXCLUI O PET PELO ID, VER class PetPath ACIMA (bizarro)
@app.delete('/pets/<int:pet_id>', tags=[pet_tag], responses={"200": PetViewSchema, "404": ErrorSchema})        
def del_pet_id(path: PetPath):
    """Deleta um Pet a partir do id informado

    Retorna uma mensagem de confirmação da remoção.
    """
    logger.debug(f"Deletando dados sobre o pet #{path.pet_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Pet).filter(Pet.id == path.pet_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado pet #{path.pet_id}")
        return {"mesage": "Pet removido", "id": path.pet_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Pet não encontrado na base :/"
        logger.warning(f"Erro ao deletar pet #'{path.pet_id}', {error_msg}")
        return {"mesage": error_msg}, 404


