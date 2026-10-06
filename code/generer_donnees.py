# Génère et insère le jeu de données dans la base
import random
from datetime import datetime, timedelta

from config import (
    get_db,
    DUREE_EMPRUNT_JOURS,
    DUREE_PROLONGATION_JOURS,
    MAX_PROLONGATIONS,
    TARIF_RETARD_PAR_JOUR,
    DELAI_EXPIRATION_RESERVATION_JOURS,
)

db = get_db()

# Date de référence du projet : on ne lit jamais l'horloge du système
AUJOURDHUI = datetime(2026, 10, 6)

NOMS = [
    "Mbarga", "Essomba", "Fotso", "Kamga", "Tchoupo", "Ngono", "Atangana",
    "Owona", "Ndongo", "Abena", "Ekane", "Manga", "Njoya", "Tchuente", "Nana",
    "Wamba", "Djoumessi", "Nkoulou", "Etoa", "Mvondo", "Bella", "Onana",
    "Talla", "Simo", "Kuete", "Ngassa", "Moukoko", "Eboa", "Hamadou", "Bouba",
]
PRENOMS = [
    "Jean", "Marie", "Paul", "Aïcha", "Boris", "Carine", "Hervé", "Christelle",
    "Arnaud", "Sandrine", "Yannick", "Gaëlle", "Franck", "Brenda", "Steve",
    "Larissa", "Ibrahim", "Fadimatou", "Rachel", "Cédric", "Ornella",
    "Wilfried", "Danielle", "Ulrich", "Mireille", "Patrick", "Estelle",
]


def date_aleatoire(debut, fin):
    """Renvoie une date (à minuit) tirée au hasard entre debut et fin inclus."""
    return debut + timedelta(days=random.randint(0, (fin - debut).days))


def generer_lecteurs(nombre):
    """Crée les lecteurs (étudiants, enseignants, personnel) avec leur carte."""
    filieres = ["GIT", "SDIA", "Génie civil", "Génie électrique", "Droit",
                "Économie", "Mathématiques", "Médecine"]
    departements = ["Informatique", "Génie civil", "Mathématiques", "Droit",
                    "Économie", "Bibliothèque", "Scolarité"]
    max_par_categorie = {"étudiant": 3, "enseignant": 5, "personnel": 2}

    lecteurs = []
    for i in range(1, nombre + 1):
        categorie = random.choices(["étudiant", "enseignant", "personnel"],
                                   weights=[75, 15, 10])[0]
        # Environ 12 % des cartes sont déjà expirées à AUJOURDHUI
        if random.random() < 0.12:
            date_expiration = date_aleatoire(AUJOURDHUI - timedelta(days=300),
                                             AUJOURDHUI - timedelta(days=1))
        else:
            date_expiration = date_aleatoire(AUJOURDHUI + timedelta(days=30),
                                             AUJOURDHUI + timedelta(days=900))
        lecteur = {
            "numero_carte": f"CARTE-{i:04d}",
            "nom": random.choice(NOMS),
            "prenom": random.choice(PRENOMS),
            "categorie": categorie,
            "date_inscription": date_aleatoire(AUJOURDHUI - timedelta(days=1200),
                                               AUJOURDHUI - timedelta(days=60)),
            "date_expiration": date_expiration,
            "max_emprunts": max_par_categorie[categorie],
        }
        if categorie == "étudiant":
            lecteur["filiere"] = random.choice(filieres)
        else:
            lecteur["departement"] = random.choice(departements)
        lecteurs.append(lecteur)

    db.lecteurs.delete_many({})
    db.lecteurs.insert_many(lecteurs)
    db.lecteurs.create_index("numero_carte", unique=True)
    print(f"{len(lecteurs)} lecteurs insérés")


# ---------------------------------------------------------------------------
# Données de référence pour les ouvrages
# ---------------------------------------------------------------------------

EDITEURS = [
    "Presses Universitaires de Yaoundé", "Éditions CLÉ", "L'Harmattan Cameroun",
    "Presses de l'UCAC", "Éditions Ifrikiya", "Afredit", "Dunod", "Eyrolles",
    "Ellipses", "Presses Universitaires d'Afrique",
]

