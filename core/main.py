#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
TMPland - 2023 - por jero98772
TMPland - 2023 - by jero98772
"""
from .constants import *
from flask import Flask, render_template ,request,session,redirect,send_file,send_from_directory
from .tools.webutils import *
from .tools.tools import *
from core.tools.dbInteracion import dbInteraciontt
from .projects import *

class webpage:
	app.secret_key = TOKEN
	print("\n* Configuration token:\n"+TOKEN+"\n","go to :\n\n\tlocalhost:9600"+BLOGWEBDIR+TOKEN+"/\n\nto get acces to configuration , rember your token is\n\n\t"+TOKEN,"\n")
	@app.route("/")
	@app.route("/index/")
	@app.route(PROJECTSWEBDIR+"B-FeelLog")
	def index():
		projects=readtxtR(PROJECTSNAMEFILE)
		return render_template("index.html",projects=projects)

	#def index():#change it with a map
	"""
	https://main.jero98772.page/blog/blogmenu.html
	"""

	@app.route(BLOGINDEX)
	def blogmain():
		session["author"] = AUTHOR
		updateBlog(BLOGSFILES,BLOGFILE)
		return render_template("config/bloglist.html", url= BLOGWEBDIR,topics = sorted(BLOGS), name = AUTHOR )


	@app.route(BLOGWEBDIR+"/config.html")
	def config():
		return render_template("config/configmenu.html")
		
	@app.route(BLOGWEBDIR+"/add.html",methods=['POST','GET'])	
	def add():
		if not session.get("loged"):
			return "error: you cannot perform this operation unless you are root."
		else:
			if request.method == "POST":
				txtp =request.form["txtp"]
				txtq = request.form["txtq"]
				txtid = request.form["id"]
				name = request.form["destiantion"]
				if os.path.isdir(BLOGPATH+name):#translate because is dir 
					files = os.listdir(BLOGPATH+name)
					for file in files:
						if file[0].isupper():
							mainLangue = file[0].lower()+file[1:-5]
							content = doHtml(txtp,txtq,txtid,AUTHOR)
							writeblog(BLOGPATH+name+"/"+file,content)	
						else:
							transalateTo = file[:-5]
					else:
						print(mainLangue,transalateTo)
						if mainLangue in SUPORTEDLANGUAGESSEAMLESS:
							print("test")
							txtp_translated = translateseamless(txtp,SUPORTEDLANGUAGESSEAMLESS[mainLangue],SUPORTEDLANGUAGESSEAMLESS[transalateTo])
							txtq_translated = translateseamless(txtq,SUPORTEDLANGUAGESSEAMLESS[mainLangue],SUPORTEDLANGUAGESSEAMLESS[transalateTo])
						else:
							txtp_translated = webTranslate(txtp,mainLangue,transalateTo)
							txtq_translated = webTranslate(txtq,mainLangue,transalateTo)
						content = doHtml(txtp_translated,txtq_translated,txtid,AUTHOR)
						writeblog(BLOGPATH+name+"/"+transalateTo+".html",content)
				else:
					content = doHtml(txtp,txtq,txtid,AUTHOR)
					writeblog(BLOGPATH+name+".html",content)
			return render_template("config/addData.html",blogs = blogsNames(BLOGPATH))
	@app.route(BLOGWEBDIR+"/createNewTopic.html",methods=['POST','GET'])	
	def CreateNewTopic():
		if not session.get("loged"):
			return "error: you cannot perform this operation unless you are root."
		else:
			msg = ""
			if request.method == "POST":
				name = str(request.form["name"])
				nameIsOk ,errormsg = clearName(name,EXCLUDEDCHARACTER,BLOGS)
				if nameIsOk:
					name = changeName(name)
				try :
					translateTo = request.form["translate_to"]
				except:
					translateTo = SUPORTEDLANGUAGES[0]
				translateFrom = request.form["translate_from"]
				if translateTo == translateFrom:
					msg = "you can not translate from "+translateTo+" to "+translateFrom
				if SUPORTEDLANGUAGES[0] == translateTo or translateTo == translateFrom:
					msg = " was create a topic without trasnlate option"
					writeblog(BLOGPATH+name+".html","")
				else:
					os.mkdir(BLOGPATH+name)
					writeblog(BLOGPATH+name+"/"+translateFrom[0].upper()+translateFrom[1:]+".html","")
					writeblog(BLOGPATH+name+"/"+translateTo+".html","")
			return render_template("config/createNewTopic.html" ,languages = SUPORTEDLANGUAGES, msg = msg)
	@app.route(BLOGWEBDIR+"/token.html",methods=['POST','GET'])
	def token():
		if not session.get("loged"):
			return "error: you cannot perform this operation unless you are root.\n please get loged with your token!!"
		else:
			if request.method == "POST":
				if request.form.get('new Token'):
					newToken = genToken()
					writeTxt(TOKENPATH,newToken,"w")
					session["loged"] = False
					return "you new Token is :\n\t"+newToken
				if request.form.get('custom Token'):
					writeTxt(TOKENPATH,request.form['customTokenValue'],"w")
					session["loged"] = False
					return "remember, save your token"
				return redirect(INDEX)
			return render_template("config/token.html")
	@app.route(BLOGWEBDIR+"/author.html",methods=['POST','GET'])
	def author():
		if not session.get("loged"):
			return "error: you cannot perform this operation unless you are root.\n please get loged with your token!!"
		else:
			if request.method == "POST":
				newAuthor = request.form['author']
				upadateAuthor(AUTHOR,newAuthor,TEMPLATE)
				writeTxt(AUTHORFILE,newAuthor,"w")
				return redirect(INDEX)
			return render_template("config/author.html",defautlAuthor = AUTHOR)
	@app.route(BLOGWEBDIR+"/thisSite.html",methods=['POST','GET'])
	def thisSite():
		if not session.get("loged"):
			return "error: you cannot perform this operation unless you are root.\n please get loged with your token!!"
		else:
			if request.method == "POST":
				whatis = request.form['this']
				upadateAuthor(USE,whatis,TEMPLATE)
				writeTxt(WHATISFILE,whatis,"w")
				return redirect(INDEX)
			return render_template("config/thisSite.html",defautlUse = USE)

	@app.route(BLOGWEBDIR+TOKEN+"/",methods=['POST','GET'])
	def trueLoged():
		msg = ""
		if request.method == "POST":
			if request.form["key"] == TOKEN:
				session["loged"] = True
				return redirect(BLOGWEBDIR+"token.html")
			else:
				msg = "Invalid token"
		return render_template("config/addkey.html",error=msg)
	@app.route(BLOGWEBDIR+"/deleteFiles.html",methods = ["POST","GET"])
	def deleteFiles():		
		msg = ""
		if request.method == "POST":
			deletechecks = request.form.getlist("delete")
			deleteAndMove(deletechecks,BLOGPATH,BLOGS) 
			deletemsg = str(deletechecks)[2:-2]
			msg =  "file removed are :"+deletemsg
		return render_template("config/deleteFiles.html",blogs = BLOGS,msg = msg)

##### test webterminal

	@app.route("/tmxhost.html")
	def tmxhost():
		return redirect("127.0.0.1")	

