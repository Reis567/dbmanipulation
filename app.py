from flask import Flask, render_template, request , redirect , url_for , flash 
import urllib.request, json
from flask_sqlalchemy import SQLAlchemy 



app = Flask(__name__)
app.secret_key = 'secret_key_31032023'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cursos.sqlite3"
db = SQLAlchemy(app)


frutas = []
registros = []

class cursos(db.Model):
	id = db.Column(db.Integer , primary_key = True)
	nome = db.Column(db.String(50) )
	descricao = db.Column(db.String(100))
	ch = db.Column(db.Integer)

	def __init__(self , nome , descricao , ch):
		self.nome = nome
		self.descricao = descricao
		self.ch = ch


@app.route('/')
def lista_cursos():
	page = request.args.get('page' , 1 , type=int)
	per_page = 4
	todos_cursos = cursos.query.paginate(page=page,per_page=per_page)
	return render_template('cursos.html' , cursos=todos_cursos)




@app.route('/cria_curso' , methods = ['GET', 'POST'])
def cria_curso():
	nome = request.form.get('nome')
	descricao = request.form.get('descricao')
	ch = request.form.get('ch')

	if request.method == 'POST':
		if not nome or not descricao or not ch:
			flash("Preencha todos os campos", "error")
		else:
			curso = cursos(nome , descricao , ch)
			db.session.add(curso)
			db.session.commit()
			return redirect(url_for('lista_cursos'))
	
	return render_template('novo_curso.html')


@app.route('/<int:id>/atualiza_curso', methods=['GET', 'POST'])
def atualiza_curso(id):
	curso = cursos.query.filter_by(id=id).first()
	if request.method == 'POST':
		nome = request.form["nome"]
		descricao = request.form["descricao"]
		ch = request.form["ch"]

		cursos.query.filter_by(id=id).update({"nome":nome , "descricao":descricao , "ch":ch})
		db.session.commit()
		return redirect(url_for('lista_cursos'))
	return render_template('atualiza_curso.html', curso = curso)

@app.route('/<int:id>/remove_curso')
def remove_curso(id):
	curso = cursos.query.filter_by(id=id).first()
	db.session.delete(curso)
	db.session.commit()
	return redirect(url_for('lista_cursos'))




if __name__ == "__main__":
	with app.app_context():
		db.create_all()	
	app.run(debug=True)