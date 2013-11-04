#!/usr/bin/env python
# -*- coding: utf-8 -*-

########################################################
# Écrit par Zachary Klaas
# Formulaire pour les cartes IQHO
# Version pour l'usage avec ArcMap 10 et aprés
# Les informations vont être inserées dans la carte
########################################################

import Tkinter
from Tkinter import *

import tkFileDialog
from tkFileDialog import askopenfilename

import arcpy

def montrer():
        f.delete(ALL)

        global titre_grand
        global titre_petit
        global zone_utm
        global date_pleine
        global numero_reference
        global assignation_carte
        global numero_carte
        global declinaison_magnetique
        global annee_carte
        global variation_annuelle
        global echelle_montree
        global topo_annees
        global eco_annees
        global reseau_routier
        global echelle_divisee
        global metres_courbes

        global informations
        global changements
        global annees
        global metres
        
        titre_grand = unicode(titre.get())
        titre_petit = unicode(titre.get())
        f.create_text(50,50,font="Arial_Black",text=u"Titre:  "+titre_grand,anchor=NW)

        zone_utm = unicode(zone.get())
        f.create_text(50,80,font="Arial_Black",text=u"Zone:  "+zone_utm,anchor=NW)

        date_carte = unicode(date.get())
        annee_carte = unicode(date_carte[0:4])
        mois_carte = unicode(date_carte[5:7])
        jour_carte = unicode(date_carte[8:10])
        jour_carte2 = unicode(str(int(date_carte[8:10])))
        mois_numerique = int(date_carte[5:7])
        assignation_carte = unicode(assignation.get())
        infodate = [u"2013",u"janvier",u"f\u00e9vrier",u"mars",u"avril",u"mai",u"juin",u"juillet",u"août",u"septembre",u"octobre",u"novembre",u"d\u00e9cembre"]
        numero_reference = jour_carte+mois_carte+annee_carte
        numero_carte = u"IQHO / "+numero_reference+u"-"+assignation_carte
        date_pleine = jour_carte2+" "+infodate[mois_numerique]+" "+annee_carte
        f.create_text(50,110,font="Arial_Black",text=u"Date:  "+date_pleine,anchor=NW)
        f.create_text(50,140,font="Arial_Black",text=u"Num\u00e9ro de r\u00e9f\u00e9rence:  "+numero_reference+u"-"+assignation_carte,anchor=NW)
        f.create_text(50,170,font="Arial_Black",text=u"Num\u00e9ro de carte:  "+numero_carte,anchor=NW)

        declinaison_magnetique = unicode(degres.get())+u"°"+unicode(minutes.get())+"\'"
        f.create_text(50,200,font="Arial_Black",text=u"D\u00e9clinaison magn\u00e9tique:  "+declinaison_magnetique,anchor=NW)        

        variation_annuelle = unicode(variation.get())+"\'"        
        f.create_text(50,230,font="Arial_Black",text=u"Variation annuelle en "+annee_carte+u":  "+variation_annuelle,anchor=NW)        

        echelle_valeur = int(echelle.get(ACTIVE)[2:7])
        echelle_montree = unicode(echelle.get(ACTIVE)[0])+u" / "+unicode(echelle.get(ACTIVE)[2:4])+u" "+unicode(echelle.get(ACTIVE)[4:7])
        f.create_text(50,260,font="Arial_Black",text=u"\u00c9chelle: "+echelle_montree,anchor=NW)

        if topo_prem.get()=="": topo_annees = unicode(topo_deux.get())
        if topo_deux.get()=="": topo_annees = unicode(topo_prem.get())
        if topo_prem.get()<>"" and topo_deux.get()<>"":
                topo_annees = unicode(topo_prem.get())+"-"+unicode(topo_deux.get())
        f.create_text(50,290,font="Arial_Black",text=u"Ann\u00e9es de couverture topographique: "+topo_annees,anchor=NW)

        if eco_prem.get()=="": eco_annees = unicode(eco_deux.get())
        if eco_deux.get()=="": eco_annees = unicode(eco_prem.get())
        if eco_prem.get()<>"" and eco_deux.get()<>"":
                eco_annees = unicode(eco_prem.get())+"-"+unicode(eco_deux.get())
        f.create_text(50,320,font="Arial_Black",text=u"Ann\u00e9es de couverture \u00e9coforesti\u00e8re: "+eco_annees,anchor=NW)

        reseau_routier = unicode(reseau.get())
        f.create_text(50,350,font="Arial_Black",text=u"Mise \u00e0 jour du r\u00e9seau routier: "+reseau_routier,anchor=NW)

        echelle_divisee = unicode(str(echelle_valeur / 100))
        f.create_text(50,380,font="Arial_Black",text=u"1 centim\u00e8tre sur la carte repr\u00e9sente " +echelle_divisee+u" m\u00e8tres au sol.",anchor=NW)

        metres_courbes = unicode(courbes.get(ACTIVE))
        f.create_text(50,410,font="Arial_Black",text=u"Equidistance des courbes: "+metres_courbes,anchor=NW)

        informations = u"Projection UTM - zone "+zone_utm+u"\nSyst\u00e8me de r\u00e9f\u00e9rence : Ellipso\u00efde GRS 80\nSyst\u00e8me de r\u00e9f\u00e9rence g\u00e9od\u00e9sique :\nDatum Nord-am\u00e9ricain 1983 (NAD 1983)\n\nDate du tra\u00e7age : "+date_pleine+u" (R\u00e9f "+numero_reference+u"-"+assignation_carte+u")"
        changements = u"N'utiliser le diagramme que pour obtenir\nles valeurs num\u00e9riques\nD\u00e9clinaison moyenne approximative\nau centre de la carte en "+annee_carte+"\nVariation annuelle "+variation_annuelle+" Est"
        partie1 = u"<FNT name='Swiss 721 BT' size='8'>Cette carte int\u00e8gre de l'information g\u00e9ographique de source gouvernementale.  Pour des besoins "
        partie2 = u"de repr\u00e9sentation,\ncertaines donn\u00e9es ont subi de transformations et des adaptations qui "
        partie3 = u"ont pu modifier la donn\u00e9e originale.</FNT>\n\n<FNT name='Courier New' size='8'><BOL>Sources des donn\u00e9es utilis\u00e9es"+u"                           "+u"Ann\u00e9es</BOL>\n"
        partie4 = u"Cartes topographiques \u00e0 l'\u00e9chelle de "+echelle_montree+u"         "+topo_annees+u"\n"
        partie5 = u"Cartes \u00e9coforesti\u00e8res \u00e0 l'\u00e9chelle de "+echelle_montree+u"         "+eco_annees+u"\n\n"
        partie6 = u"<BOL><CLR red='255'>Mise \u00e0 jour du r\u00e9seau routier: "+reseau_routier+u"</CLR></BOL>"
        partie7 = u"\n\nMinist\u00e8re des Ressources naturelles "+unichr(0x00A9)+u" Gouvernement du Qu\u00e9bec</FNT>"
        annees = partie1 + partie2 + partie3 + partie4 + partie5 + partie6 + partie7
        partie8 = u"1 centim\u00e8tre sur la carte repr\u00e9sente "+echelle_divisee
        partie9 = u" m\u00e8tres au sol.\nEquidistance des courbes : "+metres_courbes
        partie10 = u"\nAltitudes en m\u00e8tres au-dessus du niveau moyen de la mer."
        metres = partie8 + partie9 + partie10

