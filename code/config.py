# Adresse de connexion à MongoDB et nom de la base de données
# config.py : le seul fichier à modifier pour changer de base
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

MONGO_URI = "mongodb://localhost:27017/"
NOM_BASE = "bibliotheque"


def get_db():
    """Ouvre la connexion et renvoie la base, ou arrête le programme proprement."""
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=3000)
    try:
        client.admin.command("ping")
    except ServerSelectionTimeoutError:
        raise SystemExit("Impossible de joindre MongoDB : vérifiez qu'il est démarré.")
    return client[NOM_BASE]


# Règles métier de la bibliothèque
DUREE_EMPRUNT_JOURS = 14                 # durée normale d'un emprunt
DUREE_PROLONGATION_JOURS = 7             # durée ajoutée par une prolongation
MAX_PROLONGATIONS = 1                    # nombre maximal de prolongations par emprunt
TARIF_RETARD_PAR_JOUR = 100              # pénalité en FCFA par jour de retard
DELAI_EXPIRATION_RESERVATION_JOURS = 30  # une réservation non satisfaite expire après ce délai
