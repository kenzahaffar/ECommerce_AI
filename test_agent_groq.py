from app.agent import agent_groq

message = "Où est ma commande C1001 ?"

reponse = agent_groq(message)

print("Message :", message)
print("Réponse :", reponse)