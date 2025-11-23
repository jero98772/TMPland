#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
TMPland - 2023 - por jero98772
TMPland - 2023 - by jero98772
"""
from flask import Flask
from .tools.webutils import *
import os
app = Flask(__name__)

#B-feelLog

app.config["TEMPLATES_AUTO_RELOAD"] = True
EXCLUDEDCHARACTER = "#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~"
BLOGWEBDIR = "/blog/"
TEMPLATE = "core/templates/template.html"
BLOGPATH = "core/templates/blog/"
AUTHORFILE = "data/blog/authorfile.txt"
TOKENPATH = "data/blog/token.txt"
WHATISFILE = "data/blog/whatisfile.txt"
BLOGFILE = "core/blogs.py"
INDEX = "/blog.html"
#FILEUPLOAD = "static/uploads"
#FILESONLINE = "core/templates/config/files.html"
#app.config['UPLOAD_FOLDER']=FILESONLINE
TOKEN = readLine(TOKENPATH)
AUTHOR = readLine(AUTHORFILE)
USE = readLine(WHATISFILE)
BLOGINDEX="/blog.html"
try:
	BLOGS = blogNames(BLOGPATH)
	print(BLOGS)
except:
	os.mkdir(BLOGPATH)

BLOGSFILES = filesInFolders(BLOGPATH)
SUPORTEDLANGUAGES = ["No translate","spanish","english","german","basque","italian","russian"]
SUPORTEDLANGUAGESSEAMLESS={"german":"deu","english":"eng","spanish":"spa","russian":"rus"}

if os.path.isfile(BLOGFILE):
	try:
		from .blogs import blogs 
		from .blogs import app as appblogs 
		joinWebpage(BLOGSFILES,appblogs,app,url=BLOGWEBDIR)
	except:
		updateBlog(BLOGSFILES,BLOGFILE)
#projects
PROJECTSNAMEFILE="data/projects.txt"
PROJECTSWEBDIR = "/projects/"

#ttweb

DBPATHTT = "data/ttweb/"
DATAUSERTT ="data/ttweb/datauser/"
DBNAMETT = DBPATHTT + "db"
PROJECTSTTWEBDIR = PROJECTSWEBDIR+"/ttweb/"
TTFOLDER = "ttweb/"

#gregos

AUDIO_PATH="core/static/mp3/gregos/audio.mp3"
BOARD_IMG_PATH="core/static/img/gregos/tmp"
player=None
BASELANGE="en"
GREGOSFOLDERFOLDER = "gregos/"
PROJECTSGREGOSDIR = PROJECTSWEBDIR+"/Gregos/"
LANGUESGREGOS=["english","español","desch"]
GREGOSBANNER="""
  ____                          
 / ___|_ __ ___  __ _  ___  ___ 
| |  _| '__/ _ \/ _` |/ _ \/ __|
| |_| | | |  __/ (_| | (_) \__ \ 
 \____|_|  \___|\__, |\___/|___/
                |___/           
"""


#alotrolado


TEMPLATEDIR="templates/alOtroLado"
MAPS="core/maps.py"
MAPWEBADRESS="/maps/"
MAPSDIR="core/templates"+MAPWEBADRESS
FILES = os.listdir(MAPSDIR)

DATACSVFILE="https://raw.githubusercontent.com/entifais/ST0245-Plantilla/master/proyecto/codigo/alOtroLado/data/calles_de_medellin_con_acoso.csv"
DATACSVFILE="data/calles_de_medellin_con_acoso.csv"
DATANODESJSON="core/data/nodes_data.json"
DATAJSON="https://raw.githubusercontent.com/jero98772/AlOtroLado/main/core/data/medellin_data.json"#"core/data/medellin_data.json"
DATACOMPLETE="core/data/data_csv.csv"

PROJECTSALOTROLADOWEBDIR = PROJECTSWEBDIR+"/AlOtroLado/"
ALOTROLADOFOLDER = "AlOtroLado/"

# mixprojecs

MIXPROJECTS="/projects/"
PROJECTSFOLDER="projects/"

#NOAA

NOAASAVESFOLDER="core/static/audio/noaa/"
NOAAIMGFOLDER="img/noaa/"
NOAAIMGFOLDER2="core/static/"+NOAAIMGFOLDER
NOAAWEBDIR=PROJECTSWEBDIR+"/Noaa-decoding"
NOAAFOLDER="Noaa-decoding/"


#WWWOF

WWWOFWEBDIR=PROJECTSWEBDIR+"wwwof/"
WWWOFFOLDER="wwwof/"

#arreBatEro

ARREBATOWEBDIR=PROJECTSWEBDIR+"/arreBatEro/"
ARREBATOFOLDER="arreBatEro/"
ASCIITMPIMG="core/static/img/img2ascii/"

#GAS

GASDBPATH = "data/gas/"
DBNAMEGAS = GASDBPATH + "gas_db"
TABLEGAS = "gastos"
GASLOGINTABLE = "logingastos"
DATANAMEGAS = ["item","category","thread","price","amount","date"]

GASWEBDIR=PROJECTSWEBDIR+"GAS/"
GASFFOLDER="GAS/"

#commap

COMMAPWEBDIR=PROJECTSWEBDIR+"commap/"
COMMAPFFOLDER="commap/"

COMMAPDATAPATH="data/commap/data.csv"
COMMAPMAPNAME=COMMAPFFOLDER+"map.html"