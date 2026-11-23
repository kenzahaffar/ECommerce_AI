from enum import Enum
from pydantic import BaseModel, Field


class CategorieDemande(str, Enum):
    LIVRAISON = "livraison"
    PAIEMENT = "paiement"
    RETOUR = "retour"
    COMMANDE = "commande"
    AUTRE = "autre"


class ClassificationResult(BaseModel):
    categorie: CategorieDemande
    confiance: float = Field(ge=0, le=1)
    justification: str = Field(min_length=1)
    besoin_verification: bool