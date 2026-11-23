from app.schemas import ClassificationResult, CategorieDemande
from app.rules import appliquer_regles, verifier_message

resultat = ClassificationResult(
    categorie=CategorieDemande.AUTRE,
    confiance=0.90,
    justification="Demande générale.",
    besoin_verification=False
)

resultat = appliquer_regles(resultat)

print("Catégorie :", resultat.categorie.value)
print("Vérification nécessaire :", resultat.besoin_verification)

print("Message vide :", verifier_message(""))
print("Message valide :", verifier_message("Où est ma commande ?"))