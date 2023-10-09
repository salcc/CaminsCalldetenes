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


# L'explicació detallada dels algorismes que hi ha a continuació es troba
# dins del text del treball de recerca.

import pickle
from math import inf
from queue import PriorityQueue, Queue

from utils import distancia, reconstruir_cami, reconstruir_cami_bidireccional


def cerca_en_amplada(G, i, f):
  distancies = [inf] * G.ordre()
  distancies[i] = 0

  predecessors = [None] * G.ordre()

  Q = Queue()
  Q.put(i)

  while not Q.empty():
    u = Q.get()

    if u == f:
      return reconstruir_cami(predecessors, i)

    for v in G.llista_adjacencia[u]:
      if distancies[v] == inf:
        predecessors[v] = u
        distancies[v] = distancies[u] + 1
        Q.put(v)

  return None


def dijkstra(G, i, f, nom_atribut_pes):
  distancies = [inf] * G.ordre()
  distancies[i] = 0

  predecessors = [None] * G.ordre()

  PQ = PriorityQueue()
  PQ.put((distancies[i], i))

  while not PQ.empty():
    u = PQ.get()[1]

    if u == f:
      return reconstruir_cami(predecessors, f)

    for v in G.llista_adjacencia[u]:
      g = distancies[u] + G.llegir_atributs((u, v))[nom_atribut_pes]

      if g < distancies[v]:
        predecessors[v] = u
        distancies[v] = g
        PQ.put((distancies[v], v))

  return None


def a_star(G, i, f, nom_atribut_pes):
  distancies = [inf] * G.ordre()
  distancies[i] = 0

  predecessors = [None] * G.ordre()

  PQ = PriorityQueue()
  PQ.put((distancies[i], i))

  while not PQ.empty():
    u = PQ.get()[1]

    if u == f:
      return reconstruir_cami(predecessors, f)

    for v in G.llista_adjacencia[u]:
      g = distancies[u] + G.llegir_atributs((u, v))[nom_atribut_pes]

      if g < distancies[v]:
        predecessors[v] = u
        distancies[v] = g
        PQ.put((distancies[v] + distancia(G.llegir_atributs(v)["coords"], G.llegir_atributs(f)["coords"]), v))

  return None


def dijkstra_bidireccional(G, i, f, nom_atribut_pes):
  with open("static/llista_incidencia.pickle", "rb") as fitxer_llista_incidencia:
    llista_incidencia = pickle.load(fitxer_llista_incidencia)

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

  while not PQ_i.empty() and not PQ_f.empty():
    u = PQ_i.get()[1]
    for v in G.llista_adjacencia[u]:
      g = distancies_i[u] + G.llegir_atributs((u, v))[nom_atribut_pes]
      if g < distancies_i[v]:
        predecessors_i[v] = u
        distancies_i[v] = g
        PQ_i.put((distancies_i[v], v))
    processats_i.append(u)
    if u in processats_f:
      processats = processats_i + processats_f
      return reconstruir_cami_bidireccional(i, distancies_i, predecessors_i,
                                            f, distancies_f, predecessors_f,
                                            processats)

    u = PQ_f.get()[1]
    for v in llista_incidencia[u]:
      g = distancies_f[u] + G.llegir_atributs((v, u))[nom_atribut_pes]
      if g < distancies_f[v]:
        predecessors_f[v] = u
        distancies_f[v] = g
        PQ_f.put((distancies_f[v], v))
    processats_f.append(u)
    if u in processats_i:
      processats = processats_i + processats_f
      return reconstruir_cami_bidireccional(i, distancies_i, predecessors_i,
                                            f, distancies_f, predecessors_f,
                                            processats)

  return None


def a_star_bidireccional(G, i, f, nom_atribut_pes):
  with open("static/llista_incidencia.pickle", "rb") as fitxer_llista_incidencia:
    llista_incidencia = pickle.load(fitxer_llista_incidencia)

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
    for v in G.llista_adjacencia[u]:
      g = distancies_i[u] + G.llegir_atributs((u, v))[nom_atribut_pes]
      if g < distancies_i[v]:
        predecessors_i[v] = u
        distancies_i[v] = g
        PQ_i.put((distancies_i[v] + heuristica(v), v))
    processats_i.append(u)
    if u in processats_f:
      processats = processats_i + processats_f
      return reconstruir_cami_bidireccional(i, distancies_i, predecessors_i,
                                            f, distancies_f, predecessors_f,
                                            processats)

    u = PQ_f.get()[1]
    for v in llista_incidencia[u]:
      g = distancies_f[u] + G.llegir_atributs((v, u))[nom_atribut_pes]
      if g < distancies_f[v]:
        predecessors_f[v] = u
        distancies_f[v] = g
        PQ_f.put((distancies_f[v] - heuristica(v), v))
    processats_f.append(u)
    if u in processats_i:
      processats = processats_i + processats_f
      return reconstruir_cami_bidireccional(i, distancies_i, predecessors_i,
                                            f, distancies_f, predecessors_f,
                                            processats)

  return None
