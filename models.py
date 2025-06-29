from database import Base
from sqlalchemy import Column,Integer,String,Boolean,Text,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType

class Utilisateur(Base):
    __tablename__ = 'utilisateur'
    id = Column(Integer, primary_key=True)
    nom = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    est_staff = Column(Boolean, default=False)
    est_actif = Column(Boolean, default=False)
    commandes = relationship('Commande', back_populates='utilisateur')
    
    def __repr__(self):
        return f"<Utilisateur {self.nom}"
    
class Commande(Base):
    
    STATUTS_COMMANDE = (
        ('EN_ATTENTE', 'en_attente'),
        ('EN_LIVRAISON', 'en_livraison'),
        ('LIVREE', 'livree'),
    )
    
    TAILLES_PIZZA = (
        ('PETITE', 'petite'),
        ('MOYENNE', 'moyenne'),
        ('GRANDE', 'grande'),
        ('FAMILIALE', 'familiale'),
    )
    
    __tablename__ = 'commandes'
    id = Column(Integer, primary_key=True)
    quantite = Column(Integer, nullable=False)
    statut_commande = Column(ChoiceType(choices=STATUTS_COMMANDE), default='EN_ATTENTE')
    taille_pizza = Column(ChoiceType(choices=TAILLES_PIZZA), default='PETITE')
    id_utilisateur = Column(Integer, ForeignKey('utilisateur.id'))
    utilisateur = relationship('Utilisateur', back_populates='commandes')
    
    def __repr__(self):
        return f"<Commande {self.id}>"