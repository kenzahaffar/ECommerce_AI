from pathlib import Path
import numpy as np
from fastembed import TextEmbedding


DOSSIER_PROCEDURES = Path(__file__).resolve().parent.parent / "data" / "procedures"

modele = TextEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

documents = []
passages = []


def charger_documents():

    global documents, passages

    documents = []
    passages = []

    for fichier in DOSSIER_PROCEDURES.glob("*.md"):

        contenu = fichier.read_text(encoding="utf-8")

        morceaux = [
            morceau.strip()
            for morceau in contenu.split("\n\n")
            if morceau.strip()
        ]

        for morceau in morceaux:
            documents.append(fichier.name)
            passages.append(morceau)

    return passages


def rechercher(question: str, top_k: int = 3):

    if not passages:
        charger_documents()

    if not passages:
        return []

    embeddings_documents = np.array(
        list(modele.embed(passages))
    )

    embedding_question = np.array(
        list(modele.embed([question]))
    )[0]

    scores = np.dot(
        embeddings_documents,
        embedding_question
    ) / (
        np.linalg.norm(embeddings_documents, axis=1)
        * np.linalg.norm(embedding_question)
        + 1e-10
    )

    meilleurs_indices = np.argsort(scores)[::-1][:top_k]

    resultats = []

    for indice in meilleurs_indices:
        resultats.append({
            "document": documents[indice],
            "passage": passages[indice],
            "score": float(scores[indice])
        })

    return resultats
from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL


def repondre_avec_rag(question: str) -> str:

    resultats = rechercher(question, top_k=3)

    if not resultats:
        return "Je n'ai pas trouvé cette information dans les documents."

    contexte = "\n\n".join(
        [
            f"Source : {r['document']}\n{r['passage']}"
            for r in resultats
        ]
    )

    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": """
Tu es un assistant pour une boutique en ligne.

Réponds uniquement à partir du contexte fourni.
N'invente aucune information.
Si le contexte ne contient pas la réponse,
indique que l'information est indisponible.
Réponds en français.
Indique le nom du document utilisé comme source.
"""
            },
            {
                "role": "user",
                "content": f"""
Question : {question}

Contexte :
{contexte}
"""
            }
        ]
    )

    return response.choices[0].message.content