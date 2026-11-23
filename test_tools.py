from app.tools import (
    consulter_commande,
    calculer_remboursement,
    creer_ticket
)

print("=== Consultation ===")
print(consulter_commande("C1001"))

print("\n=== Remboursement ===")
print(calculer_remboursement("C1004"))

print("\n=== Création d'un ticket ===")
resultat = creer_ticket(
    client="Ahmed",
    message="Mon colis est arrivé endommagé.",
    categorie="livraison"
)

print(resultat)