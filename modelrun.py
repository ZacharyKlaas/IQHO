#!/usr/bin/env python
# -*- coding: utf-8 -*-

###########################################################
# Écrit par Zachary Klaas
# Script autogénération pour les modules du modèle IQHO
# Pour utiliser avec ModelBuilder en version 10 de ArcGIS
###########################################################

import arcpy
from arcpy import env

import time

arcpy.ImportToolbox("C:\\Temp\\Benoit Bray_Script_JLC_2\\Benoit Bray_Script_JLC_2\\map_tool2.tbx")

inputFC=arcpy.GetParameterAsText(0)

arcpy.iqho4_zakmaptools(inputFC)
print"Fait 1"
try:
    arcpy.fieldcal_zakmaptools(inputFC)
except:
    time.sleep(30)
print"Fait 2"
layer1 = arcpy.MakeFeatureLayer_management(inputFC, "featurelayer1_lyr")
arcpy.Model52_zakmaptools(layer1)
print"Fait 3"
layer2 = arcpy.MakeFeatureLayer_management(inputFC, "featurelayer2_lyr")
arcpy.Model522_zakmaptools(layer2)
print"Fait 4"
arcpy.fieldcal3_zakmaptools(inputFC)
print"Fait 5"
layer3 = arcpy.MakeFeatureLayer_management(inputFC, "featurelayer3_lyr")
arcpy.Modelben2_zakmaptools(layer3)
print"Fait 6"
arcpy.Model422_zakmaptools(inputFC)
print"Fait 7"
arcpy.Model4_zakmaptools(inputFC)
print"Fait 8"
arcpy.fieldcal2_zakmaptools(inputFC)
print"Fait 9"
