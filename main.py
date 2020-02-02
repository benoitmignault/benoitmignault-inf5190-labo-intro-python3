from decimal import *

from mes_classes.article import *
from mes_classes.client import *

from introduction_python.mes_classes.client import creation_ou_maj_client

RABAIS_GROS_ACHETEUR = 0.15  # Contante pour déterminer le nouveau prix de la facture après le rabais de 15 %
NEW_LINE = "\n"  # Contante pour changer la ligne dans l'ecriture d'un fichier


# Lecture du fichier + Création des objets de type Client et Article
def lecture_fichier(liste_clients, liste_articles):
    with open("listeDesCommandes.txt") as les_lignes:
        for une_ligne in les_lignes:
            taxe_possible = ""
            if len(une_ligne.split()) == 5:
                numero_client, nom_article, quantite, prix, taxe_possible = une_ligne.split(' ')
            else:
                numero_client, nom_article, quantite, prix = une_ligne.split(' ')

            quantite = int(quantite)  # Conversion string to int
            prix = float(prix)  # Conversion string to float
            creation_ou_maj_client(numero_client, nom_article, quantite, liste_clients)
            creation_liste_articles(nom_article, prix, taxe_possible, liste_articles)
    les_lignes.close()


# Fin de la fonction lecture_fichier


def creation_facture_client(liste_clients, liste_articles):
    for un_client in liste_clients:
        fichier_client = open("factures_commandes_clients/" + un_client.numero + ".txt", "w")
        fichier_client.write("Client numéro %s" % un_client.numero + NEW_LINE)
        fichier_client.write(NEW_LINE)
        fichier_client.write(
            "".rjust(15) + "No de produit".ljust(15) + "Qte".rjust(15) + "Prix".rjust(15) + "Total (tx)".rjust(
                15) + NEW_LINE)

        nombre_article = 1
        montant_facture_total = 0.0
        nombre_total_articles = 0
        for cle, valeur in un_client.liste_article_client.items():  # la liste des articles du client X dans la commande
            nombre_total_articles += valeur
            liste_prix = recherche_article_pour_prix(cle, valeur,
                                                     liste_articles)  # liste_prix va contenir en premier le prix unitaire et ensuite le prix calcul en fonction de la quantite et des taxes si applicables
            prix_unitaire = liste_prix[0]
            prix_quantite_avec_taxe = liste_prix[1]
            montant_facture_total += prix_quantite_avec_taxe
            enumeration_produit = "Produit #" + str(nombre_article)
            fichier_client.write(
                enumeration_produit.ljust(15) + cle.ljust(15) + "{:15d}".format(valeur) + "{:15f}".format(
                    Decimal(prix_unitaire).quantize(Decimal('.01'))) + "{:15f}".format(
                    Decimal(prix_quantite_avec_taxe).quantize(Decimal('.01'))) + NEW_LINE)
            nombre_article += 1
        # Fin du For pour lister les articles
        # A partir d'ici, on va fermer la facture avec le rabais ou non
        fichier_client.write(NEW_LINE)
        if nombre_total_articles >= 100:
            fichier_client.write("Total avant rabais :".ljust(20) + "{:10f}".format(
                Decimal(montant_facture_total).quantize(Decimal('.01'))) + NEW_LINE)
            montant_rabais = montant_facture_total * RABAIS_GROS_ACHETEUR
            fichier_client.write(
                "Rabais : ".ljust(20) + "{:10f}".format(Decimal(montant_rabais).quantize(Decimal('.01'))) + NEW_LINE)
            fichier_client.write("Total : ".ljust(20) + "{:10f}".format(
                Decimal(montant_facture_total - montant_rabais).quantize(Decimal('.01'))) + NEW_LINE)
            fichier_client.write(NEW_LINE)
        else:
            fichier_client.write("Aucun rabais est applicable sur cette commande !" + NEW_LINE)
            fichier_client.write(
                "Total : " + format(Decimal(montant_facture_total).quantize(Decimal('.01'))) + NEW_LINE)

        fichier_client.close()
    # Fin du For pour lister les clients


# Fin de la fonction preparation_facture_clientselon


def main():
    liste_clients = []  # création d'une liste vide
    liste_articles = []  # création d'une liste vide
    lecture_fichier(liste_clients, liste_articles)  # On commence par lire le fichier de commande
    creation_facture_client(liste_clients, liste_articles)


# Fin de la fonction main


main()  # Fonction principale du programme
