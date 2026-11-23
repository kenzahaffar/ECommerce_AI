
from app.schemas import ClassificationResult, CategorieDemande


SEUIL_CONFIANCE = 0.70


def appliquer_regles(resultat: ClassificationResult) -> ClassificationResult:

    resultat.besoin_verification = (
        resultat.confiance < SEUIL_CONFIANCE
        or resultat.categorie == CategorieDemande.AUTRE
    )

    return resultat


def verifier_message(message: str) -> bool:
    return bool(message and message.strip())
