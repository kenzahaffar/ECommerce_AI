from fastembed import TextEmbedding

print("Chargement du modèle...")

modele = TextEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

textes = [
    "Le remboursement est possible pour une commande annulée.",
    "Le client peut suivre sa livraison avec son identifiant.",
    "Le paiement par carte bancaire a été refusé."
]

embeddings = list(modele.embed(textes))

print("\nNombre de textes :", len(embeddings))
print("Dimension du premier embedding :", len(embeddings[0]))

print("\nTest terminé avec succès !")