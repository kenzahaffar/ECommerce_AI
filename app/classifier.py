from groq import Groq
from app.config import MODE, GROQ_API_KEY, GROQ_MODEL
from app.schemas import ClassificationResult


def classifier_mock(message: str) -> ClassificationResult:
    texte = message.lower()

    if any(mot in texte for mot in ["livraison", "colis", "livré", "reçu", "retard", "endommagé"]):
        categorie = "livraison"

    elif any(mot in texte for mot in ["paiement", "carte", "payé", "refusé"]):
        categorie = "paiement"

    elif any(mot in texte for mot in ["retour", "rembourser", "remboursement"]):
        categorie = "retour"

    elif any(mot in texte for mot in ["commande", "suivi", "commande numéro"]):
        categorie = "commande"

    else:
        categorie = "autre"

    return ClassificationResult(
        categorie=categorie,
        confiance=0.90,
        justification="Classification effectuée en mode mock.",
        besoin_verification=False
    )


def classifier_groq(message: str) -> ClassificationResult:
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Tu es un classificateur pour une boutique en ligne.

Classe le message dans une seule catégorie :
livraison, paiement, retour, commande ou autre.

Respecte strictement les types suivants :
- categorie : chaîne de caractères parmi les catégories autorisées
- confiance : nombre décimal entre 0 et 1
- justification : chaîne de caractères
Un colis endommagé ou non reçu appartient à la catégorie livraison.
Une demande de suivi ou de localisation d'une commande appartient à la catégorie commande.
Un produit reçu qui ne correspond pas à la commande appartient à la catégorie retour.
- besoin_verification : booléen true ou false

N'utilise jamais les mots "haute", "moyenne", "oui" ou "non"
pour remplacer les valeurs numériques et booléennes.
"""
            },
            {"role": "user", "content": message}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "classification",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "categorie": {
                            "type": "string",
                            "enum": [
                                "livraison",
                                "paiement",
                                "retour",
                                "commande",
                                "autre"
                            ]
                        },
                        "confiance": {
                            "type": "number"
                        },
                        "justification": {
                            "type": "string"
                        },
                        "besoin_verification": {
                            "type": "boolean"
                        }
                    },
                    "required": [
                        "categorie",
                        "confiance",
                        "justification",
                        "besoin_verification"
                    ],
                    "additionalProperties": False
                }
            }
        }
    )

    resultat = response.choices[0].message.content

    return ClassificationResult.model_validate_json(resultat)


def classifier(message: str) -> ClassificationResult:
    if MODE == "mock":
        return classifier_mock(message)

    return classifier_groq(message)