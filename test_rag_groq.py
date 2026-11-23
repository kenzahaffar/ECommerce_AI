from app.rag import repondre_avec_rag

question = "Quels sont les horaires d'ouverture de la boutique ?"

reponse = repondre_avec_rag(question)

print("Question :", question)
print("\nRéponse :", reponse)