# Pour chaque domaine : sujets, genre secondaire possible et mots-clés
DOMAINES = {
    "informatique": {
        "sujets": ["Algorithmique", "Bases de données relationnelles",
                   "Réseaux informatiques", "Programmation en Python",
                   "Programmation orientée objet en Java", "Intelligence artificielle",
                   "Big Data et NoSQL", "Sécurité des systèmes d'information",
                   "Systèmes d'exploitation", "Génie logiciel",
                   "Apprentissage automatique", "Développement web"],
        "genres_associes": ["science des données", "mathématiques"],
        "mots_cles": ["algorithme", "programmation", "données", "réseau", "python",
                      "sécurité", "logiciel", "mongodb", "web", "cloud"],
    },
    "génie civil": {
        "sujets": ["Béton armé", "Résistance des matériaux", "Mécanique des sols",
                   "Topographie", "Routes et ouvrages d'art", "Hydraulique urbaine",
                   "Construction métallique", "Géotechnique des sols latéritiques",
                   "Dessin technique du bâtiment", "Gestion de chantier"],
        "genres_associes": ["physique", "mathématiques"],
        "mots_cles": ["béton", "structure", "sol", "chantier", "pont", "route",
                      "matériaux", "eurocode", "fondation"],
    },
    "mathématiques": {
        "sujets": ["Analyse réelle", "Algèbre linéaire", "Probabilités",
                   "Statistique inférentielle", "Analyse numérique",
                   "Équations différentielles", "Recherche opérationnelle",
                   "Topologie", "Théorie des graphes", "Optimisation convexe"],
        "genres_associes": ["informatique", "physique"],
        "mots_cles": ["matrice", "intégrale", "probabilité", "statistique",
                      "graphe", "optimisation", "théorème", "suite"],
    },
    "physique": {
        "sujets": ["Mécanique du point", "Électromagnétisme", "Thermodynamique",
                   "Électronique analogique", "Optique géométrique",
                   "Énergies renouvelables", "Électrotechnique"],
        "genres_associes": ["génie civil", "mathématiques"],
        "mots_cles": ["énergie", "force", "circuit", "chaleur", "onde",
                      "solaire", "électricité"],
    },
    "droit": {
        "sujets": ["Droit constitutionnel camerounais", "Droit OHADA des affaires",
                   "Droit civil des obligations", "Droit pénal général",
                   "Droit administratif", "Droit du travail",
                   "Droit foncier au Cameroun", "Droit international public",
                   "Procédure civile", "Droit des sociétés commerciales"],
        "genres_associes": ["économie", "histoire"],
        "mots_cles": ["ohada", "constitution", "contrat", "jurisprudence",
                      "tribunal", "société", "foncier", "code pénal"],
    },
    "économie": {
        "sujets": ["Microéconomie", "Macroéconomie", "Comptabilité générale OHADA",
                   "Économie du développement", "Finance d'entreprise",
                   "Économétrie", "Marketing", "Monnaie et banque en zone CEMAC"],
        "genres_associes": ["mathématiques", "droit"],
        "mots_cles": ["marché", "croissance", "cemac", "fcfa", "banque",
                      "comptabilité", "investissement", "inflation"],
    },
    "médecine": {
        "sujets": ["Anatomie humaine", "Physiologie", "Pharmacologie",
                   "Santé publique en Afrique", "Paludisme et maladies tropicales",
                   "Pédiatrie"],
        "genres_associes": ["santé publique"],
        "mots_cles": ["santé", "paludisme", "diagnostic", "anatomie",
                      "épidémiologie", "traitement"],
    },
}

# Modèles de titres pour les domaines académiques
MODELES_TITRES = ["{}", "{} : cours et exercices corrigés",
                  "{} : théorie et applications", "{} : fondements et pratique"]

TITRES_ROMANS = [
    "Les pluies de Bafoussam", "Le chant du Wouri", "La fille du chef de Foumban",
    "Les orphelins de Mokolo", "Un été à Kribi", "Le marché de Mvog-Mbi",
    "Les silences du mont Cameroun", "Le retour de l'enfant prodigue",
    "La lettre de Garoua", "Les tambours de la forêt", "Une saison à Ebolowa",
    "Le taxi jaune", "Les veilleurs de Limbé", "Mémoires d'un instituteur",
    "La promesse de Maroua", "Le baobab et l'étudiant",
]
MOTS_CLES_ROMANS = ["famille", "amour", "village", "ville", "tradition",
                    "exil", "jeunesse", "société"]

TITRES_HISTOIRE = [
    "Histoire du Cameroun des origines à nos jours",
    "Le Cameroun sous mandat français et britannique",
    "La réunification du Cameroun (1961)",
    "Les royaumes bamiléké : histoire et traditions",
    "Le sultanat bamoun et le roi Njoya",
    "Histoire de l'Afrique centrale précoloniale",
    "La décolonisation en Afrique subsaharienne",
    "Douala, ville portuaire : une histoire",
    "Les lamidats du Nord-Cameroun",
    "Histoire économique de l'Afrique contemporaine",
    "Les grandes figures de l'indépendance africaine",
]
MOTS_CLES_HISTOIRE = ["colonisation", "indépendance", "royaume", "mémoire",
                      "patrimoine", "afrique centrale", "archives"]

THEMES_MEMOIRES = [
    "Conception d'un système de gestion de bibliothèque avec MongoDB",
    "Analyse de la qualité de l'eau potable à Yaoundé",
    "Étude de la stabilité des sols latéritiques de l'Ouest-Cameroun",
    "Prédiction des rendements agricoles par apprentissage automatique",
    "Le régime juridique du foncier au Cameroun",
    "Impact du mobile money sur l'inclusion financière",
    "Dimensionnement d'un pont en béton armé sur le Wouri",
    "Détection de fraudes bancaires par réseaux de neurones",
    "Optimisation du réseau électrique de la ville de Douala",
    "La protection des données personnelles en droit camerounais",
]

# Nombre d'ouvrages papier par domaine (total = 120)
REPARTITION_PAPIER = {
    "informatique": 20, "génie civil": 15, "mathématiques": 15, "physique": 10,
    "droit": 15, "économie": 12, "médecine": 8, "roman": 15, "histoire": 10,
}


