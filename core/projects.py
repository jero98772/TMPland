#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
TMPland - 2023 - por jero98772
TMPland - 2023 - by jero98772
"""

from .constants import *
from flask import Flask, render_template ,request,session,redirect,send_file,send_from_directory,flash
from .tools.webutils import *
from .tools.tools import *
from .tools.dbInteracion import dbInteraciontt,dbInteracionGas
from .tools.criptools import *
from .tools.flasktools import *

class tt():
  @app.route(PROJECTSTTWEBDIR,methods = ['GET','POST'])
  def ttindex():
    data=""
    try:
      datafile=getbalday(session['file'])
    except:
      datafile=""
    if request.method == 'POST':
      if session['status']:
        data=request.form["category"]
        if data!="":
          session['status']=False
          writef(session['file'] ,formatin(data))
      else:
        writef(session['file'] ,formatout())
        session['status']=True
    return render_template(TTFOLDER+"index.html",data=data,datafile=datafile)

  @app.route(PROJECTSTTWEBDIR+"/login.html",methods = ['GET','POST'])
  def ttlogin():
    if request.method == 'POST':
      db = dbInteraciontt(DBNAMETT)
      db.connect("login")
      usr = request.form["username"]
      if db.findUser(usr) and db.findPassword(enPassowrdStrHex(request.form["password"])):
        session['loged'] = True
        session['user'] = usr
        file=DATAUSERTT+usr+".ldg"
        session['file'] = file
        session['status']=True
        return redirect(PROJECTSTTWEBDIR)
    return render_template(TTFOLDER+"login.html")
  @app.route(PROJECTSTTWEBDIR+"/register",methods = ['GET','POST'])
  def registertt():
    msg=""
    if request.method == 'POST':
      pwd = request.form["pwd"]
      pwd2 = request.form["pwd2"]
      if pwd == pwd2 :
        usr = request.form["usr"]
        db = dbInteraciontt(DBNAMETT)
        db.connect("login")
        if db.findUser(usr):
          msg="User alredy register"
        else:
          if db.userAvailable(usr,"usr") :
            db.saveUser(usr,enPassowrdStrHex(pwd))
            try:
              file=DATAUSERTT+usr+".ldg"
              createLedgerFile(file)
              session['status']=True
              session['loged'] = True
              session['user'] = usr
              session['file'] = file
            except db.userError():
              return "invalid user , please try with other username and password"		
      else:
        msg="Passwords must be same"
    return render_template(TTFOLDER+"register.html",msg=msg)
  @app.route(PROJECTSTTWEBDIR+"/unlog")
  def unlog():
    session['status']= False
    session['loged']= False
    session['user'] = ""
    session['file'] = ""
    return redirect("/")
  @app.route(PROJECTSTTWEBDIR+"/data.html")
  def data():
    data=""
    try:
      if session['loged']:
        data=getbal(session['file'])
    except:
        data="you need login"
    return render_template(TTFOLDER+"data.html",data=data)


class gregos:
  @app.route(PROJECTSGREGOSDIR,methods=['POST','GET'])
  @app.route(PROJECTSGREGOSDIR+"/startgame.html",methods=['POST','GET'])  
  def startgame():
    if request.method == "POST":
      color=request.form["color"]
      level=request.form["level"]
      langue=str(request.form["langue"])[0:2].lower()
      gamemode=request.form["mode"].replace(" ","")
      color = 1 if color == "White" else 0
      #print(player)
      global player
      print(player)
      player=play(lang=langue)
      print(player)
      player.player = color
      player.gregos = not color
      player.depth = int(level)-1
      player.audio = 0
      player.langueWords = transateweb(langue)
      return redirect(PROJECTSGREGOSDIR+f"/game/{gamemode}")
    return render_template(GREGOSFOLDERFOLDER+"startgame.html",banner=GREGOSBANNER,langues=LANGUESGREGOS)

  @app.route(PROJECTSGREGOSDIR+"/game/PlayervsMachine",methods=['POST','GET'])  
  def PlayervsMachine():
    win_probability=None
    print(player.turn)
    save_board_as_image(player.board,BOARD_IMG_PATH)
    print(player.langue)
    if len(player.openings)==1:
      player.opening=webTranslate("you opening is",BASELANGE,player.langue)+" "+player.openings["opening_name"][0]
    print(player.turn)  
    if len(player.openings)==0 and player.opening=="":
      player.opening=webTranslate("you make a unknown opening",BASELANGE,player.langue)
    print(player.turn)
    if player.turn%2==player.gregos:#gregos play
      best_move,score=get_best_move(player.board, player.depth, player.gregos, player.gregos)
      gregos_move=best_move
      movef = uci2algebraic(str(best_move),player.get_board())
      player.board.push_san(str(best_move))
      player.openings=calculate_posibles_openings(movef,player.turn-1,webTranslate("moves",BASELANGE,player.langue),player.openings["opening_name"],player.openings)
      """
      i use str(board.san(move)) to format move example from e2e4 for e4, to uci to normal notacion  
      """
      save_board_as_image(player.get_board(),BOARD_IMG_PATH)
      legal_moves=list(map(str,player.board.legal_moves))
      msg=webTranslate("i gregos move",BASELANGE,player.langue)+" "+str(gregos_move)
      
      
      player.turn+=1
      return render_template(GREGOSFOLDERFOLDER+"play.html",gregos_move=gregos_move,moves=legal_moves,gregos_turn=(player.turn%2==player.gregos),opening=player.opening,trad=player.langueWords)
    print(player.turn)    
    legal_moves=list(map(str,player.board.legal_moves))
    if request.method == "POST":
      move=request.form["move"]
      gregos_move,score=get_best_move(player.board, 4, player.player, player.player)#change 4 for play.deep
      msg=webTranslate("i gregos recommends you",BASELANGE,player.langue)+" "+str(gregos_move)
      

      movef = uci2algebraic(move,player.get_board())
      player.openings=calculate_posibles_openings(movef,player.turn-1,webTranslate("moves",BASELANGE,player.langue),player.openings["opening_name"],player.openings)
      player.board.push_san(str(move))
      player.turn+=1
      save_board_as_image(player.get_board(),BOARD_IMG_PATH)
    print(player.turn)  
    if player.turn==1:
       gregos_move="<pre>"+GREGOSBANNER+"\n"+webTranslate(player.greeting(),BASELANGE,player.langue)+"</pre>"
    print(player.turn)  
    return render_template(GREGOSFOLDERFOLDER+"play.html",gregos_move=gregos_move,moves=legal_moves,gregos_turn=(player.turn%2==player.gregos),opening=player.opening,trad=player.langueWords)

class alotrolado():
    #web app 
    fixFiles(MAPS)
    @app.route(PROJECTSALOTROLADOWEBDIR,methods=["GET","POST"])
    def alotroladoindex(): 
        msg=""
        data=configData(DATAJSON).getData()
        maps=configMap(data)

        if request.method=="POST":
            validateTxt="1234567890.,- []'"
            source=request.form["source"]
            target=request.form["target"]

            if target=="" or source=="" or  not (validData(target,validateTxt) and  validData(source,validateTxt)):
                msg="Datos invalidos"
            
            else:
                print
                data=configData(DATAJSON).getData()
                maps=configMap(data)
                print(source,target)
                newPath=pathsX(data,"["+str(source)+"]", "["+str(target)+"]",graphX)
                #newPath=pathsX(DATACOMPLETE,str(source),str(target),fastgraphX)
                newPath.dijkstra()
                nodesData=newPath.getData()                
                salt=str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")
                fileName="map"+str(salt)+".html"

                serveMapCode=genPreview(fileName,"maps")
                writetxt(MAPS,serveMapCode,"a")

                configMap.newPath(nodesData)
                layers=[maps.getPathMap(),maps.getnodesMap(),configMap.newPath(nodesData)]
                maps.genMapMultlayer(MAPSDIR+fileName,layers)
                funcs=[writetxt,maps.genMapMultlayer]
                args=[[MAPS,serveMapCode,"a"],[MAPSDIR+fileName,layers]]
                return redirect("/ineedtimetowork/"+fileName)
        return render_template(ALOTROLADOFOLDER+"index.html",msg=msg)

    #information web page
    @app.route(PROJECTSALOTROLADOWEBDIR+"/about.html")
    def alotroladoabout():
        return render_template(ALOTROLADOFOLDER+"about.html")

    #geografic visualisations
    @app.route(PROJECTSALOTROLADOWEBDIR+"/mapBase.html")
    def webMapBase():
        return render_template(ALOTROLADOFOLDER+"mapBase.html")
    @app.route(PROJECTSALOTROLADOWEBDIR+"/dotsdir.html")
    def dotsdir():
        return render_template(ALOTROLADOFOLDER+"mapsplots/dotsdir.html")  
    @app.route(PROJECTSALOTROLADOWEBDIR+"/heatmap.html")
    def heatmap():
        return render_template(ALOTROLADOFOLDER+"mapsplots/heatmap.html")
    @app.route(PROJECTSALOTROLADOWEBDIR+"/medellingraph.html")
    def medellingraph():
        return render_template(ALOTROLADOFOLDER+"mapsplots/medellingraph.html")
    
    #tests 
    @app.route(PROJECTSALOTROLADOWEBDIR+"/concord2tesoro.html")
    def concord2tesoro():
        return render_template(ALOTROLADOFOLDER+"examples/concord2tesoro.html")
    @app.route(PROJECTSALOTROLADOWEBDIR+"/eafit_santafe.html")
    def eafit_santafe():
        return render_template(ALOTROLADOFOLDER+"examples/eafit_santafe.html")
    @app.route(PROJECTSALOTROLADOWEBDIR+"/eafit2medellin.html")
    def eafit2medellin():
        return render_template(ALOTROLADOFOLDER+"examples/eafit2medellin.html")
    @app.route(PROJECTSALOTROLADOWEBDIR+"/antioquia2nacional.html")
    def antioquia2nacional():
        return render_template(ALOTROLADOFOLDER+"examples/antioquia2nacional.html")
    @app.route(PROJECTSALOTROLADOWEBDIR+"/nacional2luisamigo.html")
    def nacional2luisamigo():
        return render_template(ALOTROLADOFOLDER+"examples/nacional2luisamigo.html")

        
    #data
    @app.route(PROJECTSALOTROLADOWEBDIR+"/data.json")
    def webDataJson():
        data=json.dumps(readtxt(DATAJSON))
        response = app.response_class(response=data,mimetype='application/json')
        return response
    @app.route(PROJECTSALOTROLADOWEBDIR+"/nodes.json")
    def webDataNodes():
        data=json.dumps(readtxt(DATANODESJSON))
        response = app.response_class(response=data,mimetype='application/json')
        return response

    #redirection to make time,for fix error 
    @app.route(PROJECTSALOTROLADOWEBDIR+"/ineedtimetowork/<string:fileName>",methods=["GET","POST"])
    def redirected(fileName):
        return "<h1>please wait, my algoritm is very faster for this web</h1><script>setTimeout(function () {window.location.href = '/"+fileName+"';}, 1);</script>"
        return redirect(PROJECTSALOTROLADOWEBDIR+fileName)
  
class Noaa:
  @app.route(NOAAWEBDIR,methods=['GET','POST'])
  def indexnoaa():
      if not os.path.exists(NOAASAVESFOLDER):
          print("exist")
          os.mkdir(NOAASAVESFOLDER)
      if request.method == 'POST':
          name="wavnoaa"+str(datetime.datetime.now()).replace(" ","").replace("-","").replace(":","").replace(".","")+".wav"
          file = request.files["file"]
          file.save(NOAASAVESFOLDER+name)
          try:
              resample=request.form["resample"]
              print(resample,type(resample))
          except :
              resample=None
          if resample:
              return redirect(NOAAWEBDIR+"/outr/"+name)  
          else:  
              return redirect(NOAAWEBDIR+"/out/"+name)
      return render_template(NOAAFOLDER+"noaa.html")
  @app.route(NOAAWEBDIR+"/outr/<string:name>")
  def outr(name):
      print(NOAAIMGFOLDER+name)
      filename=noaaResample(NOAAIMGFOLDER2+name,NOAASAVESFOLDER+name)
      return render_template(NOAAFOLDER+"out.html",name=NOAAIMGFOLDER+name.replace(".wav",".png"))

  @app.route(NOAAWEBDIR+"/out/<string:name>")
  def out(name):
      print(NOAAIMGFOLDER+name)
      filename=noaa(NOAAIMGFOLDER2+name,NOAASAVESFOLDER+name)
      return render_template(NOAAFOLDER+"out.html",name=NOAAIMGFOLDER+name.replace(".wav",".png"))

class wwwof:
  @app.route(WWWOFWEBDIR)
  def indexwwwof():
    return render_template(WWWOFFOLDER+"wwwof.html") 
  @app.route(WWWOFWEBDIR+"calcupH.html")
  def calcuph():
    return render_template(WWWOFFOLDER+"ph.html") 
  @app.route(WWWOFWEBDIR+"drawFISHTANK.html")
  def drawFISHTANK():
    return render_template(WWWOFFOLDER+"drawFISHTANK.html") 
  @app.route(WWWOFWEBDIR+"divePC.html")
  def divePC():
    return render_template(WWWOFFOLDER+"divePC.html")

class arrebato:
  @app.route(ARREBATOWEBDIR)
  def criptools():
    return render_template(ARREBATOFOLDER+"index.html")

  @app.route(ARREBATOWEBDIR+"rsa.html",methods=['GET','POST'])
  def criptoolsrsa():
    timeNow = hoyminsStr()
    limit = int(date2int(timeNow))
    msg = ""
    encordecOptions = ["encript,with key","decript,with key","encript,with primes numbers","decript,with primes numbers"]
    data = ["text","n","private","public","prime1","prime2","encordec"]
    num1 , num2 = genprimes(limit)
    newN, publica , privada = genKey(num1 , num2)
    primes = [num1,num2]
    if request.method == 'POST':
      dataGet = multrequest(data)
      inMsg = dataGet[0]
      n = dataGet[1]
      if dataGet[len(data)-1] == encordecOptions[0]:
        privateKey = dataGet[2]
        msg = encryptRsa(inMsg,privateKey,n)
      elif dataGet[len(data)-1] == encordecOptions[1]:
        publicKey = dataGet[3]
        msg = decryptRsa(inMsg,publicKey,n)
      elif dataGet[len(data)-1] == encordecOptions[2]:
        prime1 = int(dataGet[4])
        prime2 = int(dataGet[5])
        n, publicKey , privateKey = genKey(prime1 , prime2)
        msg = encryptRsa(inMsg,privateKey,n)
      elif dataGet[len(data)-1] == encordecOptions[3]:
        prime1 = int(dataGet[4])
        prime2 = int(dataGet[5])
        n, publicKey , privateKey = genKey(prime1 , prime2)
        msg = decryptRsa(inMsg,publicKey,n)
    return render_template(ARREBATOFOLDER+"rsa.html" ,out = msg,primes = primes,n = newN , private = privada, public = publica)

  @app.route(ARREBATOWEBDIR+"sha256.html", methods=['GET','POST'])
  def criptoolshash():
    msg = ""
    if request.method == 'POST':
      sha256 = str(request.form["sha256"])
      msg = enPassowrdStrHex(sha256)
    return render_template(ARREBATOFOLDER+"hashs.html",returnsha = msg)
  @app.route(ARREBATOWEBDIR+"caesarcipher.html" ,methods=['GET','POST'])
  def cesar():
    message = ""
    key = rndkey()
    charshtml = chars2
    if request.method == 'POST':
      option = str(request.form["optioncesar"])
      key = int(request.form["key"])
      cesartext = str(request.form["cesartext"])
      newchars = str(request.form["chars"])
      if newchars != charshtml:
        charshtml = newchars
      if option == "cifrate":
        message   = cifrarcesar(cesartext, key,str(charshtml))
      elif option == "desifrate":
        message  = descifrarcesar(cesartext, key,str(charshtml))
      else:
        message = ""
    return render_template(ARREBATOFOLDER+"cesar.html",htmlchars = charshtml,resulthtml = message,htmlkey=key)
  @app.route(ARREBATOWEBDIR+"criptophone.html",methods=['GET','POST'])
  def criptophone():
    newmsg = ""
    options = ["encode","decode"]
    if request.method == 'POST':
      option = str(request.form["option"])
      message = str(request.form["message"])
      if option == options[0]:
        newmsg = encpalabranum(message)
      else:
        newmsg = decpalabranum(message)
    return render_template(ARREBATOFOLDER+"criptophone.html",out = newmsg)
  @app.route(ARREBATOWEBDIR+"asciiart2image.html",methods=['GET','POST'])
  def img2ascii():
    outfig = ""
    limitsize = lambda x,y: x if x<y else y
    size = 15
    name = "tmp"
    defaurltFill = "@"
    defaurltNoFill = " "
    intensity = 255
    replaceValue = 0
    defaultvalues = [defaurltFill,defaurltNoFill,replaceValue,intensity]
    fillvalues = [defaurltFill,defaurltNoFill]
    values = ["fillItem","noFillItem","size","intensity","replaceValue","image","url"]
    if request.method == 'POST':
      data = multrequest(values)
      size = int(limitsize(int(data[2]),100))
      defaultvalues = [data[0],data[1],data[4],data[3]]
      fillvalues = [data[0],data[1]]
      fileName = ASCIITMPIMG+name
      if data[5] == "file":
        imgfile = request.files["imgfile"]
        ext = getExt(str(imgfile))
        imgfile.save(fileName+ext)
      else:
        ext = ".jpg"
        getImg(data[6],fileName+ext)
      outfig = img2asciiart(fileName+ext,size,data[3] , data[4],fillvalues)
      deleteWithExt(ASCIITMPIMG+name,ext)

    return render_template(ARREBATOFOLDER+"img2asciiart.html",out = outfig,size = size ,defaultvalues = defaultvalues )
class gas():
  @app.route(GASWEBDIR+"user_register.html", methods = ['GET','POST'])
  def registergas():
    if request.method == 'POST':
      pwd = request.form["pwd"]
      pwd2 = request.form["pwd2"]
      if pwd == pwd2 :
        usr = request.form["usr"]
        db = dbInteracionGas(DBNAMEGAS)
        db.connect(GASLOGINTABLE)
        if db.userAvailable(usr,"usr") :
          encpwd = enPassowrdStrHex(pwd+usr) 
          db.saveUser(usr,enPassowrdStrHex(pwd))
          try:
            db.createUser(usr)
            session['loged'] = True
            session['user'] = usr
            session['encpwd'] = encpwd
          except db.userError():
            return "invalid user , please try with other username and password"   
    return render_template(GASFFOLDER+"user_register.html")
  @app.route(GASWEBDIR)
  def gasinfo():
    return render_template(GASFFOLDER+"gasinfo.html")
  @app.route(GASWEBDIR + "gas.html", methods=['GET', 'POST'])
  def gas():
      priceCol = "price"
      data = []
      db = dbInteracionGas(DBNAMEGAS)
      timenow = hoyminsStr()

      if not session.get('loged'):
          return render_template(GASFFOLDER+"gas_login.html")
      else:
          user = session.get('user')
          encpwd = session.get('encpwd')
          db.connect(TABLEGAS + user)
          item_id = db.getID()

          rows= db.getDataGas()
          ids=db.getsIdsGas()
          print(rows,"\n",ids)
          keys = len(DATANAMEGAS) * [encpwd]
          pricesum = 0
          decdata = []
          for i in range(len(rows)):
            decdata.append([])
            decdata[i].append(ids[i][0])
            for ii in range(len(rows[i])):
              decdata[i].append(decryptAES(eval(rows[i][ii]), encpwd))
            pricesum+=float(decdata[i][4])*float(decdata[i][5]) 

          try:
              priceavg = pricesum / len(rows)
          except ZeroDivisionError:
              priceavg = "no data"

          if request.method == 'POST':
              data = multrequest(DATANAMEGAS)
              print(data)
              encdata=list(map(lambda x: str(encryptAES(x, encpwd)), data))
              print(data,encdata)

              #dec=list(map(lambda x: decryptAES(x, encpwd), encdata))
              print(encdata)
              db.addGas(DATANAMEGAS, encdata)
              return redirect("/projects/GAS/gas.html")
          return render_template(GASFFOLDER+"gas.html", purchases=decdata, now=timenow, sum=pricesum, avg=priceavg)
  @app.route(GASWEBDIR+"gas_login.html", methods=['GET', 'POST'])
  def gaslogin(): 
    usr = request.form['username']
    pwd = request.form["password"]
    encpwd = enPassowrdStrHex(pwd+usr)
    protectpwd = enPassowrdStrHex(pwd)
    db = dbInteracionGas(DBNAMEGAS)
    db.connect(GASLOGINTABLE)
    if db.findUser(usr) and db.findPassword(protectpwd)  :
      session['loged'] = True
      session['user'] = usr
      session['encpwd'] = encpwd
      return redirect("/projects/GAS/gas.html")
    else:
      flash('wrong password!')
    return gas.gas()
  @app.route(GASWEBDIR+'actualisar<string:id>', methods = ['GET','POST'])
  def update_gas(id):
    user = session.get('user')
    db = dbInteracionGas(DBNAMEGAS)
    db.connect(TABLEGAS+user)
    key = session.get('encpwd')
    keys = len(DATANAMEGAS)*[key]
    if request.method == 'POST':
      data = multrequest(DATANAMEGAS)
      encdata = list(map(encryptAES , data, keys))
      encdata = list(map(str,encdata))
      del key,keys,data
      sentence = setUpdate(DATANAMEGAS,encdata)
      db.updateGas(sentence,id)
      flash(' Updated Successfully')
    return redirect(GASWEBDIR)
  @app.route(GASWEBDIR+'editar<string:id>', methods = ['POST', 'GET'])
  def get_gas(id):
    user = session.get('user')
    db = dbInteracionGas(DBNAMEGAS)
    db.connect(TABLEGAS+user)
    key = session.get('encpwd')
    keys = len(DATANAMEGAS)*[key]
    print()
    rows = db.getDataGasWhere("item_id",id)[0]
    print(rows)
    idData=[id]
    for i in range(len(rows)):
      idData.append(decryptAES(eval(rows[i]), key))
    print(idData)
    #idData = [id]+list(map(decryptAES,rows,keys))
    del key,keys , user , rows
    return render_template(GASFFOLDER+'gas_update.html', purchase = idData )
  @app.route(GASWEBDIR+"eliminar/<string:id>", methods = ['GET','POST'])
  def gassdelete(id):
    user = session.get('user')
    db = dbInteracionGas(DBNAMEGAS)
    db.connect(TABLEGAS+user)
    db.deleteWhere("item_id",id)
    #flash('you delete that')
    return redirect(GASWEBDIR)

class commap:
  if not os.path.isfile(COMMAPDATAPATH):
    writetxt(COMMAPDATAPATH,"name,contact,lat,lng")
  @app.route(COMMAPWEBDIR)
  def commapindex():
    return render_template(COMMAPFFOLDER+"index.html")
  @app.route(COMMAPWEBDIR+"map.html")
  def commapmapweb():
    return render_template(COMMAPMAPNAME)
  @app.route(COMMAPWEBDIR+"addData.html",methods=["GET","POST"])
  def commapaddData():
    if request.method=="POST":
     name=request.form["name"]
     contact=request.form["contact"]
     lat=request.form["lat"]
     lng=request.form["lng"]
     data=name+","+contact+","+lat+","+lng+"\n"
     writetxt(COMMAPDATAPATH,data,"a")
     df=pd.read_csv(COMMAPDATAPATH)
     genMap(df,"templates/"+COMMAPMAPNAME)
    return render_template(COMMAPFFOLDER+"addData.html")