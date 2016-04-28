#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################################
# Écrit par Zachary Klaas
# Implementation ArcPy de la division des fichiers selon nom de tuiles
# Version pour l'usage avec ArcMap 10.3 et après
######################################################################

print "Importation des progiciels nécessaires..."
import arcpy
import numpy as np
#Ce script utilise seulement les fonctions de ArcPy (ArcGIS) et de Numpy
#   (fonctions numériques).

print "Création des fonctions..."
def unique_values(table, field):
	data = arcpy.da.TableToNumPyArray(table, [field])
	return np.unique(data[field])
#Cette fonction renvoie les valeurs uniques dans une série. Quand la fonction
#   est instanciée, seulement les lignes dans la tableau qui correspond à un
#   valeur spécifique vont être renvoyées.

print "Création de la liste des tuiles..."
fc = arcpy.GetParameterAsText(0)
tilefield = "FCA_NO_FEU"
valuesarray = unique_values(fc, tilefield)
#Ici on met en oeuvre la fonction.  L'utilisateur fournit le nom du fichier
#   géographique, et le champ qui identifie les tuiles, FCA_NO_FEU, est
#   également fourni.  Avec ces informations, la fonction est met en oeuvre.

print "En faisant les fichiers pour chaque tuile..."
tilecount = valuesarray.size - 1
arcpy.env.overwriteOutput = True
for tile in range(1,tilecount):
	whereclause = str("\"FCA_NO_FEU\" = '" + valuesarray[tile] + "'")
	print whereclause
	arcpy.MakeFeatureLayer_management(fc, "result", whereclause)
	newname = "Jenks Temp " + str(tile) + ".dbf"
	arcpy.CopyFeatures_management("result",newname)
print "Tuiles finis..."
#Pour chaque tuile, l'iteration "for" va donc créer un nouveau fichier géographique.