def generer_auteurs():
    """Renvoie une liste de 1 à 3 noms d'auteurs."""
    return [f"{random.choice(PRENOMS)} {random.choice(NOMS)}"
            for _ in range(random.randint(1, 3))]


def titres_academiques(domaine, nombre, deja_pris):
    """Tire `nombre` titres distincts pour un domaine académique."""
    candidats = [m.format(s) for s in DOMAINES[domaine]["sujets"] for m in MODELES_TITRES]
    candidats = [t for t in candidats if t not in deja_pris]
    return random.sample(candidats, nombre)


def description_ouvrage(domaine, titre):
    """Construit les champs communs (hors code et type) d'un ouvrage."""
    if domaine == "roman":
        genres = ["roman"] + random.sample(["littérature africaine"], random.randint(0, 1))
        mots = MOTS_CLES_ROMANS
    elif domaine == "histoire":
        genres = ["histoire"] + random.sample(["sciences politiques"], random.randint(0, 1))
        mots = MOTS_CLES_HISTOIRE
    else:
        infos = DOMAINES[domaine]
        genres = [domaine] + random.sample(infos["genres_associes"], random.randint(0, 1))
        mots = infos["mots_cles"]
    return {
        "titre": titre,
        "auteurs": generer_auteurs(),
        "editeur": random.choice(EDITEURS),
        "annee": random.randint(1995, 2025),
        "genres": genres,
        "mots_cles": random.sample(mots, random.randint(2, 4)),
    }


def generer_ouvrages():
    """Crée 150 ouvrages : 120 papier (avec exemplaires) et 30 numériques."""
    titres_pris = set()

    # 1. Description des 120 ouvrages papier
    papiers = []
    for domaine, nombre in REPARTITION_PAPIER.items():
        if domaine == "roman":
            titres = random.sample(TITRES_ROMANS, nombre)
        elif domaine == "histoire":
            titres = random.sample(TITRES_HISTOIRE, nombre)
        else:
            titres = titres_academiques(domaine, nombre, titres_pris)
        titres_pris.update(titres)
        papiers += [description_ouvrage(domaine, t) for t in titres]

    # 2. Description des 30 ouvrages numériques : 12 pdf, 8 vidéos, 10 mémoires
    numeriques = []
    domaines_academiques = list(DOMAINES)
    for format_doc, nombre in [("pdf", 12), ("vidéo", 8), ("mémoire", 10)]:
        for i in range(nombre):
            if format_doc == "mémoire":
                domaine = random.choice(domaines_academiques)
                titre = "Mémoire de master : " + THEMES_MEMOIRES[i]
            else:
                domaine = random.choice(domaines_academiques)
                titre = titres_academiques(domaine, 1, titres_pris)[0]
                if format_doc == "vidéo":
                    titre = "Cours vidéo - " + titre
            titres_pris.add(titre)
            doc = description_ouvrage(domaine, titre)
            doc["format"] = format_doc
            numeriques.append(doc)

    # 3. Ordre aléatoire puis attribution des codes OUV-0001...
    tous = [("papier", d) for d in papiers] + [("numérique", d) for d in numeriques]
    random.shuffle(tous)
    ouvrages = []
    for i, (type_doc, desc) in enumerate(tous, start=1):
        code = f"OUV-{i:04d}"
        ouvrage = {"code": code, **desc, "type": type_doc}
        if type_doc == "papier":
            ouvrage["exemplaires"] = [
                {"cote": f"{code}-{chr(65 + k)}",
                 "etat": random.choices(["neuf", "bon", "abîmé"], weights=[30, 55, 15])[0],
                 "disponible": True}
                for k in range(random.randint(2, 5))
            ]
        else:
            extension = {"pdf": "pdf", "vidéo": "mp4", "mémoire": "pdf"}[ouvrage["format"]]
            ouvrage["lien"] = f"https://bibliotheque.univ.cm/numerique/{code}.{extension}"
            if ouvrage["format"] == "vidéo":
                ouvrage["taille_mo"] = round(random.uniform(150, 1200), 1)
            else:
                ouvrage["taille_mo"] = round(random.uniform(0.5, 25), 1)
        ouvrages.append(ouvrage)

    # 4. Au moins 400 exemplaires : on complète si nécessaire
    papiers_doc = [o for o in ouvrages if o["type"] == "papier"]
    total = sum(len(o["exemplaires"]) for o in papiers_doc)
    while total < 400:
        o = random.choice([p for p in papiers_doc if len(p["exemplaires"]) < 5])
        k = len(o["exemplaires"])
        o["exemplaires"].append({"cote": f"{o['code']}-{chr(65 + k)}",
                                 "etat": "neuf", "disponible": True})
        total += 1

    db.ouvrages.delete_many({})
    db.ouvrages.insert_many(ouvrages)
    db.ouvrages.create_index("code", unique=True)
    print(f"{len(ouvrages)} ouvrages insérés ({total} exemplaires)")


# ---------------------------------------------------------------------------
# Emprunts
# ---------------------------------------------------------------------------

