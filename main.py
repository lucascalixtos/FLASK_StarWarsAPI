from flask import Flask, render_template
import requests, json, math, decimal

app = Flask(__name__)

port = 5000

def RealizaRequisicaoPersonagens(pagina):
    url = "https://swapi.dev/api/people?page=" + str(pagina)
    requisicao = requests.get(url)
    resultado = json.loads(requisicao.text)
    #print(parse['results'])
    return resultado

def OrdenarPersonagens(pagina, atributo):
    url = "https://swapi.dev/api/people?page=" + str(pagina)
    requisicao = requests.get(url)
    resultado = json.loads(requisicao.text)

    jsonFinal = {"count": resultado["count"],"results":[]}
    jsonFinal = json.dumps(jsonFinal)
    jsonFinal = json.loads(jsonFinal)

    for item in resultado['results']:
        name = item['name']
        if(str(item['mass']).lower() == 'unknown'):
            item['mass'] = 0
        if(str(item['height']).lower() == 'unknown'):
            item['height'] = 0

        jsonFinal['results'].append({'name': item['name'], 'gender': item['gender'], 'mass': str(item['mass']).replace(',',''), 'height': str(item['height']).replace(',','')})

    if(atributo == 'name' or atributo == 'gender'):
        jsonFinal["results"] = sorted(jsonFinal['results'], key=lambda x : x[atributo])
    else:
        jsonFinal["results"] = sorted(jsonFinal['results'], key=lambda x : float(x[atributo]), reverse=True)
        

    return jsonFinal

def CalculaScore(hyperdrive_rating, cost_in_credits):
    if(hyperdrive_rating == 'unknown' or cost_in_credits == 'unknown'):
        total = 0
    else:
        hyperdrive = float(hyperdrive_rating)
        cost = float(cost_in_credits)
        total = cost/hyperdrive
    
     
    return  total

def RealizarRequisicaoNaves():
    url = "https://swapi.dev/api/starships/"
    requisicao = requests.get(url)
    resultado = json.loads(requisicao.text)
    count = math.ceil(int(resultado['count'])/10)
    jsonFinal = {"item":[]}
    jsonAppend = json.dumps(jsonFinal)
    jsonAppend = json.loads(jsonAppend)

    #print(resultado)

    for item in resultado['results']:
        name = item['name']
        score = CalculaScore(item['hyperdrive_rating'], item['cost_in_credits'])
        jsonAppend['item'].append({'name': name, 'hyper': item['hyperdrive_rating'], 'cost': item['cost_in_credits'], 'score': score})

    while(count > 1):
        url = "https://swapi.dev/api/starships/?page=" + str(count)
        requisicao = requests.get(url)
        resultado = json.loads(requisicao.text)
        
        for item in resultado['results']:
            name = item['name']
            score = CalculaScore(item['hyperdrive_rating'], item['cost_in_credits'])
            jsonAppend['item'].append({'name': name, 'hyper': item['hyperdrive_rating'], 'cost': item['cost_in_credits'], 'score': score})

        count = count - 1


    jsonAppend["item"] = sorted(jsonAppend['item'], key=lambda x : int(x['score']), reverse=True)


    return jsonAppend

def RealizarRequisicaoDetalhar(nome):
    url = 'https://swapi.dev/api/people/?search=' + nome
    requisicao = requests.get(url)
    resultado = json.loads(requisicao.text)


    for item in resultado['results']:
        nome = item["name"]
        peso = item['mass']
        altura = item['height']
        cabelo = item['hair_color']
        pele = item['skin_color']
        olhos = item['eye_color']
        nascimento = item['birth_year']
        genero = item['gender']
        filmesUrl = item['films']
        planetaUrl = item['homeworld']
        veiculosUrl = item['vehicles']
        navesUrl = item['starships']

    planeta = requests.get(planetaUrl)
    planeta = json.loads(planeta.text)

    jsonFinal = {"name": nome,"mass": peso, "height": altura, "hair_color": cabelo, "skin_color": pele, "eye_color": olhos, "birth_year": nascimento,"gender": genero, "homeworld": planeta["name"],"films":[],"vehicles":[],"starships":[]}
    jsonFinal = json.dumps(jsonFinal)
    jsonFinal = json.loads(jsonFinal)

    for item in filmesUrl:
        objeto = requests.get(item)
        objeto = json.loads(objeto.text)
        jsonFinal['films'].append(objeto['title'])
    
    for item in veiculosUrl:
        objeto = requests.get(item)
        objeto = json.loads(objeto.text)
        jsonFinal['vehicles'].append(objeto['name'])

    for item in navesUrl:
        objeto = requests.get(item)
        objeto = json.loads(objeto.text)
        jsonFinal['starships'].append(objeto['name'])
    
    print(jsonFinal)

    return jsonFinal

@app.route("/")
def home():
    return render_template("index.html")



@app.route("/personagens", defaults={'pagina': 1,'atributo': 'null'})
@app.route("/personagens/<pagina>", defaults={'atributo': 'null'})
@app.route("/personagens/<pagina>/order/<atributo>")
def personagens(pagina, atributo):
    if(atributo == 'null'):
        conteudo = RealizaRequisicaoPersonagens(pagina)
    else:
        conteudo = OrdenarPersonagens(pagina, atributo)
    return render_template("personagens.html", conteudo=conteudo, pagina_atual=pagina)

@app.route("/naves")
def naves():
    conteudo = RealizarRequisicaoNaves()
    return render_template("naves.html", conteudo = conteudo)

    
@app.route("/detalhar/<nome>")
def detalhar(nome):
    conteudo = RealizarRequisicaoDetalhar(nome)
    print(conteudo)
    return render_template("detalhar.html", conteudo = conteudo)

     
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port)
