
# E-Commerce AI – Assistant intelligent pour une boutique en ligne

## 1. Présentation du projet

E-Commerce AI est une application basée sur l'intelligence artificielle qui aide les clients d'une boutique en ligne à obtenir des réponses à leurs demandes.

L'application utilise un modèle IA pour classifier les messages, répondre aux questions des clients et effectuer certaines opérations grâce à un agent intelligent.

## 2. Fonctionnalités principales

- Classification automatique des demandes : livraison, paiement, retour, commande et autre.
- Détection des demandes nécessitant une vérification humaine.
- Réponses aux questions à partir de documents grâce au RAG.
- Consultation du statut d'une commande.
- Calcul de l'éligibilité au remboursement.
- Création d'un ticket de support à la demande du client.

## 3. Technologies utilisées

- Python
- FastAPI
- Groq API
- Pydantic
- JSON
- FastEmbed
- Scikit-learn
- Uvicorn

## 4. Structure du projet

```text
ECommerce_AI/
├── app/
│   ├── main.py
│   ├── schemas.py
│   ├── config.py
│   ├── classifier.py
│   ├── rules.py
│   ├── rag.py
│   ├── agent.py
│   └── tools.py
├── data/
│   ├── commandes.json
│   ├── tickets.json
│   └── procedures/
├── evaluation/
│   ├── dataset.json
│   ├── evaluer.py
│   ├── comparer.py
│   └── evaluer_rag.py
├── tests/
├── results/
├── .env
├── .env.example
└── requirements.txt
```

## 5. Installation

Créer et activer l'environnement virtuel :

```bash
python -m venv venv
venv\Scripts\activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

Configurer le fichier `.env` avec les paramètres nécessaires :

```env
MODE=real
GROQ_API_KEY=votre_cle_api
GROQ_MODEL=openai/gpt-oss-20b
```

Ne jamais publier sa clé API sur GitHub.

## 6. Exécution

Lancer l'application :

```bash
python -m uvicorn app.main:app --reload
```

Documentation interactive de l'API :

http://127.0.0.1:8000/docs

## 7. Endpoints API

- `GET /health` : vérifier le fonctionnement de l'application.
- `POST /classify` : classifier une demande.
- `POST /chat` : répondre à une question avec le RAG.
- `POST /agent` : utiliser l'agent intelligent et ses outils.

## 8. Évaluation

Le projet utilise un dataset de 20 exemples annotés.

Résultats obtenus :

- Classification : 20/20 exemples corrects (100 %).
- Vérification humaine : 85 % d'exactitude.
- Comparaison des prompts :
  - Prompt 1 : 19/20 (95 %).
  - Prompt 2 : 20/20 (100 %).
- Évaluation RAG : Recall@3 = 1.0 et MRR = 1.0.

Le seuil de confiance utilisé pour demander une vérification humaine est de 0.70. Une vérification est également demandée lorsque la catégorie détectée est « autre ».

Ces résultats concernent le jeu de données utilisé et ne garantissent pas les mêmes performances sur tous les messages réels.

## 9. Sécurité et limites

- La clé API est stockée dans le fichier `.env`.
- Les réponses sont structurées et validées avec Pydantic.
- L'agent utilise trois outils avec un nombre limité d'étapes.
- La création d'un ticket nécessite une demande explicite du client.

## 10. Auteur

Projet réalisé dans le cadre d'un travail universitaire en développement des systèmes d'information.
