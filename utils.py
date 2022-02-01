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

from math import sqrt, radians, sin, cos, asin, inf


def distancia(coords1, coords2):
  '''Calcula la distància entre dues coordenades terrestres expressades en graus
  utilitzant la fórmula del semiversiuns.'''
  lat1, lon1 = coords1
  lat2, lon2 = coords2
  lat1, lon1, lat2, lon2 = radians(lat1), radians(lon1), radians(lat2), radians(lon2)
  return (2 * 6371008.8 * asin(sqrt(
    sin((lat2 - lat1) / 2) ** 2 + cos(lat1) * cos(lat2) *
    sin((lon2 - lon1) / 2) ** 2)))


def vertex_mes_proper(G, coordenades):
  '''Troba el vèrtex més proper a unes coordenades terrestres. Perquè funcioni el
  graf ha de tenir en tots els seus vèrtexs un atribut "coords" que indiqui
  les coordenades del vèrtex.'''
  # La funció va trobant la distància entre cada vèrtex del graf i les
  # coordenades donades i retorna el vèrtex tal que la seva distància és menor que
  # la de tots els altres.
  distancia_minima = inf
  mes_proper = None
  for v in G.vertexs():
    d = distancia(coordenades, G.llegir_atributs(v)["coords"])
    if d < distancia_minima:
      distancia_minima = d
      mes_proper = v
  return mes_proper

def reconstruir_cami(predecessors, f):
  '''Aconsegueix el camí més curt a partir de la llista de predecessors que els
  algorismes produeixen.
  '''
  # Per fer-ho, fem una llista buida i afegim al principi el vèrtex al qual volem
  # arribar. Aquest vèrtex serà el final del camí i, per això, l'anomenarem f. Després,
  # afegim al principi de la llista el predecessor de f, a continuació el predecessor
  # del predecessor de f...
  # Anem fent així fins que el predecessor sigui nul, cosa que voldrà dir que hem
  # arribat al vèrtex inicial, que recordem que sempre té com a predecessor un
  # valor nul.
  cami = []
  while f is not None:
    cami.insert(0, f)
    f = predecessors[f]
  return cami



def reconstruir_cami_bidireccional(i, distancies_i, predecessors_i,
                                   f, distancies_f, predecessors_f,
                                   processats):
  '''Aconsegueix el camí més curt a partir de la informació que les dues cerques
  dels algorismes bidireccionals produeixen.
  '''
  # Per fer-ho, primer es troba quin vèrtex hem d'utilitzar per unir les dues cerques 
  # per minimitzar la distància. A aquest vèrtex l'anomenem c. Un cop trobat c,
  # s'utilitzen les llistes de predecessors de cada cerca per reconstruir el camí.
  # Per reconstruir el camí que ha trobat la cerca que comença des de i, inserirem al
  # principi c, llavors el predecessor de c, després el predecessor del predecessor
  # de c i així fins a arribar al vèrtex inicial. Llavors farem el mateix per trobar
  # el camí des de c fins a f, tot i que haurem d'inserir els elements en ordre invers
  # (al final de la llista en comptes del principi) perquè aquesta cerca anava endarrere.
  distancia_total = inf
  millor = None
  for u in processats:
    if distancies_i[u] + distancies_f[u] < distancia_total:
      millor = u
      distancia_total = distancies_i[u] + distancies_f[u]

  cami = []
  c = millor
  while c is not None:
    cami.insert(0, c)
    c = predecessors_i[c]

  c = millor
  while c != f:
    c = predecessors_f[c]
    cami.append(c)

  return cami
