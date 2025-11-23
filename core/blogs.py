from flask import Flask, render_template
app = Flask(__name__)
class blogs():
	@app.route("/blog/proyectos.html")
	def proyectos():
		return render_template("blog/proyectos.html")
	@app.route("/blog/blogmenu.html")
	def blogmenu():
		return render_template("blog/blogmenu.html")
	@app.route("/blog/blog1.html")
	def blog1():
		return render_template("blog/blog1.html")
	@app.route("/blog/manifest.html")
	def manifest():
		return render_template("blog/manifest.html")
	@app.route("/blog/GEtoEN/english.html")
	def GEtoENenglish():
		return render_template("blog/GEtoEN/english.html")
	@app.route("/blog/GEtoEN/German.html")
	def GEtoENGerman():
		return render_template("blog/GEtoEN/German.html")
	@app.route("/blog/blog6.html")
	def blog6():
		return render_template("blog/blog6.html")
	@app.route("/blog/blog5.html")
	def blog5():
		return render_template("blog/blog5.html")
	@app.route("/blog/blog3.html")
	def blog3():
		return render_template("blog/blog3.html")
	@app.route("/blog/blog2.html")
	def blog2():
		return render_template("blog/blog2.html")
	@app.route("/blog/blog4.html")
	def blog4():
		return render_template("blog/blog4.html")
	@app.route("/blog/blog7.html")
	def blog7():
		return render_template("blog/blog7.html")
	@app.route("/blog/story.html")
	def story():
		return render_template("blog/story.html")
	@app.route("/blog/LearningGerman/English.html")
	def LearningGermanEnglish():
		return render_template("blog/LearningGerman/English.html")
	@app.route("/blog/LearningGerman/german.html")
	def LearningGermangerman():
		return render_template("blog/LearningGerman/german.html")
	@app.route("/blog/Technotes.html")
	def Technotes():
		return render_template("blog/Technotes.html")