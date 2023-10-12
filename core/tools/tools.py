#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
TMPland - 2023 - por jero98772
TMPland - 2023 - by jero98772
"""
from hashlib import  sha256
import base64
import numpy as np
import matplotlib.pyplot as plt

from subprocess import run
import chess
from multiprocessing import Pool
import os
import random
import pandas as pd
import chess.svg
import pydeck as pdk
import networkx as nx
import os
import json
import scipy.io.wavfile as wav
import scipy.signal as signal
from PIL import Image
import datetime
def enPassowrdStrHex(password):
	password = str(password)
	hashPassowrd = str(sha256(password.encode('utf-8')).hexdigest())
	return hashPassowrd
def enPassowrdHash(password):
	password = str(password)
	hashPassowrd = sha256(password.encode("utf-8")).digest()
	return hashPassowrd
def generatePassword():
	"""generatePassword(),return srtring
	generate random string 
	"""
	genPassowrd = ""
	for i in range(0,16):
		if len(genPassowrd) >= 16 and len(genPassowrd)-len(hexStr) <= 16:
			num = rnd.randint(0,9999)
			if 32 > num >126:
				char = chr(num)
				genPassowrd += char
			else:
				hexStr = str(hex(hexStr))
				genPassowrd += hexStr
		else:
			break
	return genPassowrd
def createLedgerFile(name):
	"""
	writetxt(name,content) , write in txt file something  
	"""
	with open(name, 'w') as file:
		file.write("")
		file.close()
def deleteWithExt(path,ext):
    """
    deleteWithExt(<file path>,<file extencion>) , delete file with file extencion
    """
    if os.path.isfile(path+ext) :           
        os.remove(path+ext)
def img2asciiart(img,size = 15,intensity = 255,replaceItem = 0,items = ["@"," "]):
    """
    img2asciiart(img,size = 15,intensity = 255,replaceItem = 0,items = ["@"," "]) ,return a  matrix img as str
    """
    import cv2
    from numpy import asarray 
    dataFile = cv2.imread(img,cv2.IMREAD_GRAYSCALE)
    imgresized  = cv2.resize(dataFile , (size, size))
    imgstr = ""
    #imgstr = asarray(imgresized , dtype= str)
    for count in range(len(imgresized)):
        for cont in range(len(imgresized[count]))  :
                if imgresized[count,cont]//intensity == replaceItem:
                    #imgstr[count,cont]= items[0]
                    imgstr += items[0]
                else:
                    #imgstr[count,cont] = items[1]
                    imgstr += items[1]
        imgstr += "\n"
    outfig = [imgresized,imgstr]
    return outfig 
def readtxtR(name):
	"""
	readtxt(name) , return txt content as array ,element by line 
	"""
	content = []
	with open(name, 'r') as file:
		for i in file.readlines():
			content.append(str(i).replace("\n",""))
	return reversed(content)
def formatin(category):
	now=datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
	return "i "+now+" "+category+"\n"
def formatout():
	now=datetime.datetime.today().strftime("%Y/%m/%d %H:%M:%S")
	return "o "+now+"\n"
def writef(fname,content):

	"""
	writetxt(name,content) , write in txt file something  
	"""
	with open(fname, 'a') as file:
		file.write(content)
		file.close()
#def outcategory():
def getbal(fname,txt="data/tmp.txt"):
	run(f"ledger -f {fname} bal > {txt}",shell=True)
	return readtxt(txt)
def getbalday(fname,txt="data/tmp.txt"):
    run(f'ledger -f {fname} bal -p "since today" > {txt}', shell=True)
    return readtxt(txt)
def hoyminsStr():
    """
    return date and hours and minutes as string
    """
    hoy = datetime.datetime.today().strftime("%m/%d/%Y, %H:%M")
    return hoy
def date2int(date):
    """
    date2int(date) convert date to int
    """
    date = str(date)
    intdate = date.replace(":","").replace("/","").replace(",","").replace(" ","")
    return int(intdate)
def setUpdate(dataname, data):
    """
    generate update sentece for sqlite3 
    """
    sentence = dataname[0]+" = "+ '"'+data[0]+'"'
    for i ,ii in zip(dataname[1:] , data[1:]):
        sentence += ','+i+" = "+ '"'+ii+'"'
    return sentence
def concatenateStrInList(arr):
    """
    concatenates the numbers of a string, the elements of an array : return  integer
    """
    intAsString = ""
    for i in arr:
        intAsString += i
    return int(intAsString)
def getImg(url,imgname):
    """
    get image form url 
    """
    import requests
    imgrequ = requests.get(url).content
    with open(imgname, "wb") as file:
        file.write(imgrequ)
class play:
  def __init__(self,player=None,depth=4,lang="en"):
    self.gregos = not player
    self.player = player
    self.board = chess.Board()
    self.turn = 1
    self.depth = depth
    self.audio = 1
    self.openings=pd.read_csv("https://raw.githubusercontent.com/jero98772/Gregos/main/data/chess_openings.csv",sep=",").head(1000)
    self.opening=""
    self.langue=lang
    self.langueWords=None



  def get_board(self):
    return self.board
    #in future we add a langue option   

  def greeting(self):
    return "Hello i am Gregos an i will be your trainer"
  #def __dict__(self):
    #return {"gregos":self.gregos,"player":self.player,"board":self.board}


def uci2algebraic(move:str,board:chess.Board()):
	"""
	convert from uci notation to algebraic notation
	"""
	movef=chess.Move.from_uci(move)
	return board.san(movef)
def speak(audioString:str,path:str,lang='es'):
	"""
	speak audioString variable using google text to speak and a system call
	"""
	tts = gTTS(text=audioString,lang=lang)
	tts.save(path)
	os.system("mpg123 "+path)

def all_attackers(board:chess.Board(),color:bool)->int:
	"""
	return a number of attackers for color
	"""
	total=0
	for i in range(64):
  		total+=len(board.attackers(color,i)) 
	return total

def calculate_posibles_openings(move:str,turn:int,colname:str,rows:list,dataframe):
  """

  """
  for i in range(len(rows)):
    try:
      if dataframe[colname][i].split()[turn]!=move:
        dataframe=dataframe.drop(index=i)
    except:
      dataframe=dataframe.drop(index=i)

  return dataframe.reset_index(drop=True)

def save_board_as_image(board:chess.Board(),path:str):
	"""
	save board as image
	"""
	boardsvg = chess.svg.board(board)
	outputfile = open(path+".svg", "w")
	outputfile.write(boardsvg)
	outputfile.close()

def score_analisis(board:chess.Board(), my_color:bool):
	"""
	score_analisis the heuristic , this function calculate the score of the board
	"""
	POINTS_BY_PIECE = [
	(chess.PAWN,100),
	(chess.KNIGHT,320),
	(chess.BISHOP, 330),
	(chess.ROOK, 500),
	(chess.QUEEN, 900),
	(chess.KING, 20000)
	]
	score = random.random()*10
	for (piece, value) in POINTS_BY_PIECE:
		score+=len(board.pieces(piece, my_color)) * value
		score-=len(board.pieces(piece, not my_color)) * value
	score += 100 if board.is_checkmate() else 0
	score -= 20 if board.is_insufficient_material() else 0
	score -= 10 if board.is_stalemate() else 0
	
	#add pawns structure
	#score +=all_attackers(board,not my_color)
	#score -=all_attackers(board,my_color)
	return score
def winner(board:chess.Board(),turn:bool)->str:
	"""
	return a string the color of the winner
	"""
	if board.is_checkmate():
		if turn:return "White Win"
		else:return "Black Win"
	else: 
		return "No winner"

def gameover(board:chess.Board())->bool:
	"""
	Function that is in charge of evaluating if the match has gotten to a stalemate point, if it did returns
 	True, otherwise returns False.
	"""
	return board.is_stalemate() or board.is_insufficient_material() or board.is_checkmate() or board.is_seventyfive_moves() or board.is_variant_draw()

def alphabeta(board:chess.Board, depth:int, alpha:int, beta:int,  maximizing_player:bool, maximizing_color:bool) -> int:
  """
  #This function implements the MinMax algorithm along with the Alpha-Beta pruning enhancement technique. 
  #Minmax is an heuristic search algorithm that finds the best possible way to make a play when there's multiple 
  #choices available. Also works with the help of Alpha-Beta pruning technique which iscommonly use to discard 
  #the choices (branches of the tree) that don't show any benefits respect to the solution.
  """
  if depth == 0 or board.is_game_over():
    return score_analisis(board, maximizing_color)
  # Generate legal moves
  legal_moves = list(board.legal_moves)
  # Randomize moves to avoid predictable move patterns
  random.shuffle(legal_moves)
  
  if maximizing_player:
    max_eval = float('-inf')
    for move in legal_moves:
      board.push(move)
      eval = alphabeta(board, depth-1, alpha, beta, False, maximizing_color)
      board.pop()

      max_eval = max(max_eval, eval)
      alpha = max(alpha, eval)
      if beta <= alpha:
          break
    return max_eval
  else:
    min_eval = float('inf')
    for move in legal_moves:
      board.push(move)
      eval = alphabeta(board, depth-1, alpha, beta, True, maximizing_color)
      board.pop()

      min_eval = min(min_eval, eval)
      beta = min(beta, eval)
      if beta <= alpha:
          break
    return min_eval

def get_best_move(board:chess.Board, depth:int,  maximizing_player:bool, maximizing_color:bool):
  """
  Function that returns the best move using Alpha-Beta algorithm
  """
  best_move = None
  max_eval = float('-inf')
  alpha = float('-inf')
  beta = float('inf')
  for move in board.legal_moves:
      board.push(move)
      evalf = alphabeta(board, depth-1, alpha, beta,  maximizing_player, maximizing_color)
      board.pop()
      if evalf > max_eval:
          max_eval = evalf
          best_move = move
  return best_move, max_eval


def webTranslate(txt,writeIn,translateTo):
  from deep_translator import GoogleTranslator 
  translatedTxt = GoogleTranslator(source=writeIn, target=translateTo).translate(txt)
  return translatedTxt

def transateweb(lang):
  Available_moves=webTranslate("Available moves","en",lang)
  nexttxt=webTranslate("Next","en",lang)
  play=webTranslate("Play","en",lang)
  move=webTranslate("Move","en",lang)
  recomends_you=webTranslate("recomend you","en",lang)
  return {"Available_moves":Available_moves,"next":nexttxt,"play":play,"move":move,"gregos_recomend":recomends_you}


def writetxt(name,content,mode="w"):
  """
  writetxt(name,content) , write in txt file something  
  """
  content=str(content)
  with open(name, mode) as file:
    file.write(content)
    file.close()

def readtxt(name):
  """
  readtxt(name) , return txt content as array ,element by line 
  """
  content = []
  with open(name, 'r') as file:
    for i in file.readlines():
      content.append(str(i).replace("\n",""))
  return content
def joinWebpage(direccions,webApp,actualapp,url=""):  
    for webroute in direccions:   
      @actualapp.route(url+webroute, endpoint=webroute , methods=['GET','POST'])
      def site():
        return webApp
    return site()
    
def genPreview(name,path):
    txt = f'\n\t@app.route("/{name}")\n\tdef {str(name[:-5]).replace("/","")}():\n\t\treturn render_template("{path}/{name}")'
    return txt

def initMap(dataDir:str)->None:
    """
    initMap(dataDir:str)->None
    create python file with code for add flask,like the code that generates genPreview 
    """
    newCode = """from flask import Flask, render_template
