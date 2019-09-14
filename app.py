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

import json
import pickle

from flask import Flask, render_template, request

from cami_mes_curt import dijkstra, a_star
from cami_mes_curt_visual import dijkstra_visual, a_star_visual
from utils import vertex_mes_proper

app = Flask(__name__)

graf = None


@app.before_first_request
def carregar_graf():
  global graf
  f = open("graf.pickle", "rb")
  graf = pickle.load(f)
  f.close()


@app.route("/", methods=["GET", "POST"])
def index():
  user_agent = request.user_agent.string
  if "MSIE" in user_agent or "Trident" in user_agent or "Edge" in user_agent:
    return render_template("error/navegador_no_suportat.html")
  if request.method == "POST":
    origen = vertex_mes_proper(graf, eval(request.form["coordenades_origen"]))
    destinacio = vertex_mes_proper(graf, eval(request.form["coordenades_destinacio"]))
    algorisme = eval(request.form["algorisme"])
    if algorisme == a_star:
      cami = algorisme(graf, origen, destinacio, "llargada")
      cami = [graf.llegir_atributs(vertex)["coordenades"] for vertex in cami]
      return json.dumps(cami)
    else:
      cami, visualitzacio = algorisme(graf, origen, destinacio, "llargada")
      cami = [graf.llegir_atributs(vertex)["coordenades"] for vertex in cami]
      return json.dumps([cami, visualitzacio])

  return render_template("index.html")


@app.errorhandler(404)
def error404(e):
  return render_template("error/pagina_no_trobada.html"), 404


@app.errorhandler(Exception)
def error500(e):
  return render_template("error/error_del_servidor.html"), 500
