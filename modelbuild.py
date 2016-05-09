#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Code à exécuter pour activer le processus "modelbuilder" pour tous les fichiers denommés IQH_Temp.shp
##     dans les dossiers différents.  Ce code est écrit en Python 3 pour ArcPRO.

import arcpy
# On commence par l'importation du progiciel ArcPy.

pathname = "C:\\Pro\\Toponav\\IQH_Zak\\"
# C'est le chemin qui contient les fichiers denommés IQH_Temp.shp.

folderlist = ["11MSE", "11NNO", "11NSO"]
# Dans la liste entre les crochets, il faut incluer tous les dossiers qui contient un fichier IQH_Temp.shp
#     trouvé au chemin identifié antérieurement dans "pathname".

file = "\\IQH_Temp.shp"
# Le fichier qu'on cherche dans tous les dossiers est IQH_Temp.shp.

arcpy.ImportToolbox("C:/Temp/Nouveau outil/IQH_FINAL_PRO.tbx")
# C'est le boîte des outils pour notre compilation des scripts.

def doStuff(inputFC):
        print (inputFC)
        arcpy.iqho4232272222_zaktomodel(inputFC)
# Cette fonction va faire exécuter la compilation des scripts dans le modèle "modelbuilder".  Quand cette
#     fonction est instantiée, les scripts vont être exécutés pour un nouveau fichier.

count = 0

for folder in folderlist:
    try:
        currentfile = pathname + folderlist[count] + file
        doStuff(currentfile)
        count = count + 1
    except arcpy.ExecuteError:
        print (arcpy.GetMessages(2))
# Pour chacun des dossiers qui contient un fichier IQH_Temp.shp, les scripts vont être exécutés selon les
#     informations dans la list des dossiers entre les crochets dans "folderlist".#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Code à exécuter pour activer le processus "modelbuilder" pour tous les fichiers denommés IQH_Temp.shp
##     dans les dossiers différents.  Ce code est écrit en Python 3 pour ArcPRO.

import arcpy
# On commence par l'importation du progiciel ArcPy.

pathname = "C:\\Pro\\Toponav\\IQH_Zak\\"
# C'est le chemin qui contient les fichiers denommés IQH_Temp.shp.

folderlist = ["11MSE", "11NNO", "11NSO"]
# Dans la liste entre les crochets, il faut incluer tous les dossiers qui contient un fichier IQH_Temp.shp
#     trouvé au chemin identifié antérieurement dans "pathname".

file = "\\IQH_Temp.shp"
# Le fichier qu'on cherche dans tous les dossiers est IQH_Temp.shp.

arcpy.ImportToolbox("C:/Temp/Nouveau outil/IQH_FINAL_PRO.tbx")
# C'est le boîte des outils pour notre compilation des scripts.

def doStuff(inputFC):
        print (inputFC)
        arcpy.iqho4232272222_zaktomodel(inputFC)
# Cette fonction va faire exécuter la compilation des scripts dans le modèle "modelbuilder".  Quand cette
#     fonction est instantiée, les scripts vont être exécutés pour un nouveau fichier.

count = 0

for folder in folderlist:
    try:
        currentfile = pathname + folderlist[count] + file
        doStuff(currentfile)
        count = count + 1
    except arcpy.ExecuteError:
        print (arcpy.GetMessages(2))
# Pour chacun des dossiers qui contient un fichier IQH_Temp.shp, les scripts vont être exécutés selon les
#     informations dans la list des dossiers entre les crochets dans "folderlist".
