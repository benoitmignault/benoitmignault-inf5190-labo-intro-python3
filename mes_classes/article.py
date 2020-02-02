TAXE_FED = 0.05  # Constante pour la taxe fédérale canadienne
TAXE_PROV = 0.09975  # Constante pour la taxe provinciale du Québec


class Article(object):
    def __init__(self, nom_article, prix_avant_tx, existante_taxe_fed, existante_taxe_prov):
        self.nom_article = nom_article  # type VARCHAR
        self.prix_avant_tx = prix_avant_tx  # type FLOAT
        self.existante_taxe_fed = existante_taxe_fed  # type BOOLEAN
        self.existante_taxe_prov = existante_taxe_prov  # type BOOLEAN


# Fin de la classe Article

def creation_liste_articles(nom_article, prix, taxe_possible, liste_articles):
    for un_article in liste_articles:
        if un_article.nom_article == nom_article:
            return  # Alors l'article existe déjà donc on peut sortir de la def
    # On doit vérifier sur quelles taxes l'article sera taxé
    indicateur_tax_fed = False
    indicateur_tax_prov = False
    taxe_possible = taxe_possible.rstrip('\n')  # On retire le charactere de retour de ligne pour un meilleur resultat

    if taxe_possible == "FP":
        indicateur_tax_fed = True
        indicateur_tax_prov = True
    elif taxe_possible == "F":
        indicateur_tax_fed = True
    elif taxe_possible == "P":
        indicateur_tax_prov = True

    nouvel_article = Article(nom_article, prix, indicateur_tax_fed, indicateur_tax_prov)
    liste_articles.append(nouvel_article)


# Fin de la fonction creation_liste_articles

def recherche_article_pour_prix(nom_article, quantite, liste_articles):
    liste_prix = []
    for un_article in liste_articles:
        if un_article.nom_article == nom_article:  # Nous avons alors trouvé l'article donc on va calculer combien ça coute...
            liste_prix.append(un_article.prix_avant_tx)
            prix_quantite = un_article.prix_avant_tx * quantite
            montant_taxe_fed = 0.0
            montant_taxe_prov = 0.0
            if un_article.existante_taxe_fed:
                montant_taxe_fed = prix_quantite * TAXE_FED
            if un_article.existante_taxe_prov:
                montant_taxe_prov = prix_quantite * TAXE_PROV
            prix_quantite_taxe = prix_quantite + montant_taxe_fed + montant_taxe_prov
            liste_prix.append(prix_quantite_taxe)
            return liste_prix
        # Si on avait trouvé l'article, on a donc calculer le prix en fonction de la quantité et des taxes
# Fin de la fonction recherche_article_pour_prix
