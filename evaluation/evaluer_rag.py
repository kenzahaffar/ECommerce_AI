import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.rag import charger_documents, rechercher

charger_documents()

tests = [
    {
        "question": "Quelles sont les conditions de remboursement ?",
        "document_attendu": "remboursement.md"
    },
    {
        "question": "Comment suivre ma livraison ?",
        "document_attendu": "livraison.md"
    },
    {
        "question": "Que faire si mon paiement est refusé ?",
        "document_attendu": "paiement.md"
    },
    {
        "question": "Comment obtenir le remboursement d'une commande annulée ?",
        "document_attendu": "remboursement.md"
    },
    {
        "question": "Quels moyens de paiement sont acceptés ?",
        "document_attendu": "paiement.md"
    }
]

total_recall = 0
total_mrr = 0

for test in tests:

    resultats = rechercher(test["question"], top_k=3)

    documents = [r["document"] for r in resultats]
    attendu = test["document_attendu"]

    recall = 1 if attendu in documents else 0
    total_recall += recall

    rang = 0

    for position, document in enumerate(documents, start=1):
        if document == attendu:
            rang = position
            break

    mrr = 1 / rang if rang != 0 else 0
    total_mrr += mrr

    print("\nQuestion :", test["question"])
    print("Document attendu :", attendu)
    print("Documents retrouvés :", documents)
    print("Recall@3 :", recall)
    print("RR :", round(mrr, 3))


print("\n========== RÉSULTATS GLOBAUX ==========")
print("Recall@3 :", round(total_recall / len(tests), 3))
print("MRR :", round(total_mrr / len(tests), 3))