def envoyer():
        global titre_grand
        global titre_petit
        global zone_utm
        global date_pleine
        global numero_reference
        global numero_carte
        global declinaison_magnetique
        global annee_carte
        global variation_annuelle
        global echelle_montree
        global topo_annees
        global eco_annees
        global reseau_routier
        global echelle_divisee
        global metres_courbes

        global informations
        global changements
        global annees
        global metres

        fichier = askopenfilename(parent=fenetre)

        mxd = arcpy.mapping.MapDocument(fichier)

        f.delete(ALL)

        f.create_text(50,50,font="Arial_Black",text="1) "+titre_grand,anchor=NW)
        print titre_grand
        print u"-"
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "titre_grand")[0]
        elm.text = titre_grand      

        f.create_text(50,80,font="Arial_Black",text="2) "+titre_petit,anchor=NW)
        print titre_petit
        print u"-"
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "titre_petit")[0]
        elm.text = titre_petit      

        informations = u"Projection UTM - zone "+zone_utm+u"\nSyst\u00e8me de r\u00e9f\u00e9rence : Ellipso\u00efde GRS 80\nSyst\u00e8me de r\u00e9f\u00e9rence g\u00e9od\u00e9sique :\nDatum Nord-am\u00e9ricain 1983 (NAD 1983)\n \nDate du tra\u00e7age : "+date_pleine+u" (R\u00e9f "+numero_reference+u"-"+assignation_carte+u")"
        f.create_text(50,110,font="Arial_Black",text="3) "+informations,anchor=NW)
        print informations
        print u"-"
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "informations")[0]
        elm.text = informations
        elm.elementPositionY = 0.54

        f.create_text(50,260,font="Arial_Black",text="4) "+numero_carte,anchor=NW)
        print numero_carte
        print u"-"
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "numero_carte")[0]
        elm.text = numero_carte      

        f.create_text(50,290,font="Arial_Black",text="5) "+declinaison_magnetique,anchor=NW)
        print declinaison_magnetique
        print u"-"
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "declinaison_magnetique")[0]
        elm.text = declinaison_magnetique      

        changements = u"N'utiliser le diagramme que pour obtenir\nles valeurs num\u00e9riques\nD\u00e9clinaison moyenne approximative\nau centre de la carte en "+annee_carte+"\nVariation annuelle "+variation_annuelle+" Est"
        f.create_text(50,320,font="Arial_Black",text="6) "+changements,anchor=NW)
        print changements
        print u"-"
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "changements")[0]
        elm.text = changements
        elm.elementPositionY = 4.25

        partie1 = u"<FNT name='Swiss 721 BT' size='8'>Cette carte int\u00e8gre de l'information g\u00e9ographique de source gouvernementale.  Pour des besoins "
        partie2 = u"de repr\u00e9sentation,\\ncertaines donn\u00e9es ont subi de transformations et des adaptations qui "
        partie3 = u"ont pu modifier la donn\u00e9e originale.</FNT>\\n \\n<FNT name='Courier New' size='8'><BOL>Sources des donn\u00e9es utilis\u00e9es"+u"                           "+u"Ann\u00e9es</BOL>\\n"
        partie4 = u"Cartes topographiques \u00e0 l'\u00e9chelle de "+echelle_montree+u"         "+topo_annees+u"\\n"
        partie5 = u"Cartes \u00e9coforesti\u00e8res \u00e0 l'\u00e9chelle de "+echelle_montree+u"         "+eco_annees+u"</FNT>\\n \\n"
        partie6 = u"<FNT name='Swiss 721 BT' size='8'><BOL><CLR red='255'>Mise \u00e0 jour du r\u00e9seau routier: "+reseau_routier+u"</CLR></BOL>"
        partie7 = u"\\n \\nMinist\u00e8re des Ressources naturelles "+unichr(0x00A9)+u" Gouvernement du Qu\u00e9bec</FNT>"
        annees = partie1 + partie2 + partie3 + partie4 + partie5 + partie6 + partie7
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "annees")[0]
        elm.text = annees 

        partie1 = u"<FNT name='Swiss 721 BT' size='8'>Cette carte int\u00e8gre de l'information g\u00e9ographique de source gouvernementale.  Pour des besoins "
        partie2 = u"de repr\u00e9sentation,\ncertaines donn\u00e9es ont subi de transformations et des adaptations qui "
        partie3 = u"ont pu modifier la donn\u00e9e originale.</FNT>\n\n<FNT name='Courier New' size='8'><BOL>Sources des donn\u00e9es utilis\u00e9es"+u"                           "+u"Ann\u00e9es</BOL>\n"
        partie4 = u"Cartes topographiques \u00e0 l'\u00e9chelle de "+echelle_montree+u"         "+topo_annees+u"\n"
        partie5 = u"Cartes \u00e9coforesti\u00e8res \u00e0 l'\u00e9chelle de "+echelle_montree+u"         "+eco_annees+u"</FNT>\n\n"
        partie6 = u"<FNT name='Swiss 721 BT' size='8'><BOL><CLR red='255'>Mise \u00e0 jour du r\u00e9seau routier: "+reseau_routier+u"</CLR></BOL>"
        partie7 = u"\n\nMinist\u00e8re des Ressources naturelles (c) Gouvernement du Qu\u00e9bec</FNT>"
        annees = partie1 + partie2 + partie3 + partie4 + partie5 + partie6 + partie7
        
        f.create_text(50,430,font="Arial_Black",text="7) "+annees,anchor=NW)
        print annees
        print u"-"

        partie8 = u"1 centim\u00e8tre sur la carte repr\u00e9sente "+echelle_divisee
        partie9 = u" m\u00e8tres au sol.\n\nEquidistance des courbes : "+metres_courbes
        partie10 = u"\nAltitudes en m\u00e8tres au-dessus du niveau moyen de la mer."
        metres = partie8 + partie9 + partie10
        f.create_text(50,620,font="Arial_Black",text="8) "+metres,anchor=NW)
        print metres
        print u"-"
        elm = arcpy.mapping.ListLayoutElements(mxd, "TEXT_ELEMENT", "metres")[0]
        elm.text = metres
        elm.elementPositionY = 0.2503

        mxd.save()
        del mxd

