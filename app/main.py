from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.classifier import classifier
from app.rules import appliquer_regles, verifier_message
from app.rag import repondre_avec_rag
from app.agent import agent_groq


app = FastAPI(
    title="E-Commerce AI",
    description="Assistant intelligent pour une boutique en ligne",
    version="1.0"
)


class MessageRequest(BaseModel):
    message: str


@app.get("/health")
def health():
    return {
        "status": "ok",
        "application": "E-Commerce AI"
    }


@app.post("/classify")
def classify(request: MessageRequest):

    if not verifier_message(request.message):
        raise HTTPException(
            status_code=400,
            detail="Le message ne peut pas être vide."
        )

    resultat = classifier(request.message)
    resultat = appliquer_regles(resultat)

    return resultat


@app.post("/chat")
def chat(request: MessageRequest):

    if not verifier_message(request.message):
        raise HTTPException(
            status_code=400,
            detail="Le message ne peut pas être vide."
        )

    reponse = repondre_avec_rag(request.message)

    return {
        "question": request.message,
        "reponse": reponse
    }
@app.post("/agent")
def agent(request: MessageRequest):

    if not verifier_message(request.message):
        raise HTTPException(
            status_code=400,
            detail="Le message ne peut pas être vide."
        )

    reponse = agent_groq(request.message)

    return {
        "question": request.message,
        "reponse": reponse
    }