from app.classifier import classifier

messages = [
    "Où est ma commande C1001 ?",
    "Mon paiement a été refusé",
    "Je veux retourner mon produit",
    "Je n'ai pas reçu mon colis",
    "Bonjour, comment allez-vous ?"
]

for message in messages:
    resultat = classifier(message)

    print("\nMessage :", message)
    print("Catégorie :", resultat.categorie.value)
    print("Confiance :", resultat.confiance)