def copier():
        global titre_grand
        global titre_petit
        global numero_carte
        global declinaison_magnetique

        global informations
        global changements
        global annees
        global metres

        resultats = Tkinter.Tk()
        resultats.title("Resultats")

        resultats.minsize(800,700)

        cadreresultats = Frame(resultats,width=1000,height=700)

        text = Text(cadreresultats,width=120,height=40,font=("Courier New",10))

        text.insert(INSERT,titre_grand+u"\n")
        text.insert(INSERT,u"-\n")
        text.insert(INSERT,titre_petit+u"\n")
        text.insert(INSERT,u"-\n")
        text.insert(INSERT,informations+u"\n")
        text.insert(INSERT,u"-\n")
        text.insert(INSERT,numero_carte+u"\n")
        text.insert(INSERT,u"-\n")
        text.insert(INSERT,declinaison_magnetique+u"\n")
        text.insert(INSERT,u"-\n")
        text.insert(INSERT,changements+u"\n")
        text.insert(INSERT,u"-\n")
        text.insert(INSERT,annees+u"\n")
        text.insert(INSERT,u"-\n")
        text.insert(INSERT,metres+u"\n")
        text.insert(END,u"-\n")
        text.pack()

        titre_grand = ""
        titre_petit = ""
        informations = ""
        numero_carte = ""
        declinaison_magnetique = ""
        changements = ""
        annees = ""
        metres = ""

        cadreresultats.pack()
        
        resultats.mainloop()

