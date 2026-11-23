
import json
import sys
from pathlib import Path
from groq import Groq

sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.config import GROQ_API_KEY, GROQ_MODEL

FICHIER = Path(__file__).parent / "dataset.json"

with open(FICHIER, "r", encoding="utf-8") as f:
    dataset = json.load(f)

client = Groq(api_key=GROQ_API_KEY)


def classifier_test(message, consigne):
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": consigne},
            {"role": "user", "content": message}
        ],
        response_format={"type": "json_object"}
    )

    resultat = json.loads(response.choices[0].message.content)
    return resultat["categorie"]


consigne_1 = """
Classe le message dans une seule catégorie :
livraison, paiement, retour, commande ou autre.
Retourne uniquement un JSON avec le champ categorie.
"""

consigne_2 = """
Tu es un assistant spécialisé dans le commerce en ligne.
Classe chaque message selon son intention :
- livraison : colis, retard, colis endommagé ou non reçu
- paiement : carte bancaire, paiement refusé ou montant débité
- retour : retourner un produit ou demander un remboursement
- commande : suivi, annulation ou statut d'une commande
- autre : message hors sujet ou demande impossible à classer.
Retourne uniquement un JSON avec le champ categorie.
"""

bon_prompt = 0
simple_prompt = 0

for exemple in dataset:
    message = exemple["message"]
    attendu = exemple["categorie_attendue"]

    resultat_1 = classifier_test(message, consigne_1)
    resultat_2 = classifier_test(message, consigne_2)

    if resultat_1 == attendu:
        simple_prompt += 1

    if resultat_2 == attendu:
        bon_prompt += 1

print("\n========== COMPARAISON ==========")
print("Nombre d'exemples :", len(dataset))
print("Consigne 1 :", simple_prompt, "/", len(dataset))
print("Consigne 2 :", bon_prompt, "/", len(dataset))

print("Ecart :", abs(bon_prompt - simple_prompt), "exemple(s)")
