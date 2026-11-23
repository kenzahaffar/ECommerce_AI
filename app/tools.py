import json
from pathlib import Path


FICHIER_COMMANDES = Path(__file__).resolve().parent.parent / "data" / "commandes.json"


def consulter_commande(commande_id: str) -> dict:
    with open(FICHIER_COMMANDES, "r", encoding="utf-8") as fichier:
        commandes = json.load(fichier)

    for commande in commandes:
        if commande["id"].lower() == commande_id.lower():
            return {
                "trouvee": True,
                "commande": commande
            }

    return {
        "trouvee": False,
        "message": "Commande introuvable."
    }
def calculer_remboursement(commande_id: str) -> dict:
    resultat = consulter_commande(commande_id)

    if not resultat["trouvee"]:
        return resultat

    commande = resultat["commande"]

    if commande["statut"] == "Annulée":
        montant = commande["montant"]
        return {
            "commande_id": commande_id,
            "remboursement_possible": True,
            "montant_remboursement": montant,
            "message": "Remboursement total possible."
        }

    return {
        "commande_id": commande_id,
        "remboursement_possible": False,
        "montant_remboursement": 0,
        "message": "Cette commande ne remplit pas les conditions de remboursement."
    }
FICHIER_TICKETS = Path(__file__).resolve().parent.parent / "data" / "tickets.json"


def creer_ticket(client: str, message: str, categorie: str) -> dict:
    with open(FICHIER_TICKETS, "r", encoding="utf-8") as fichier:
        tickets = json.load(fichier)

    nouveau_ticket = {
        "id": f"T{len(tickets) + 1:04d}",
        "client": client,
        "message": message,
        "categorie": categorie,
        "statut": "Ouvert"
    }

    tickets.append(nouveau_ticket)

    with open(FICHIER_TICKETS, "w", encoding="utf-8") as fichier:
        json.dump(tickets, fichier, ensure_ascii=False, indent=4)

    return {
        "succes": True,
        "ticket": nouveau_ticket
    }