fenetre = Tkinter.Tk()
fenetre.title("Formulaire pour les cartes IQHO")

cadre1 = Frame(fenetre,width=800,height=700)

f = Tkinter.Canvas(cadre1,scrollregion=(0,0,1000,1000),background="light blue")

v1 = Scrollbar(cadre1,orient=VERTICAL)
v2 = Scrollbar(cadre1,orient=HORIZONTAL)

v1.pack(side=RIGHT,fill=Y)
v1.config(command=f.yview)
v2.pack(side=BOTTOM,fill=X)
v2.config(command=f.xview)
f.config(width=800,height=700)
f.config(yscrollcommand=v1.set)
f.config(xscrollcommand=v2.set)
f.pack(side=LEFT,expand=True,fill=BOTH)
cadre1.pack(side=LEFT)

etiquette1 = Label(fenetre,text=u"Quel est le titre pour la carte?",font=("Arial",8))
titre = Entry(fenetre)

etiquette1.pack()
titre.pack()

etiquette2 = Label(fenetre,text=u"Dans quelle zone UTM est la carte principalement situ\u00e9e?",font=("Arial",8))
zone = Entry(fenetre)

etiquette2.pack()
zone.pack()

etiquette3 = Label(fenetre,text=u"Quelle est la date? (Entrez la date dans le façon de cet exemple - 2013-09-29)",font=("Arial",8))
date = Entry(fenetre)

