from app.agent import OUTILS, executer_outil

print("Nombre d'outils :", len(OUTILS))

for outil in OUTILS:
    print("Outil :", outil["function"]["name"])

print("\nTest d'exécution :")
resultat = executer_outil(
    "consulter_commande",
    {"commande_id": "C1001"}
)

print(resultat)