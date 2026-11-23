import pytest
from fastapi.testclient import TestClient

import app.main as main
from app.main import app
from app.schemas import ClassificationResult, CategorieDemande


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_classify():
    resultat = ClassificationResult(
        categorie=CategorieDemande.LIVRAISON,
        confiance=0.95,
        justification="Problème de livraison",
        besoin_verification=False
    )

    main.classifier = lambda message: resultat

    response = client.post(
        "/classify",
        json={"message": "Mon colis est en retard"}
    )

    assert response.status_code == 200
    assert response.json()["categorie"] == "livraison"


def test_chat(monkeypatch):
    monkeypatch.setattr(
        main,
        "repondre_avec_rag",
        lambda message: "Votre colis est en cours de livraison."
    )

    response = client.post(
        "/chat",
        json={"message": "Où est mon colis ?"}
    )

    assert response.status_code == 200
    assert "reponse" in response.json()


def test_agent(monkeypatch):
    monkeypatch.setattr(
        main,
        "agent_groq",
        lambda message: "Votre commande est confirmée."
    )

    response = client.post(
        "/agent",
        json={"message": "Consulter ma commande"}
    )

    assert response.status_code == 200
    assert "reponse" in response.json()


@pytest.mark.parametrize("route", ["/classify", "/chat", "/agent"])
def test_message_vide(route):
    response = client.post(
        route,
        json={"message": "   "}
    )

    assert response.status_code == 400