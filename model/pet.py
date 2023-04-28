from sqlalchemy import Column, String, Integer, DateTime
from datetime import datetime
from typing import Union

from model import Base


class Pet(Base):
    __tablename__ = 'pet'

    id = Column("pk_pet", Integer, primary_key=True)
    nome = Column(String(40), unique=False)
    raca = Column(String(80), unique=False)
    idade = Column(Integer)
    tutor_telefone = Column(String(20), unique=False)
    tutor_email = Column(String(80), unique=False)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, nome: str, raca: str, idade: int,
                 tutor_telefone: str, tutor_email: str,
                 data_insercao: Union[DateTime, None] = None):
        """
        Cria um Pet

        Arguments:
            nome: nome do pet
            raca: raça do pet
            idade = idade do pet
            tutor_telefone = telefone do responsável pela doação
            tutor_email = email do responsável pela doação
            data_insercao: data de quando o pet foi cadastrado
        """
        self.nome = nome
        self.raca = raca
        self.idade = idade
        self.tutor_telefone = tutor_telefone
        self.tutor_email = tutor_email

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
