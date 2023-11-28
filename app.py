from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import re
import ply.yacc as yacc
import ply.lex as lex

app = Flask(__name__, template_folder='templates', static_folder='static')
Bootstrap(app)
moment = Moment(app)

registros = []

# Definición de tokens
tokens = (
    'NUMERO',
    'INGRESO',
    'EGRESO',
    'COMANDO_INVALIDO',
)

# Expresiones regulares para tokens simples
t_NUMERO = r'\d+(\.\d+)?'
t_INGRESO = r'ingreso'
t_EGRESO = r'egreso'
t_COMANDO_INVALIDO = r'.+'

# Ignorar caracteres como espacios y saltos de línea
t_ignore = ' \t\n'



# Funciones de manejo de tokens
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()

# Definición de la gramática
def p_comando_ingreso_egreso(p):
    '''
    comando : INGRESO NUMERO
            | EGRESO NUMERO
    '''
    tipo = 'ingreso' if p[1] == 'ingreso' else 'egreso'
    monto = float(p[2])
    registros.append({'tipo': tipo, 'monto': monto})

def p_comando_invalido(p):
    'comando : COMANDO_INVALIDO'
    print(f"Comando inválido: {p[1]}")

def p_error(p):
    print("Error de sintaxis")

parser = yacc.yacc()

@app.context_processor
def inject_today():
    return {'fecha_actual': datetime.now().strftime('%Y-%m-%d')}

@app.route('/')
def index():
    ingresos = sum(registro['monto'] for registro in registros if registro['tipo'] == 'ingreso')
    egresos = sum(registro['monto'] for registro in registros if registro['tipo'] == 'egreso')

    return render_template('index_lujoso.html', registros=registros, ingresos=ingresos, egresos=egresos)

@app.route('/ingresar_ingreso', methods=['GET', 'POST'])
def ingresar_ingreso():
    if request.method == 'POST':
        comando = request.form['comando']
        parser.parse(comando)

    return render_template('ingresar_ingreso.html')

@app.route('/ingresar_egreso', methods=['GET', 'POST'])
def ingresar_egreso():
    if request.method == 'POST':
        comando = request.form['comando']
        parser.parse(comando)

    return render_template('ingresar_egreso.html')

if __name__ == '__main__':
    app.run(debug=True)
