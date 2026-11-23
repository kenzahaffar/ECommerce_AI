from app.tools import (
    consulter_commande,
    calculer_remboursement,
    creer_ticket
)


OUTILS = [
    {
        "type": "function",
        "function": {
            "name": "consulter_commande",
            "description": "Consulter une commande à partir de son identifiant.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commande_id": {
                        "type": "string",
                        "description": "Identifiant de la commande, exemple C1001"
                    }
                },
                "required": ["commande_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculer_remboursement",
            "description": "Vérifier si une commande peut être remboursée et calculer le montant.",
            "parameters": {
                "type": "object",
                "properties": {
                    "commande_id": {
                        "type": "string"
                    }
                },
                "required": ["commande_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "creer_ticket",
            "description": "Créer un ticket uniquement lorsque le client demande explicitement de signaler ou d'enregistrer une réclamation.",
            "parameters": {
                "type": "object",
                "properties": {
                    "client": {"type": "string"},
                    "message": {"type": "string"},
                    "categorie": {
                        "type": "string",
                        "enum": [
                            "livraison",
                            "paiement",
                            "retour",
                            "commande",
                            "autre"
                        ]
                    }
                },
                "required": ["client", "message", "categorie"]
            }
        }
    }
]


def executer_outil(nom, arguments):
    outils = {
        "consulter_commande": consulter_commande,
        "calculer_remboursement": calculer_remboursement,
        "creer_ticket": creer_ticket
    }

    if nom not in outils:
        return {"erreur": "Outil inconnu"}

    return outils[nom](**arguments)
import json
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL


def agent_groq(message: str, max_tours: int = 5) -> str:

    client = Groq(api_key=GROQ_API_KEY)

    messages = [
        {
            "role": "system",
            "content": """
Tu es un assistant intelligent pour une boutique en ligne tunisienne.

Tu aides les clients concernant leurs commandes,
livraisons, paiements et remboursements.

RÈGLES OBLIGATOIRES :

1. UTILISATION DES OUTILS
- Utilise consulter_commande pour rechercher une commande.
- Utilise calculer_remboursement pour vérifier l'éligibilité
  d'une commande au remboursement.
- Utilise creer_ticket uniquement si le client demande
  explicitement de créer une réclamation.
- Ne crée jamais un ticket sans autorisation explicite.

2. EXACTITUDE DES INFORMATIONS
- N'invente jamais les informations d'une commande.
- Utilise uniquement les résultats retournés par les outils.
- Tous les montants sont exprimés en dinars tunisiens (DT).
- N'utilise jamais l'euro (€).

3. REMBOURSEMENT
- Si l'outil indique remboursement_possible = true,
  dis uniquement que le remboursement est possible.
- Ne dis jamais que le remboursement est confirmé,
  effectué, lancé ou en cours de traitement.
- L'application vérifie uniquement l'éligibilité.
  Elle n'effectue aucune opération de remboursement.
- N'invente aucun délai de remboursement.
- Ne promets aucune confirmation par e-mail.

4. LIVRAISON ET RÉCLAMATIONS
- N'invente aucun délai de livraison.
- Ne promets pas qu'un livreur ou un agent contactera le client.
- Ne prétends pas qu'une action a été réalisée si aucun outil
  ne l'a réellement effectuée.

5. COMMUNICATION
- Si une information est inconnue, indique-le clairement.
- Réponds toujours en français.
- Sois clair, poli et concis.
"""
        },
        {
            "role": "user",
            "content": message
        }
    ]

    for tour in range(max_tours):

        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            tools=OUTILS,
            tool_choice="auto"
        )

        choix = response.choices[0].message

        if not choix.tool_calls:
            return choix.content or "Je ne peux pas répondre à cette demande."

        messages.append(choix.model_dump(exclude_none=True))

        for appel in choix.tool_calls:

            nom = appel.function.name
            arguments = json.loads(appel.function.arguments)

            resultat = executer_outil(nom, arguments)

            messages.append({
                "role": "tool",
                "tool_call_id": appel.id,
                "content": json.dumps(
                    resultat,
                    ensure_ascii=False
                )
            })

    return "Le nombre maximal d'appels à l'agent a été atteint."