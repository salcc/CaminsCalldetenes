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

import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

import urllib.request

import pickle
import xml.etree.ElementTree as xml

from utils import distancia
from graf import GrafDirigit


def descarregar_osm():
  url = "https://www.openstreetmap.org/api/0.6/map?bbox=2.2347%2C41.8981%2C2.3554%2C41.952"
  with urllib.request.urlopen(url) as response, open("convertidor/mapa.osm", 'wb') as mapa_osm:
    mapa_osm.write(response.read())


def processar_osm():
  element_tree = xml.parse("convertidor/mapa.osm").getroot()
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

  f = open("graf.pickle", "wb")
  pickle.dump(G, f)
  f.close()


print("Descarregant el mapa de Calldetenes d'OpenStreetMap...")
descarregar_osm()
print("Convertint el mapa en un graf...")
processar_osm()
print("Procés completat!")
