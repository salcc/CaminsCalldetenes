# Copyright (C) 2019 Utricularia gibba
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


# L'explicació detallada dels algorismes que hi ha a continuació es troben
# dins del text del treball de recerca.

import pickle
from math import inf
from queue import PriorityQueue

from utils import distancia, reconstruir_cami, reconstruir_cami_bidireccional


# - G: el graf en què es busca el camí
# - i: el vèrtex inicial del camí més curt
# - f: el vèrtex final del camí més curt
# - nom_atribut_pes: cadena de text que té el nom de l'atribut que representa
#                    el pes de cada aresta
# - heuristiques: és un booleà que
#                 si és False no s'utilitzaran heurístiques i serà Dijkstra,
#                 si és True s'utilitzaran herurístiques i serà cerca A*


def visual(G, i, f, nom_atribut_pes, heuristiques):
  distancies = [inf] * G.ordre()
  distancies[i] = 0

  predecessors = [None] * G.ordre()

  PQ = PriorityQueue()
  PQ.put((distancies[i], i))

  visualitzacio = []

  while not PQ.empty():
    u = PQ.get()[1]

    if predecessors[u] is not None:
      visualitzacio.append([[G.llegir_atributs(predecessors[u])["coords"], G.llegir_atributs(u)["coords"]], "Lime"])

    if u == f:
      return reconstruir_cami(predecessors, f), visualitzacio

    for v in G.llista_adjacencia[u]:
      g = distancies[u] + G.llegir_atributs((u, v))[nom_atribut_pes]

      if g < distancies[v]:
        predecessors[v] = u
        distancies[v] = g
        if heuristiques:
          PQ.put((distancies[v] + distancia(G.llegir_atributs(v)["coords"], G.llegir_atributs(f)["coords"]), v))
        else:
          PQ.put((distancies[v], v))

        visualitzacio.append([[G.llegir_atributs(u)["coords"], G.llegir_atributs(v)["coords"]], "ForestGreen"])

  return None, visualitzacio


def visual_bidireccional(G, i, f, nom_atribut_pes, heuristiques):
  fitxer = open("llista_incidencia.pickle", "rb")
  llista_incidencia = pickle.load(fitxer)
  fitxer.close()

  distancies_i = [inf] * G.ordre()
  distancies_i[i] = 0
  distancies_f = [inf] * G.ordre()
  distancies_f[f] = 0

  PQ_i = PriorityQueue()
  PQ_i.put((distancies_i[i], i))
  PQ_f = PriorityQueue()
  PQ_f.put((distancies_f[f], f))

  predecessors_i = [None] * G.ordre()
  predecessors_f = [None] * G.ordre()

  processats_i = []
  processats_f = []

  visualitzacio = []

  if heuristiques:
    h = [inf] * G.ordre()

    def heuristica(v):
      if h[v] == inf:
        h[v] = (distancia(G.llegir_atributs(v)["coords"],
                          G.llegir_atributs(f)["coords"]) -
                distancia(G.llegir_atributs(v)["coords"],
                          G.llegir_atributs(i)["coords"])) / 2
      return h[v]

  while not PQ_i.empty() and not PQ_f.empty():
    u = PQ_i.get()[1]
    if predecessors_i[u] is not None:
      visualitzacio.append([[G.llegir_atributs(predecessors_i[u])["coords"], G.llegir_atributs(u)["coords"]], "Lime"])
    for v in G.llista_adjacencia[u]:
      g = distancies_i[u] + G.llegir_atributs((u, v))[nom_atribut_pes]
      if g < distancies_i[v]:
        predecessors_i[v] = u
        distancies_i[v] = g
        if heuristiques:
          PQ_i.put((distancies_i[v] + heuristica(v), v))
        else:
          PQ_i.put((distancies_i[v], v))
        visualitzacio.append([[G.llegir_atributs(u)["coords"], G.llegir_atributs(v)["coords"]], "ForestGreen"])
    processats_i.append(u)
    if u in processats_f:
      processats = processats_i + processats_f
      return reconstruir_cami_bidireccional(i, distancies_i, predecessors_i,
                                            f, distancies_f, predecessors_f,
                                            processats), visualitzacio

    u = PQ_f.get()[1]
    if predecessors_f[u] is not None:
      visualitzacio.append([[G.llegir_atributs(predecessors_f[u])["coords"], G.llegir_atributs(u)["coords"]], "Red"])
    for v in llista_incidencia[u]:
      g = distancies_f[u] + G.llegir_atributs((v, u))[nom_atribut_pes]
      if g < distancies_f[v]:
        predecessors_f[v] = u
        distancies_f[v] = g
        if heuristiques:
          PQ_f.put((distancies_f[v] - heuristica(v), v))
        else:
          PQ_f.put((distancies_f[v], v))
        visualitzacio.append([[G.llegir_atributs(u)["coords"], G.llegir_atributs(v)["coords"]], "DarkRed"])
    processats_f.append(u)
    if u in processats_i:
      processats = processats_i + processats_f
      return reconstruir_cami_bidireccional(i, distancies_i, predecessors_i,
                                            f, distancies_f, predecessors_f,
                                            processats), visualitzacio

  return None, visualitzacio