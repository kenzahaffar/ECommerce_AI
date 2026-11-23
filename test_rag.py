from app.rag import charger_documents, rechercher

print("Chargement des documents...")

passages = charger_documents()

print("Nombre de passages :", len(passages))

question = "Quelles sont les conditions de remboursement ?"

print("\nQuestion :", question)

resultats = rechercher(question, top_k=3)

for resultat in resultats:
    print("\nDocument :", resultat["document"])
    print("Score :", round(resultat["score"], 3))
    print("Passage :", resultat["passage"])