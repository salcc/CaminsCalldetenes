# Copyright (C) 2019 Marçal Comajoan Cara
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import pickle
import urllib.request
import xml.etree.ElementTree as xml

from graf import GrafDirigit
from utils import distancia


# Es descarrega el fitxer OSM XML amb les dades del mapa de Calldetenes
# i els seus voltants (entre les coordenades 2.2347, 41.8981 i 2.3554, 41.952)
def descarregar_osm():
  url = "https://www.openstreetmap.org/api/0.6/map?bbox=2.2347%2C41.8981%2C2.3554%2C41.952"
  with urllib.request.urlopen(url) as response, open("mapa.osm", 'wb') as mapa_osm:
    mapa_osm.write(response.read())


# Es processa el fitxer OSM XML per crear un graf amb la classe definida a
# graf.py. L'explicació detallada d'aquesta funció es dins del text del treball
# de recerca.
# Un cop s'ha obtingut el graf, es guarda en pickle (un format per guardar
# objectes de Python) per no haver-lo de processar cada cop.
def processar_osm():
  element_tree = xml.parse("mapa.osm").getroot()
  dicc_vertexs = {}
  vies = []

  tipus_via = ["motorway", "motorway_link", "trunk", "trunk_link", "primary",
               "primary_link", "secondary", "secondary_link", "tertiary",
               "tertiary_link", "unclassified", "residential", "service",
               "living_street", "track"]
  for i in element_tree:
    if i.tag == "node":
      dicc_vertexs[int(i.attrib["id"])] = [
        float(i.attrib["lat"]), float(i.attrib["lon"])]
    elif i.tag == "way":
      via = []
      unidireccional = False
      insertar = False
      for j in i:
        if j.tag == "nd":
          via.append(int(j.attrib["ref"]))
        elif j.tag == "tag":
          if (j.attrib["k"] == "oneway" and j.attrib["v"] == "yes") or (
              j.attrib["k"] == "junction" and (
              j.attrib["v"] in ["roundabout", "circular"])):
            unidireccional = True
          elif j.attrib["k"] == "highway" and j.attrib["v"] in tipus_via:
            insertar = True

      if insertar:
        vies.append(via)
        if not unidireccional:
          vies.append(list(reversed(via)))

  G = GrafDirigit()

  for id, coordenades in dicc_vertexs.items():
    for via in vies:
      if id in via:
        dicc_vertexs[id] = G.ordre()
        G.afegir_vertex(coords=coordenades)
        break

  for via in vies:
    for i, id in enumerate(via):
      via[i] = dicc_vertexs[id]
    for i in range(len(via) - 1):
      G.afegir_aresta((via[i], via[i + 1]))

  for e in G.arestes():
    G.assignar_atributs(e, llargada=distancia(
      G.llegir_atributs(e[0])["coords"],
      G.llegir_atributs(e[1])["coords"]))

  fitxer = open("graf.pickle", "wb")
  pickle.dump(G, fitxer)
  fitxer.close()


# A partir de la llista d'adjacència del graf es genera la llista d'adjacència
# del graf, que serà utilitzada pels algorismes de cerca bidireccional.
def generar_llista_incidencia():
  fitxer = open("graf.pickle", "rb")
  G = pickle.load(fitxer)
  fitxer.close()
  llista_incidencia = []
  for u in G.vertexs():
    llista_incidencia.append([])
  for u in G.vertexs():
    for v in G.llista_adjacencia[u]:
      llista_incidencia[v].append(u)
  fitxer = open("llista_incidencia.pickle", "wb")
  pickle.dump(llista_incidencia, fitxer)
  fitxer.close()


print("Descarregant el mapa de Calldetenes d'OpenStreetMap...")
descarregar_osm()
print("Convertint el mapa en un graf...")
processar_osm()
print("Generant la llista d'incidència del graf pels algorismes de cerca "
      "bidireccional...")
generar_llista_incidencia()
print("Procés completat!")
