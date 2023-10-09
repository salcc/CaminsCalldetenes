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

from flask import Flask, render_template, request, g

from cami_mes_curt import a_star_bidireccional
from cami_mes_curt_visual import visual, visual_bidireccional
from utils import vertex_mes_proper

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
  # Abans que comenci la primera sol·licitud de buscar un camí més curt, es
  # carrega el graf que haurà set prèviament convertit des d'un fitxer OSM XML.
  if 'graf' not in g:
    with open("static/graf.pickle", "rb") as fitxer_graf:
      g.graf = pickle.load(fitxer_graf)
  G = g.graf

  user_agent = request.user_agent.string
  if "MSIE" in user_agent or "Trident" in user_agent or "Edge" in user_agent:
    return render_template("error/navegador_no_suportat.html")
  if request.method == "POST":
    data = request.get_json()
    i = vertex_mes_proper(G, data["coords_inicial"])
    f = vertex_mes_proper(G, data["coords_final"])
    algorisme = data["algorisme"]

    if "visual" in algorisme:
      if "bidireccional" in algorisme:
        cami, visualitzacio = visual_bidireccional(G, i, f, "llargada", "a_star" in algorisme)
      else:
        cami, visualitzacio = visual(G, i, f, "llargada", "a_star" in algorisme)
      cami = [G.llegir_atributs(vertex)["coords"] for vertex in cami]
      return json.dumps([cami, visualitzacio])

    cami = a_star_bidireccional(G, i, f, "llargada")
    cami = [G.llegir_atributs(vertex)["coords"] for vertex in cami]
    return json.dumps(cami)

  return render_template("index.html")


@app.errorhandler(404)
def error404(e):
  return render_template("error/pagina_no_trobada.html"), 404


@app.errorhandler(Exception)
def error500(e):
  return render_template("error/error_del_servidor.html"), 500
