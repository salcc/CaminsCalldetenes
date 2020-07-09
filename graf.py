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


class GrafDirigit:

  # Mètode que s'executa quan es crea una nova instància de la classe.
  def __init__(self):
    # S'inicialitza el graf amb una llista d'adjacència buida,
    # ja que al principi encara no té cap vèrtex.
    self.llista_adjacencia = []

    # El diccionari __atributs és una variable privada de la
    # classe que guarda els atributs de les arestes i els vèrtexs.
    self.__atributs = {}

  # Mètode per afegir un vèrtex al graf.
  # El paràmetre 'atributs' és opcional i serveix per assignar atributs
  # al vèrtex que s'està afegint.
  def afegir_vertex(self, **atributs):

    # Assigna els atributs indicats en el paràmetre 'atributs'
    # al diccionari d'atributs del vèrtex que s'està afegint.
    self.__atributs[self.ordre()] = atributs

    # Afegeix una llista buida a la llista d'adjacència, que
    # representarà el vèrtex afegit. Incialment està buida,
    # però es pot omplir si afegim una aresta que connecti
    # des del vèrtex afegit a un altre.
    self.llista_adjacencia.append([])

  # Mètode que retorna una llista de tots els vèrtexs del graf.
  def vertexs(self):
    return list(range(self.ordre()))

  # Mètode per afegir una aresta al graf.
  # El paràmetre 'aresta' és obligatori i serveix per indicar quins dos
  # vèrtexs connecta l'aresta. Per exemple pot ser (0, 1), per indicar que
  # l'aresta que s'està afegint va del vèrtex 0 al vèrtex 1.
  # El paràmetre 'atributs' és opcional i serveix per assignar atributs
  # a l'aresta que s'està afegint.
  def afegir_aresta(self, aresta, **atributs):
    # Separa el paràmetre 'aresta' en les variables 'vertex1' i 'vertex2',
    # els dos vèrtexs que l'aresta connecta.
    vertex1, vertex2 = aresta

    # Llança un error en cas de que l'aresta connecti dos vèrtexs
    # que no estàn presents en el graf.
    if vertex1 >= self.ordre() or vertex2 >= self.ordre():
      raise IndexError

    # Afageix 'vertex2' a la llista d'adjacència de 'vertex1',
    # indicant així que 'vertex1' incideix a 'vertex2'.
    self.llista_adjacencia[vertex1].append(vertex2)
    self.__atributs[aresta] = atributs

  # Mètode que retorna una llista de totes les arestes del graf.
  def arestes(self):
    llista_arestes = []
    for vertex1 in self.vertexs():
      for vertex2 in self.llista_adjacencia[vertex1]:
        llista_arestes.append((vertex1, vertex2))
    return llista_arestes

  # Mètode que retorna l'ordre (el nombre de vèrtexs) del graf.
  def ordre(self):
    return len(self.llista_adjacencia)

  # Mètode que retorna la mida (el nombre d'arestes) del graf.
  def mida(self):
    mida = 0
    for vertex in self.llista_adjacencia:
      mida += len(vertex)
    return mida

  # Mètode que retorna el diccionari d'atributs del vèrtex o aresta
  # indicat en el paràmetre obligatori 'vertex_o_aresta'.
  def llegir_atributs(self, vertex_o_aresta):
    return self.__atributs[vertex_o_aresta]

  # Mètode per assignar atributs al diccionari d'atributs del vèrtex
  # o aresta indicat en el paràmetre obligatori 'vertex_o_aresta'.
  def assignar_atributs(self, vertex_o_aresta, **atributs):
    for nom_atribut, valor in atributs.items():
      self.__atributs[vertex_o_aresta][nom_atribut] = valor

  def __str__(self):
    s = "[\n"
    for v in self.vertexs():
      s += "\t" + str(v) + ": [\n\t\t[\n"
      for u in self.llista_adjacencia[v]:
        s += "\t\t\t" + str(u) + " " + str(self.llegir_atributs((v, u))) + "\n"
      s += "\t\t] " + str(self.llegir_atributs(v)) + "\n\t]\n"
    s += "]"
    return s