app = Flask(__name__)
class maps():"""
    writetxt(dataDir,newCode)
    #tryng to move to emacs is ... a disasters with tabs 
def validData(txt:str,dicts:list)-> bool:
  """
  validData(txt:str,dicts:list)-> bool
  check if data is valid, if character is in dicts is not valid
  """
  tmp=False
  for i in txt:
    if not i in dicts:
      tmp=False
      break
    else:
      tmp=True
  return tmp

def readRealtime(name:str,sep=";"):
  """
  readRealtime(name:str,sep=";":str)) , is a genteretor return row of csv at iteration 
  """
  with open(name, 'r') as file:
    for i in file.readlines():
      yield i.split(sep)

def fixFiles(maps):
	if os.path.isfile(maps):
	    if readtxt(maps)=="":
	        initMap(maps)
	    try:
	        from .maps import maps 
	        from .maps import app as appmaps
	        joinWebpage(FILES,appmaps,app,"/")
	        print("not try error")
	    except:
	        print("error open file")
	else:
	    initMap(maps)

class configData:
    def __init__(self,file,sep=";"):
        self._data=""
        if file[-4:]==".csv":
            self._data = pd.read_csv(file,sep=";")
        if file[-5:]==".json":
            self._data = pd.read_json(file)

    #if needed download, you can pass a url remote acces of data
    def downloadCsv(self):
        self._data.to_csv(index=False)

    def downloadJson(self):
        self._data.to_json(index=False)

    def getData(self):
        return self._data
    #code for clear data     
    def clearDataJsonRoutes(data,name="out.json"):
        dataclear = ""
        for i in range(len(data)): 
            origin = (data["origin"][i][1:-1].split(","))
            destination = (data["destination"][i][1:-1].split(","))
            try:
                dataclear+='{"name":"'+data["name"][i]+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+"]]},"
            except:
                dataclear+='{"name":"'+str(i)+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+"]]},"
        writetxt(name,"["+dataclear[:-1]+"]")
    
    def clearAllDataJson(data,name="out.json"):
        dataclear = ""
        for i in range(len(data)): 
            origin = (data["origin"][i][1:-1].split(","))
            destination = (data["destination"][i][1:-1].split(","))
            try:
                dataclear+='{"name":"'+data["name"][i]+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+']],"node":['+origin[0]+","+origin[1]+'],"harassmentRisk":'+str(data["harassmentRisk"][i]).replace("nan","0")+',"length":'+str(data["length"][i])+'},'
            except:
                dataclear+='{"name":"'+str(i)+'","path": ['+"["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1]+']],"node":['+origin[0]+","+origin[1]+'],"harassmentRisk":0,"length":'+str(data["length"][i])+'},'
        writetxt(name,"["+dataclear[:-1]+"]")

    def createNodes(self,data,name="data/out.json"):
        data=self.data
        dataclear = ""
        for i in range(len(data)): 
            origin = (data["origin"][i][1:-1].split(","))
            destination = (data["destination"][i][1:-1].split(","))
            try:
                dataclear+='{"name":"'+data["name"][i]+'","node":['+origin[0]+','+origin[1]+']},'
            except:
                dataclear+='{"name":"'+str(i)+'","node":['+origin[0]+','+origin[1]+']},'
        writetxt(name,"["+dataclear[:-1]+"]")
    def cretejson(self,fileName="data/"):
        import numpy as np

        if fileName=="data/":
            salt=str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
            fileName="data"+str(salt)
        mean=np.mean(self._data["harassmentRisk"])
        for i in range(len(self._data)):
            length=self._data["length"][i]
            origin = (self._data["origin"][i][1:-1].split(","))
            destination = (self._data["destination"][i][1:-1].split(","))
            node=[str(self._data["origin"][i][1:-1])]
            edges="["+str(node)+",["+str(self._data["destination"][i][1:-1])+"]]"
            weights=(self._data["harassmentRisk"][i]*length)/length

        if np.isnan(self._data["harassmentRisk"][i]) and  (self._data["name"][i]=="nan" or type(self._data["name"][i])==type(0.0)):
            weights=(mean*length)/length
            newdata+='{"name":"'+str(i)+'","origin":"'+str(self._data["origin"][i])+'","destination":"'+str(self._data["destination"][i])+'","length":"'+str(self._data["length"][i])+'","oneway":"'+str(self._data["oneway"][i])+'","harassmentRisk":"'+str(mean)+'","geometry":"'+str(self._data["geometry"][i])+'","weights":"'+str(weights)+'","edges":"'+str("[["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1])+']]","node":"['+origin[0]+","+origin[1]+']"},'
        
        elif self._data["name"][i]=="nan" or type(self._data["name"][i])==type(0.0) :
            newdata+='{"name":"'+str(i)+'","origin":"'+str(self._data["origin"][i])+'","destination":"'+str(self._data["destination"][i])+'","length":"'+str(self._data["length"][i])+'","oneway":"'+str(self._data["oneway"][i])+'","harassmentRisk":"'+str(self._data["harassmentRisk"][i])+'","geometry":"'+str(self._data["geometry"][i])+'","weights":"'+str(weights)+'","edges":"'+str("[["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1])+']]","node":"['+origin[0]+","+origin[1]+']"},'
        
        elif np.isnan(self._data["harassmentRisk"][i]):
            weights=(mean*length)/length
            newdata+='{"name":"'+self._data["name"][i]+'","origin":"'+str(self._data["origin"][i])+'","destination":"'+str(self._data["destination"][i])+'","length":"'+str(self._data["length"][i])+'","oneway":"'+str(self._data["oneway"][i])+'","harassmentRisk":"'+str(mean)+'","geometry":"'+str(self._data["geometry"][i])+'","weights":"'+str(weights)+'","edges":"'+str("[["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1])+']]","node":"['+origin[0]+","+origin[1]+']"},'

        else:
            newdata+='{"name":"'+self._data["name"][i]+'","origin":"'+str(self._data["origin"][i])+'","destination":"'+str(self._data["destination"][i])+'","length":"'+str(self._data["length"][i])+'","oneway":"'+str(self._data["oneway"][i])+'","harassmentRisk":"'+str(self._data["harassmentRisk"][i])+'","geometry":"'+str(self._data["geometry"][i])+'","weights":"'+str(weights)+'","edges":"'+str("[["+origin[0]+","+origin[1]+"]"+",["+destination[0]+","+destination[1])+']]","node":"['+origin[0]+","+origin[1]+']"},'
        writetxt(fileName+".json","["+newdata[:-1]+"]")

    def cretecsv(self,fileName="data/"):
        import numpy as np

        newdata="name;origin;destination;length;oneway;harassmentRisk;geometry;weights;edges;node\n"
        mean=np.mean(self._data["harassmentRisk"])

        if fileName=="data/":
            salt=str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
            fileName="data"+str(salt)
        for i in range(len(self._data)):
            length=self._data["length"][i]
            node=[str(self._data["origin"][i][1:-1])]
            edges="["+str(node)+",["+str(self._data["destination"][i][1:-1])+"]]"
            weights=(self._data["harassmentRisk"][i]*length)/length

            if np.isnan(self._data["harassmentRisk"][i]) and  (self._data["name"][i]=="nan" or type(self._data["name"][i])==type(0.0)):
                weights=(mean*length)/length
                newdata+=str(i)+";"+str(self._data["origin"][i])+";"+str(self._data["destination"][i])+";"+str(self._data["length"][i])+";"+str(self._data["oneway"][i])+";"+str(mean)+";"+str(self._data["geometry"][i])+";"+str(weights)+";"+str(edges)+";"+";"+str(node)+"\n"
            
            elif self._data["name"][i]=="nan" or type(self._data["name"][i])==type(0.0) :
                newdata+=str(i)+";"+str(self._data["origin"][i])+";"+str(self._data["destination"][i])+";"+str(self._data["length"][i])+";"+str(data["oneway"][i])+";"+str(self._data["harassmentRisk"][i])+";"+str(self._data["geometry"][i])+";"+str(weights)+";"+str(edges)+";"+";"+str(node)+"\n"
            
            elif np.isnan(self._data["harassmentRisk"][i]):
                weights=(mean*length)/length
                newdata+=str(data["name"][i])+";"+str(data["origin"][i])+";"+str(data["destination"][i])+";"+str(data["length"][i])+";"+str(data["oneway"][i])+";"+str(mean)+";"+str(data["geometry"][i])+";"+str(weights)+";"+str(edges)+";"+";"+str(node)+"\n"
            
            else:
                newdata+=str(data["name"][i])+";"+str(data["origin"][i])+";"+str(data["destination"][i])+";"+str(data["length"][i])+";"+str(data["oneway"][i])+";"+str(data["harassmentRisk"][i])+";"+str(data["geometry"][i])+";"+str(weights)+";"+str(edges)+";"+";"+str(node)+"\n"
            writetxt(fileName+".csv",newdata)

class graphX():
    """
    create graph with pandas data
    """
    def __init__(self,data):
        self.graph=nx.Graph()
        for i in range(len(data)):
            node=data["node"][i]
            weight=(data["harassmentRisk"][i]+0.5)*data["length"][i]
            #weight=(data["length"][i])
            self.graph.add_edge(str(data["edges"][i][0]),str(data["edges"][i][1]),weight=weight)
            self.graph.add_node(str(node))

class fastgraphX():
    """
    create graph while read file
    """
    def __init__(self,file):
        self.graph=nx.Graph()
        i=0
        for data in readRealtime(file,sep=";"): 
            if i==0:
                i+=1
            else:
                edge=data[-2][2:-2].split("],[")
                self.graph.add_edge(str(edge[0]),str(edge[1]),weight=float(data[-3]))
                self.graph.add_node(str(data[-1][:-1]))
            i+=1

class pathsX(graphX):
    def __init__(self,data,source,target,graphtype):
        """
        class for chose shorts path algoritms
        modes
        fast
        nofast
        """
        super().__init__(data)
        self._source=source
        self._target=target
    def dijkstra(self):
        self._nodes=nx.dijkstra_path(self.graph, self._source, self._target, weight='weight')

    def dijkstraNoW(self):
        self._nodes=nx.dijkstra_path(self.graph, self._source, self._target, weight=None)

    def bellmanford(self):
        self._nodes=nx.shortest_path(self.graph, self._source, self._target, weight='weight', method='bellman-ford')

    def getData(self):
        """
        return data from shorts path algoritms
        """
        pathdf=pd.DataFrame([{"name":"path","path":[eval(i) for i in self._nodes]}])
        return pathdf
    def printg(self):
        print(self.graph.to_string())

#debugs code no erase
#self._nodes=nx.dijkstra_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5572602, 6.2612576]", weight=None)
#self._nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight=None, method='bellman-ford')
#nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight='weight', method='dijkstra')
#nodes=nx.shortest_path(Grafo, "[-75.6909483, 6.338773]", "[-75.5705202, 6.2106275]", weight=None, method='dijkstra')
#self._nodes=nx.dijkstra_path(self.graph, "[-75.6909483, 6.338773]", "[-75.5572602, 6.2612576]", weight=None)

class configMap:
    """
    class for draw in map
    """
    def __init__(self,data):

        self.emptyMap = pdk.Layer(
            type="PathLayer",
            data="",
            pickable=True,
            get_color=(0,155,0),
            width_scale=1,
            width_min_pixels=1,
            get_path="edges",
            get_width=1,
        )

        self.pathMap = pdk.Layer(
            type="PathLayer",
            data=data,
            pickable=True,
            get_color=(0,155,0),
            width_scale=1,
            width_min_pixels=1,
            get_path="edges",
            get_width=2,
        )

        self.nodesMap = pdk.Layer(
            "ScatterplotLayer",
            data=data,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="node",
            get_radius=1,
            get_fill_color=[137, 36, 250],
            get_line_color=[0, 0, 0],
        )

    def newPath(data,tag="path",color=(0,15,205)):
        newPath = pdk.Layer(
            type="PathLayer",
            data=data,
            pickable=False,
            get_color=color,
            width_scale=5,
            width_min_pixels=5,
            get_path=tag,
            get_width=5,
        )
        return newPath

    def genMapMultlayer(self,fileName,layers:list):
        view = pdk.ViewState(latitude=6.256405968932449, longitude= -75.59835591123756, pitch=40, zoom=12)
        mapCompleate = pdk.Deck(layers=layers, initial_view_state=view)
        mapCompleate.to_html(fileName)
    
    def getEmptyMap(self):return self.emptyMap
    def getPathMap(self):return self.pathMap
    def getnodesMap(self):return self.nodesMap

def noaaResample(name:str,savesf:str):
    fs, data = wav.read(savesf)  
    data_crop = data[20*fs:21*fs]
    analytical_signal = signal.hilbert(data)
    data_am = np.abs(analytical_signal)
    frame_width = int(0.5*fs)
    w, h = frame_width, data_am.shape[0]//frame_width
    image = Image.new('RGB', (w, h))
    px, py = 0, 0
    for p in range(data_am.shape[0]):
        lum = int(data_am[p]//32 - 32)
        if lum < 0: lum = 0
        if lum > 255: lum = 255
        image.putpixel((px, py), (0, lum, 0))
        px += 1
        if px >= w:
            px = 0
            py += 1
            if py >= h:
                break
    image = image.resize((w, 4*h))
    plt.imshow(image)
    filename=name.replace(".wav",".png")
    plt.savefig(filename)
    return filename
def noaa(name:str,savesf:str):
    fs, data = wav.read(savesf)  
    data_crop = data[20*fs:21*fs]
    resample = 4
    data = data[::resample]
    fs = fs//resample
    analytical_signal = signal.hilbert(data)
    data_am = np.abs(analytical_signal)
    frame_width = int(0.5*fs)
    w, h = frame_width, data_am.shape[0]//frame_width
    image = Image.new('RGB', (w, h))
    px, py = 0, 0
    for p in range(data_am.shape[0]):
        lum = int(data_am[p]//32 - 32)
        if lum < 0: lum = 0
        if lum > 255: lum = 255
        image.putpixel((px, py), (0, lum, 0))
        px += 1
        if px >= w:

            px = 0
            py += 1
            if py >= h:
                break
    image = image.resize((w, 4*h))
    plt.imshow(image)
    filename=name.replace(".wav",".png")
    plt.savefig(filename)
    return filename