# Fin fictive d'un emprunt en cours, pour les tests de chevauchement
FIN_EN_COURS = AUJOURDHUI + timedelta(days=3650)


def se_chevauchent(debut1, fin1, debut2, fin2):
    """Vrai si les intervalles fermés [debut1, fin1] et [debut2, fin2] se touchent."""
    return debut1 <= fin2 and debut2 <= fin1


def exemplaire_libre(occupations, cote, debut, fin):
    """Vrai si l'exemplaire n'a aucun emprunt qui chevauche [debut, fin]."""
    return all(not se_chevauchent(debut, fin, d, f) for d, f in occupations[cote])


def lecteur_peut_emprunter(lecteur, occupations, debut, fin):
    """Vrai si le lecteur a le droit d'emprunter sur la période [debut, fin].

    - la carte doit être valide au début de l'emprunt
      (et encore valide AUJOURDHUI si l'emprunt est en cours) ;
    - le nombre de ses emprunts qui chevauchent la période doit rester
      strictement inférieur à max_emprunts : il ne peut donc jamais le dépasser.
    """
    if not (lecteur["date_inscription"] <= debut <= lecteur["date_expiration"]):
        return False
    if fin == FIN_EN_COURS and lecteur["date_expiration"] < AUJOURDHUI:
        return False
    simultanes = sum(1 for d, f in occupations[lecteur["numero_carte"]]
                     if se_chevauchent(debut, fin, d, f))
    return simultanes < lecteur["max_emprunts"]


def choisir_lecteur(lecteurs, occupations_lecteurs, debut, fin):
    """Renvoie un lecteur autorisé à emprunter sur [debut, fin], ou None."""
    for lecteur in random.sample(lecteurs, len(lecteurs)):
        if lecteur_peut_emprunter(lecteur, occupations_lecteurs, debut, fin):
            return lecteur
    return None


