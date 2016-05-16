#!/usr/bin/env python
# -*- coding: utf-8 -*-

##################################################################
# Écrit par Zachary Klaas
# Implementation ArcPy de l'analyse Jenks Natural Breaks
# En utilisant les utiles PySAL (Python Spatial Analysis Library)
# Version pour l'usage avec ArcMap 10.3 et après
##################################################################

import scipy, pandas, pysal
import arcpy
import numpy as np
import pandas as pd
from numpy import array
from pandas import DataFrame
print "Importation des progiciels nécessaires..."
#Le progiciel ArcPy est le progiciel qui met en oeuvre les fonctions ArcGIS dans
#  le langage informatique de Python.  Le logithèque libre PySAL fournit les fonctions
#  d'analyse géographique.  C'est ce logithèque-ci qu'on utilise pour exécuter
#  l'analyse "natural breaks" (catégories naturelles) de George Jenks.  PySAL n'est pas 
#  inclus avec ArcGIS 10.3; il faut l'installer avant de exécuter ce script.
#Les progiciels numpy (fonctions numériques et mathématiques), scipy (fonctions
#  d'analyse scientifique) et pandas (fonctions d'analyse des données) élargissent
#  les pouvoirs de Python.  Ils sont inclus avec le logiciel ArcGIS 10.3 et après.
#  Avant de cette version, il faudrait les installer.
#Les progiciels numpy et pandas sont instanciés comme "np" et "pd" parce qu'on
#  a besoin des elements du tableau numérique de numpy (Numpy Array) et cadre de
#  données de pandas(Pandas DataFrame).

print "Importation des fonctions PySAL..."
from pysal.esda.mapclassify import Natural_Breaks as nb
#La fonction Jenks est partie du progiciel pysal.esda.mapclassify.Natural_Breaks.
#   Pour simplifier, on va instancier ça comme "nb" a partir de maintenant dans
#   le script.

print "Conversion IQHO en version de tableau numérique Numpy (Numpy Array)..."
fc = arcpy.GetParameterAsText(0)
field = "IQH_FINAL"
myArray = arcpy.da.FeatureClassToNumPyArray(fc, field)
myArray.dtype = np.float32
cursor = arcpy.da.UpdateCursor(fc,field)
thecount = 0
for row in cursor:
	if row[0] < 0:
		myArray[thecount] = None
		print thecount
		thecount += 1
	else:
		myArray[thecount] = row[0]
		thecount += 1
try:
	myDataFrame = pd.DataFrame({"TheData": myArray})
	#La fonction "GetParameterAsText" invite l'utilisateur de nommer le fichier géographique
	#  ("feature class" ou "fc") sur lequel les opérations vont commencer.
	#Ce script utilise "IQH_FINAL" comme le champ des données sur lequel les opérations vont
	#   commencer ("field").
	#La calculation utilise les progiciels arcpy.da (analyse des données) et numpy.
	#Nonobstant que le tableau numérique consiste en nombres entiers, le tableau est
	#   transformé au format de point flottant ("float") parce que le progiciel PySAL
	#   a besoin de cette transformation pour l'intégrer avec la fonction KMEANS.
	#L'iteration "for-if-else" trie les valeurs "null" des vraies données, et après cette
	#   sortation, les données sont transferées en format de cadre des données pandas.

	print "Calcul des Jenks natural breaks..."
	breaks = nb(myDataFrame["TheData"].dropna().values,k=4,initial=20)
	#Le calcul des valeurs Jenks est produit par le progiciel pysal.  Tous les valeurs
	#   "null" sont sortis, et les données qui restent sont préparées pour l'analyse.
	#La paramètre k symbolise le nombre des classes la fonction Jenks va créer pour
	#   l'utilisateur.
	#La paramètre initial est le semence de la fonction Jenks.  Un valeur grand va
	#   converger la fonction plus vite; un valeur petit, d'autre part, va être plus exact. 

	print "Vérification s'il y avait calculs précédents des champs de valeurs Jenks..."
	try:
		arcpy.DeleteField_management(fc, "Jenks")
		print "Calculs précédents des champs de valeurs Jenks effacés..."

	except Exception as e:
		print "Aucuns champs des valeurs Jenks trouvés..."
	#Cette iteration "try-except" efface les calculs précédents s'ils existent. Si un champ
	#   des résultats "Jenks" existe, le partie "try" va l'effacer.  Si un tel champ n'existe
	#   pas, le partie "except" annonce que c'est le cas.

	print "Exportation des resultats au fichier géographique (shapefile)..."
	arcpy.AddField_management(fc,"index","long")
	arcpy.AddField_management(fc,"Jenks","long")
	myData = pd.DataFrame({"Jenks": breaks.yb}, index=myDataFrame["TheData"].dropna().index)
	joinData = myDataFrame.join(myData)
	joinData["Jenks"].fillna(0, inplace=True)
	joinData.drop("TheData",1,inplace=True)
	myReturnArray = joinData.to_records()
	arcpy.da.ExtendTable(fc, "FID", myReturnArray, "index", False)
	arcpy.DeleteField_management(fc, "index")
	arcpy.DeleteField_management(fc,"TheData")
	#Un champ intitulé "index" est temporairement ajouté au tableau du fichier géographique,
	#   et aussi un champ plus permanent intitulé "Jenks", en utilisant les fonctions arcpy.
	#Un cadre de données pandas est créé, et les resultats de l'analyse sont dirigés version
	#   le cadre.  Tous les valeurs "null" qu'on a trouvé avant sont donc identifiés comme
	#   parti du premier catégorie (le catégorie 0, parce que les catégories rangent entre
	#   0-3).
	#En utilisant la fonction to_records() de pandas, les données sont inscrites dans un
	#   tableau, est les valeurs de ce tableau sont après transferés dans les champs "index"
	#   et "Jenks".
	
except Exception as e:
	print "Les données ne sont pas suffisantes pour catégorisation par l'analyse Jenks."
	print "Le fichier n'est pas être produit."
	#Le code est dans un loop "try-except" parce qu'il faut assurer qu'il sera un
	#   nombre des données suffisant pour génerer un analyse Jenks.  Si ce n'est pas
	#   possible, le code va completer sans erreur en tout cas.
