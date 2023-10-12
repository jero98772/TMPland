from flask import Flask, render_template
app = Flask(__name__)
class blogs():
	@app.route("/blog/Micosa/german.html")
	def Micosagerman():
		return render_template("blog/Micosa/german.html")
	@app.route("/blog/Micosa/Spanish.html")
	def MicosaSpanish():
		return render_template("blog/Micosa/Spanish.html")