import json
import sys
from pathlib import Path
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.classifier import classifier
from app.rules import appliquer_regles


FICHIER = Path(__file__).parent / "dataset.json"

with open(FICHIER, "r", encoding="utf-8") as f:
    dataset = json.load(f)

categories_reelles = []
categories_predites = []

total_verification_correcte = 0

for exemple in dataset:
    message = exemple["message"]
    categorie_attendue = exemple["categorie_attendue"]
    verification_attendue = exemple["verification_attendue"]

    resultat = classifier(message)
    resultat = appliquer_regles(resultat)

    categorie_predite = resultat.categorie.value

    categories_reelles.append(categorie_attendue)
    categories_predites.append(categorie_predite)

    if resultat.besoin_verification == verification_attendue:
        total_verification_correcte += 1

    print("\nMessage :", message)
    print("Catégorie attendue :", categorie_attendue)
    print("Catégorie prédite :", categorie_predite)
    print("Confiance :", resultat.confiance)
    print("Vérification humaine :", resultat.besoin_verification)


accuracy = accuracy_score(categories_reelles, categories_predites)

print("\n========== RÉSULTATS GLOBAUX ==========")
print("Nombre d'exemples :", len(dataset))
print("Accuracy :", round(accuracy, 3))
print(
    "Exactitude de la vérification humaine :",
    round(total_verification_correcte / len(dataset), 3)
)

print("\nRapport de classification :")
print(
    classification_report(
        categories_reelles,
        categories_predites,
        labels=["livraison", "paiement", "retour", "commande", "autre"],
        zero_division=0
    )
)

print("Matrice de confusion :")
print(
    confusion_matrix(
        categories_reelles,
        categories_predites,
        labels=["livraison", "paiement", "retour", "commande", "autre"]
    )
)