etiquette3.pack()
date.pack()

etiquette4 = Label(fenetre,text=u"Quelle est la d\u00e9clinaison magn\u00e9tique calcul\u00e9e pour cette carte?\n(Entrez degr\u00e9s dans la premi\u00e9re boite, minutes dans la deuxi\u00e8me boite.)",font=("Arial",8))
degres = Entry(fenetre)
minutes = Entry(fenetre)

etiquette4.pack()
degres.pack()
minutes.pack()

etiquette5 = Label(fenetre,text=u"Quelle est la variation annuelle calcul\u00e9e pour cette d\u00e9clinaison magn\u00e9tique en minutes?",font=("Arial",8))
variation = Entry(fenetre)

etiquette5.pack()
variation.pack()

etiquette6 = Label(fenetre,text=u"Quelle est l'\u00e9chelle de la carte?",font=("Arial",8))
echelle = Listbox(fenetre, height=4)
for item in [" ","1:10000", "1:20000", "1:50000"]:
    echelle.insert(END, item)

etiquette6.pack()
echelle.pack()

etiquette7 = Label(fenetre,text=u"Pour la couche topographique, quelles sont les ann\u00e9es de couverture?\n(Entrez la premi\u00e9re ann\u00e9e dans la premi\u00e8re boite, et la deuxi\u00e8me, s'il y a lieu, dans la deuxi\u00e8me boite.)",font=("Arial",8))
topo_prem = Entry(fenetre)
topo_deux = Entry(fenetre)

etiquette7.pack()
topo_prem.pack()
topo_deux.pack()

etiquette8 = Label(fenetre,text=u"Pour la couche \u00e9coforesti\u00e8re, quelles sont les ann\u00e9es de couverture?\n(Entrez la premi\u00e9re ann\u00e9e dans la premi\u00e8re boite, et la deuxi\u00e8me, s'il y a lieu, dans la deuxi\u00e8me boite.)",font=("Arial",8))
eco_prem = Entry(fenetre)
eco_deux = Entry(fenetre)

etiquette8.pack()
eco_prem.pack()
eco_deux.pack()

etiquette9 = Label(fenetre,text=u"Pour la couche du r\u00e9seau routier, quelle est l'ann\u00e9e de la base de donn\u00e9es utilis\u00e9e?",font=("Arial",8))
reseau = Entry(fenetre)

etiquette9.pack()
reseau.pack()

etiquette10 = Label(fenetre,text=u"Quelle est la equidistance des courbes pour cette carte?",font=("Arial",8))
courbes = Listbox(fenetre, height=8, width=40)
for item in [u" ",u"10 m\u00e8tres", u"15.24 m\u00e8tres", u"20 m\u00e8tres", u"10 m\u00e8tres ou 15.24 m\u00e8tres", u"10 m\u00e8tres ou 20 m\u00e8tres", u"15.24 m\u00e8tres ou 20 m\u00e8tres", u"10 m\u00e8tres, 15.24 m\u00e8tres ou 20 m\u00e8tres"]:
    courbes.insert(END, item)

etiquette10.pack()
courbes.pack()

etiquette11 = Label(fenetre,text=u"Quelle est le num\u00e9ro sp\u00e9cifique assign\u00e9 \u00e0 cette carte?",font=("Arial",8))
assignation = Entry(fenetre)

etiquette11.pack()
assignation.pack()

titre.focus_set()

cadre2 = Frame(fenetre)
cadre2.pack()

bouton1 = Button(cadre2, text="Montrer", width=10, command=montrer)
bouton1.pack(side=LEFT)

bouton2 = Button(cadre2, text="Envoyer", width=10, command=envoyer)
bouton2.pack(side=LEFT)

bouton3 = Button(cadre2, text="Copier", width=10, command=copier)
bouton3.pack()

fenetre.mainloop()