def generer_emprunts():
    """Crée environ 600 emprunts cohérents sur les exemplaires papier.

    Chaque exemplaire et chaque lecteur possède la liste des périodes où il est
    occupé ; un emprunt n'est créé que si ces deux listes l'autorisent.
    """
    lecteurs = list(db.lecteurs.find())
    papiers = list(db.ouvrages.find({"type": "papier"}))
    nb_en_cours, nb_rendus = 90, 510
    nb_en_cours_retard = 20

    occupations_ex = {ex["cote"]: [] for o in papiers for ex in o["exemplaires"]}
    occupations_lec = {l["numero_carte"]: [] for l in lecteurs}
    emprunts = []

    def enregistrer(ouvrage, cote, lecteur, debut, prolongations, retour_effectif):
        """Ajoute l'emprunt et marque l'exemplaire et le lecteur comme occupés."""
        duree = DUREE_EMPRUNT_JOURS + prolongations * DUREE_PROLONGATION_JOURS
        fin = retour_effectif if retour_effectif else FIN_EN_COURS
        occupations_ex[cote].append((debut, fin))
        occupations_lec[lecteur["numero_carte"]].append((debut, fin))
        emprunts.append({
            "numero_carte": lecteur["numero_carte"],
            "code_ouvrage": ouvrage["code"],
            "cote": cote,
            "date_emprunt": debut,
            "date_retour_prevu": debut + timedelta(days=duree),
            "date_retour_effectif": retour_effectif,
            "nb_prolongations": prolongations,
        })

    # Popularité inégale : poids décroissant selon un rang tiré au hasard
    rangs = random.sample(range(1, len(papiers) + 1), len(papiers))
    poids = {o["code"]: 1 / r ** 0.9 for o, r in zip(papiers, rangs)}

    # 1. Emprunts en cours ------------------------------------------------
    # 12 titres (parmi ceux à 2 ou 3 exemplaires) ont TOUS leurs exemplaires sortis
    petits = [o for o in papiers if len(o["exemplaires"]) <= 3]
    titres_complets = random.sample(petits, 12)
    a_sortir = [(o, ex["cote"]) for o in titres_complets for ex in o["exemplaires"]]
    for o in titres_complets:
        poids[o["code"]] *= 3  # titres très demandés
    deja = {cote for _, cote in a_sortir}
    autres = [(o, ex["cote"]) for o in papiers if o not in titres_complets
              for ex in o["exemplaires"]]
    while len(a_sortir) < nb_en_cours:
        o, cote = random.choices(autres, weights=[poids[o["code"]] for o, _ in autres])[0]
        if cote not in deja:
            deja.add(cote)
            a_sortir.append((o, cote))

    indices_retard = set(random.sample(range(nb_en_cours), nb_en_cours_retard))
    for i, (ouvrage, cote) in enumerate(a_sortir):
        prolongations = 1 if random.random() < 0.2 else 0
        duree = DUREE_EMPRUNT_JOURS + prolongations * DUREE_PROLONGATION_JOURS
        while True:
            if i in indices_retard:
                # retour prévu déjà dépassé
                debut = AUJOURDHUI - timedelta(days=duree + random.randint(1, 45))
            else:
                # retour prévu aujourd'hui ou plus tard
                debut = AUJOURDHUI - timedelta(days=random.randint(0, duree))
            lecteur = choisir_lecteur(lecteurs, occupations_lec, debut, FIN_EN_COURS)
            if lecteur:
                break
        enregistrer(ouvrage, cote, lecteur, debut, prolongations, None)

    # 2. Emprunts rendus ---------------------------------------------------
    # Exactement 25 % des rendus sont en retard (1 à 20 jours)
    retards = [True] * (nb_rendus // 4) + [False] * (nb_rendus - nb_rendus // 4)
    random.shuffle(retards)
    poids_liste = [poids[o["code"]] for o in papiers]
    for en_retard in retards:
        while True:
            ouvrage = random.choices(papiers, weights=poids_liste)[0]
            cote = random.choice(ouvrage["exemplaires"])["cote"]
            prolongations = 1 if random.random() < 0.15 else 0
            duree = DUREE_EMPRUNT_JOURS + prolongations * DUREE_PROLONGATION_JOURS
            debut = date_aleatoire(AUJOURDHUI - timedelta(days=730),
                                   AUJOURDHUI - timedelta(days=15))
            prevu = debut + timedelta(days=duree)
            if en_retard:
                retour = prevu + timedelta(days=random.randint(1, 20))
            else:
                retour = debut + timedelta(days=random.randint(1, duree))
            if retour >= AUJOURDHUI:
                continue
            if not exemplaire_libre(occupations_ex, cote, debut, retour):
                continue
            lecteur = choisir_lecteur(lecteurs, occupations_lec, debut, retour)
            if lecteur:
                break
        enregistrer(ouvrage, cote, lecteur, debut, prolongations, retour)

    # 3. Codes chronologiques EMP-0001... puis insertion
    emprunts.sort(key=lambda e: e["date_emprunt"])
    for i, e in enumerate(emprunts, start=1):
        e["code_emprunt"] = f"EMP-{i:04d}"

    db.emprunts.delete_many({})
    db.emprunts.insert_many(emprunts)
    db.emprunts.create_index("code_emprunt", unique=True)

    # 4. Mise à jour de la disponibilité des exemplaires
    db.ouvrages.update_many({"type": "papier"},
                            {"$set": {"exemplaires.$[].disponible": True}})
    for e in emprunts:
        if e["date_retour_effectif"] is None:
            db.ouvrages.update_one({"exemplaires.cote": e["cote"]},
                                   {"$set": {"exemplaires.$.disponible": False}})
    print(f"{len(emprunts)} emprunts insérés ({nb_en_cours} en cours)")


# ---------------------------------------------------------------------------
# Pénalités
# ---------------------------------------------------------------------------

def generer_penalites():
    """Crée une pénalité pour chaque emprunt rendu en retard (et seulement ceux-là)."""
    rendus_en_retard = db.emprunts.find({
        "date_retour_effectif": {"$ne": None},
        "$expr": {"$gt": ["$date_retour_effectif", "$date_retour_prevu"]},
    }).sort("code_emprunt", 1)

    penalites = []
    for i, e in enumerate(rendus_en_retard, start=1):
        jours = (e["date_retour_effectif"] - e["date_retour_prevu"]).days
        penalites.append({
            "code_penalite": f"PEN-{i:04d}",
            "numero_carte": e["numero_carte"],
            "code_emprunt": e["code_emprunt"],
            "jours_retard": jours,
            "montant": jours * TARIF_RETARD_PAR_JOUR,
            "payee": random.random() < 0.6,
        })

    db.penalites.delete_many({})
    if penalites:
        db.penalites.insert_many(penalites)
    db.penalites.create_index("code_penalite", unique=True)
    print(f"{len(penalites)} pénalités insérées")


# ---------------------------------------------------------------------------
# Réservations
# ---------------------------------------------------------------------------

def generer_reservations():
    """Crée 60 réservations : 20 en attente, 25 satisfaites, 15 expirées."""
    lecteurs = list(db.lecteurs.find())
    papiers = list(db.ouvrages.find({"type": "papier"}))
    emprunts = list(db.emprunts.find())
    reservations = []

    # Titres dont aucun exemplaire n'est disponible
    titres_indisponibles = [o["code"] for o in papiers
                            if all(not ex["disponible"] for ex in o["exemplaires"])]
    # Couples (lecteur, ouvrage) ayant un emprunt en cours
    en_cours = {(e["numero_carte"], e["code_ouvrage"])
                for e in emprunts if e["date_retour_effectif"] is None}

    # 1. En attente : titre indisponible, réservation récente, carte valide
    lecteurs_valides = [l for l in lecteurs if l["date_expiration"] >= AUJOURDHUI]
    deja_reserve = set()
    while len(reservations) < 20:
        code = random.choice(titres_indisponibles)
        lecteur = random.choice(lecteurs_valides)
        couple = (lecteur["numero_carte"], code)
        if couple in en_cours or couple in deja_reserve:
            continue
        deja_reserve.add(couple)
        reservations.append({
            "numero_carte": lecteur["numero_carte"],
            "code_ouvrage": code,
            "date_reservation": AUJOURDHUI - timedelta(days=random.randint(0, 29)),
            "statut": "en attente",
        })

    # 2. Satisfaites : liées à un emprunt existant, 1 à 30 jours avant celui-ci
    inscriptions = {l["numero_carte"]: l["date_inscription"] for l in lecteurs}
    candidats = [e for e in emprunts
                 if (e["date_emprunt"] - inscriptions[e["numero_carte"]]).days >= 1]
    for e in random.sample(candidats, 25):
        ecart_max = min(30, (e["date_emprunt"] - inscriptions[e["numero_carte"]]).days)
        reservations.append({
            "numero_carte": e["numero_carte"],
            "code_ouvrage": e["code_ouvrage"],
            "date_reservation": e["date_emprunt"] - timedelta(days=random.randint(1, ecart_max)),
            "statut": "satisfaite",
        })

    # 3. Expirées : plus de 30 jours, sans emprunt ultérieur du lecteur sur le titre
    nb_expirees = 0
    while nb_expirees < 15:
        lecteur = random.choice(lecteurs)
        ouvrage = random.choice(papiers)
        date_res = AUJOURDHUI - timedelta(
            days=random.randint(DELAI_EXPIRATION_RESERVATION_JOURS + 1, 600))
        if not (lecteur["date_inscription"] <= date_res <= lecteur["date_expiration"]):
            continue
        emprunte_ensuite = any(
            e["numero_carte"] == lecteur["numero_carte"]
            and e["code_ouvrage"] == ouvrage["code"]
            and e["date_emprunt"] >= date_res
            for e in emprunts)
        if emprunte_ensuite:
            continue
        reservations.append({
            "numero_carte": lecteur["numero_carte"],
            "code_ouvrage": ouvrage["code"],
            "date_reservation": date_res,
            "statut": "expirée",
        })
        nb_expirees += 1

    # Codes chronologiques RES-0001...
    reservations.sort(key=lambda r: r["date_reservation"])
    for i, r in enumerate(reservations, start=1):
        r["code_reservation"] = f"RES-{i:04d}"

    db.reservations.delete_many({})
    db.reservations.insert_many(reservations)
    db.reservations.create_index("code_reservation", unique=True)
    print(f"{len(reservations)} réservations insérées")


# ---------------------------------------------------------------------------
# Vérification
# ---------------------------------------------------------------------------

def controle(condition, libelle, detail=""):
    """Affiche OK ou ERREUR pour un contrôle et renvoie le résultat."""
    if condition:
        print(f"  OK      {libelle}")
    else:
        print(f"  ERREUR : {libelle} {detail}")
    return condition


def verifier_coherence():
    """Affiche des statistiques et vérifie chaque contrainte du jeu de données."""
    lecteurs = {l["numero_carte"]: l for l in db.lecteurs.find()}
    ouvrages = {o["code"]: o for o in db.ouvrages.find()}
    emprunts = list(db.emprunts.find())
    penalites = list(db.penalites.find())
    reservations = list(db.reservations.find())

    papiers = [o for o in ouvrages.values() if o["type"] == "papier"]
    numeriques = [o for o in ouvrages.values() if o["type"] == "numérique"]
    total_ex = sum(len(o["exemplaires"]) for o in papiers)
    cote_vers_ouvrage = {ex["cote"]: o["code"] for o in papiers for ex in o["exemplaires"]}
    rendus = [e for e in emprunts if e["date_retour_effectif"] is not None]
    cours = [e for e in emprunts if e["date_retour_effectif"] is None]

    print("\n=== Statistiques ===")
    for nom in ["lecteurs", "ouvrages", "emprunts", "penalites", "reservations"]:
        print(f"  {nom:<13}: {db[nom].count_documents({})} documents")
    print(f"  exemplaires  : {total_ex}")
    print(f"  numériques   : {len(numeriques)}")
    print(f"  emprunts     : {len(rendus)} rendus, {len(cours)} en cours")

    print("\n=== Ouvrages ===")
    controle(len(ouvrages) == 150 and len(papiers) == 120 and len(numeriques) == 30,
             "150 ouvrages dont 120 papier et 30 numériques")
    controle(total_ex >= 400, "au moins 400 exemplaires", f"({total_ex})")
    controle(all(2 <= len(o["exemplaires"]) <= 5 for o in papiers),
             "chaque ouvrage papier a 2 à 5 exemplaires")
    controle(all("lien" not in o and "taille_mo" not in o for o in papiers),
             "aucun ouvrage papier n'a de lien ni de taille_mo")
    controle(all("exemplaires" not in o and "lien" in o and "taille_mo" in o
                 and o["format"] in ("pdf", "vidéo", "mémoire") for o in numeriques),
             "les numériques ont lien, taille_mo, format et pas d'exemplaires")
    controle(all(1 <= len(o["auteurs"]) <= 3 and 1 <= len(o["genres"]) <= 2
                 and 2 <= len(o["mots_cles"]) <= 4 and isinstance(o["annee"], int)
                 for o in ouvrages.values()),
             "auteurs (1-3), genres (1-2), mots_cles (2-4), annee entière")

    print("\n=== Emprunts ===")
    controle(len(emprunts) >= 500, "au moins 500 emprunts", f"({len(emprunts)})")
    controle(all(cote_vers_ouvrage.get(e["cote"]) == e["code_ouvrage"] for e in emprunts),
             "chaque emprunt porte sur un exemplaire d'un ouvrage papier")
    champs_dates = ["date_emprunt", "date_retour_prevu"]
    controle(all(isinstance(e[c], datetime) for e in emprunts for c in champs_dates)
             and all(isinstance(e["date_retour_effectif"], datetime) for e in rendus),
             "toutes les dates sont des datetime")
    controle(all(e["nb_prolongations"] in range(MAX_PROLONGATIONS + 1)
                 and e["date_retour_prevu"] == e["date_emprunt"] + timedelta(
                     days=DUREE_EMPRUNT_JOURS + e["nb_prolongations"] * DUREE_PROLONGATION_JOURS)
                 for e in emprunts),
             "date_retour_prevu = date_emprunt + 14 j (+ 7 j si prolongé)")
    controle(all(e["date_retour_effectif"] > e["date_emprunt"]
                 and e["date_retour_effectif"] < AUJOURDHUI for e in rendus),
             "retour effectif après l'emprunt et avant AUJOURDHUI")

    # Aucun chevauchement sur un même exemplaire, au plus un emprunt en cours
    par_cote = {}
    for e in emprunts:
        par_cote.setdefault(e["cote"], []).append(e)
    chevauchements = 0
    for liste in par_cote.values():
        liste.sort(key=lambda e: e["date_emprunt"])
        for avant, apres in zip(liste, liste[1:]):
            if avant["date_retour_effectif"] is None \
                    or apres["date_emprunt"] <= avant["date_retour_effectif"]:
                chevauchements += 1
    controle(chevauchements == 0, "aucun exemplaire avec deux emprunts simultanés",
             f"({chevauchements} chevauchements)")
    controle(all(sum(e["date_retour_effectif"] is None for e in l) <= 1
                 for l in par_cote.values()),
             "au plus un emprunt en cours par exemplaire")

    # Disponibilité cohérente avec les emprunts en cours
    cotes_sorties = {e["cote"] for e in cours}
    incoherents = [ex["cote"] for o in papiers for ex in o["exemplaires"]
                   if ex["disponible"] == (ex["cote"] in cotes_sorties)]
    controle(not incoherents, "disponible = false exactement pour les exemplaires sortis",
             f"({len(incoherents)} incohérents)")

    # Maximum d'emprunts par lecteur
    nb_cours = {}
    for e in cours:
        nb_cours[e["numero_carte"]] = nb_cours.get(e["numero_carte"], 0) + 1
    depassements = [c for c, n in nb_cours.items() if n > lecteurs[c]["max_emprunts"]]
    controle(not depassements, "aucun lecteur au-delà de max_emprunts en cours",
             f"({depassements})")
    # Même contrôle à tout instant de l'historique (balayage chronologique)
    depassements_hist = set()
    par_lecteur = {}
    for e in emprunts:
        fin = e["date_retour_effectif"] or FIN_EN_COURS
        par_lecteur.setdefault(e["numero_carte"], []).extend(
            [(e["date_emprunt"], 0, +1), (fin, 1, -1)])
    for carte, evenements in par_lecteur.items():
        simultanes = 0
        for _, _, delta in sorted(evenements):
            simultanes += delta
            if simultanes > lecteurs[carte]["max_emprunts"]:
                depassements_hist.add(carte)
    controle(not depassements_hist, "max_emprunts jamais dépassé dans l'historique",
             f"({sorted(depassements_hist)})")
    expires = [e["code_emprunt"] for e in cours
               if lecteurs[e["numero_carte"]]["date_expiration"] < AUJOURDHUI]
    controle(not expires, "aucun emprunt en cours pour une carte expirée", f"({expires})")

    # Répartition temporelle
    il_y_a_2_ans = AUJOURDHUI - timedelta(days=730)
    il_y_a_1_an = AUJOURDHUI - timedelta(days=365)
    controle(all(il_y_a_2_ans <= e["date_emprunt"] <= AUJOURDHUI for e in emprunts)
             and any(e["date_emprunt"] < il_y_a_1_an for e in emprunts),
             "dates d'emprunt étalées sur les 2 dernières années")
    part_rendus = len(rendus) / len(emprunts)
    controle(0.80 <= part_rendus <= 0.90, "environ 85 % rendus / 15 % en cours",
             f"({part_rendus:.0%})")
    rendus_retard = [e for e in rendus if e["date_retour_effectif"] > e["date_retour_prevu"]]
    part_retard = len(rendus_retard) / len(rendus)
    controle(0.20 <= part_retard <= 0.30, "environ 25 % des rendus en retard",
             f"({part_retard:.0%})")
    controle(all(1 <= (e["date_retour_effectif"] - e["date_retour_prevu"]).days <= 20
                 for e in rendus_retard), "retards des rendus entre 1 et 20 jours")
    anciens = sum(1 for e in rendus if e["date_retour_effectif"] < il_y_a_1_an)
    controle(anciens >= 100, "au moins 100 emprunts rendus depuis plus d'un an",
             f"({anciens})")
    cours_retard = [e for e in cours if e["date_retour_prevu"] < AUJOURDHUI]
    controle(len(cours_retard) >= 15, "au moins 15 emprunts en cours en retard",
             f"({len(cours_retard)})")
    print(f"          ({len(cours_retard)} en retard, "
          f"{len(cours) - len(cours_retard)} pas encore échus)")

    # Popularité inégale
    compte = {}
    for e in emprunts:
        compte[e["code_ouvrage"]] = compte.get(e["code_ouvrage"], 0) + 1
    valeurs = sorted(compte.values(), reverse=True)
    mediane = valeurs[len(valeurs) // 2]
    controle(valeurs[9] >= 2 * mediane, "popularité inégale (10e du top ≥ 2 × médiane)",
             f"(10e : {valeurs[9]}, médiane : {mediane})")
    top3 = sorted(compte.items(), key=lambda x: -x[1])[:3]
    print("          top 3 : " + ", ".join(f"{ouvrages[c]['titre']} ({n})" for c, n in top3))

    titres_complets = [o["code"] for o in papiers
                       if all(ex["cote"] in cotes_sorties for ex in o["exemplaires"])]
    controle(len(titres_complets) >= 10,
             "au moins 10 titres avec tous leurs exemplaires en cours d'emprunt",
             f"({len(titres_complets)})")

    print("\n=== Pénalités ===")
    codes_retard = {e["code_emprunt"] for e in rendus_retard}
    codes_penalites = [p["code_emprunt"] for p in penalites]
    controle(sorted(codes_penalites) == sorted(codes_retard),
             "une pénalité par emprunt rendu en retard, et seulement pour eux")
    emprunt_par_code = {e["code_emprunt"]: e for e in emprunts}
    controle(all(p["jours_retard"] == (emprunt_par_code[p["code_emprunt"]]["date_retour_effectif"]
                                       - emprunt_par_code[p["code_emprunt"]]["date_retour_prevu"]).days
                 and p["montant"] == p["jours_retard"] * TARIF_RETARD_PAR_JOUR
                 and p["numero_carte"] == emprunt_par_code[p["code_emprunt"]]["numero_carte"]
                 for p in penalites),
             "jours_retard, montant et numero_carte corrects")
    part_payees = sum(p["payee"] for p in penalites) / len(penalites)
    controle(0.50 <= part_payees <= 0.70, "environ 60 % des pénalités payées",
             f"({part_payees:.0%})")

    print("\n=== Réservations ===")
    controle(len(reservations) >= 60, "au moins 60 réservations", f"({len(reservations)})")
    controle(all(ouvrages[r["code_ouvrage"]]["type"] == "papier" for r in reservations),
             "réservations uniquement sur des ouvrages papier")
    par_statut = {}
    for r in reservations:
        par_statut.setdefault(r["statut"], []).append(r)
    print("          " + ", ".join(f"{s} : {len(l)}" for s, l in par_statut.items()))
    controle(set(par_statut) == {"en attente", "satisfaite", "expirée"},
             "statuts limités à en attente / satisfaite / expirée")

    couples_cours = {(e["numero_carte"], e["code_ouvrage"]) for e in cours}
    erreurs = [r["code_reservation"] for r in par_statut.get("en attente", [])
               if r["code_ouvrage"] not in titres_complets
               or not (AUJOURDHUI - timedelta(days=30) < r["date_reservation"] <= AUJOURDHUI)
               or (r["numero_carte"], r["code_ouvrage"]) in couples_cours]
    controle(not erreurs, "en attente : titre indisponible, < 30 jours, pas déjà emprunté",
             f"({erreurs})")

    erreurs = [r["code_reservation"] for r in par_statut.get("satisfaite", [])
               if not any(e["numero_carte"] == r["numero_carte"]
                          and e["code_ouvrage"] == r["code_ouvrage"]
                          and 1 <= (e["date_emprunt"] - r["date_reservation"]).days <= 30
                          for e in emprunts)]
    controle(not erreurs, "satisfaite : emprunt correspondant 1 à 30 jours après",
             f"({erreurs})")

    erreurs = [r["code_reservation"] for r in par_statut.get("expirée", [])
               if (AUJOURDHUI - r["date_reservation"]).days <= DELAI_EXPIRATION_RESERVATION_JOURS
               or any(e["numero_carte"] == r["numero_carte"]
                      and e["code_ouvrage"] == r["code_ouvrage"]
                      and e["date_emprunt"] >= r["date_reservation"]
                      for e in emprunts)]
    controle(not erreurs, "expirée : plus de 30 jours et aucun emprunt correspondant",
             f"({erreurs})")

    print("\n=== Index ===")
    for collection, champ in [("lecteurs", "numero_carte"), ("ouvrages", "code"),
                              ("emprunts", "code_emprunt")]:
        uniques = [i for i in db[collection].index_information().values()
                   if i.get("unique") and i["key"] == [(champ, 1)]]
        controle(bool(uniques), f"index unique sur {collection}.{champ}")


if __name__ == "__main__":
    random.seed(42)
    generer_lecteurs(120)
    generer_ouvrages()
    generer_emprunts()
    generer_penalites()
    generer_reservations()
    verifier_coherence()
