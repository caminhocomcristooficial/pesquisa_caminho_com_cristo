#!/usr/bin/env python
# coding: utf-8

# In[4]:


from flask import Flask, request, render_template_string, redirect, url_for
import csv
from datetime import datetime
from pathlib import Path
import json
import urllib.request
app = Flask(__name__)

ARQUIVO = Path("respostas_pesquisa.csv")
URL_GOOGLE = "https://script.google.com/macros/s/AKfycbw6fpVlVmcuqcLcQgogSQBLXhmPTnaBytcwVpsZtG14NSJzvQyHMQZy_MnObulL5fmxWQ/exec"
# =========================================================
# PERGUNTAS
# =========================================================

PERGUNTAS = [
    {
        "icone": "💭",
        "titulo": "Qual foi sua primeira impressão ao ler o e-book?",
        "opcoes": [
            "Me tocou profundamente",
            "Foi uma leitura muito agradável",
            "Trouxe reflexões importantes",
            "Gostei, mas esperava algo diferente"
        ]
    },
    {
        "icone": "❤️",
        "titulo": "Depois da leitura, alguma mensagem ficou especialmente com você?",
        "opcoes": [
            "Sim, bastante",
            "Sim, algumas",
            "Pouco",
            "Ainda estou refletindo"
        ]
    },
    {
        "icone": "📖",
        "titulo": "Qual tema mais chamou sua atenção?",
        "opcoes": [
            "❤️ Amor",
            "🤍 Perdão",
            "🙏 Fé e oração",
            "🌱 Dificuldades e propósito",
            "✨ Esperança e vida eterna",
            "📚 Outro"
        ]
    },
    {
        # ÍCONE DE COMPARTILHAMENTO
        "icone": "↗",
        "titulo": "Você indicaria o “Caminho com Cristo” para alguém próximo?",
        "opcoes": [
            "Com certeza",
            "Provavelmente",
            "Talvez",
            "Não"
        ]
    }
]

# =========================================================
# HTML + CSS
# =========================================================

HTML = """
<!DOCTYPE html>
<html lang="pt-BR">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>Caminho com Cristo — Pesquisa</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    min-height: 100vh;

    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background:
        radial-gradient(
            circle at top,
            #21184b 0%,
            #0e1128 45%,
            #070914 100%
        );

    color: white;

    display: flex;

    justify-content: center;

    padding: 25px 15px;

}


/* CONTAINER */

.container {

    width: 100%;

    max-width: 650px;

}


/* MARCA */

.brand {

    text-align: center;

    color: #d9b65b;

    font-size: 13px;

    font-weight: bold;

    letter-spacing: 2px;

    text-transform: uppercase;

    margin-bottom: 15px;

}


/* PROGRESSO */

.progress-area {

    margin-bottom: 20px;

}

.progress-bar {

    width: 100%;

    height: 6px;

    background: rgba(255,255,255,.12);

    border-radius: 20px;

    overflow: hidden;

}

.progress {

    height: 100%;

    background:
        linear-gradient(
            90deg,
            #b98b2f,
            #f1d17a
        );

    border-radius: 20px;

    transition: width .4s ease;

}

.progress-text {

    text-align: right;

    color: #999;

    font-size: 12px;

    margin-top: 7px;

}


/* CARTÃO */

.card {

    background:
        rgba(255,255,255,.075);

    border:
        1px solid
        rgba(255,255,255,.14);

    border-radius: 25px;

    padding: 30px 25px;

    box-shadow:
        0 20px 60px
        rgba(0,0,0,.4);

    backdrop-filter: blur(12px);

    animation:
        aparecer .45s ease;

}


@keyframes aparecer {

    from {

        opacity: 0;

        transform:
            translateY(15px);

    }

    to {

        opacity: 1;

        transform:
            translateY(0);

    }

}


/* ÍCONE */

.icon {

    width: 78px;

    height: 78px;

    margin:
        0 auto 20px;

    border-radius: 23px;

    display: flex;

    align-items: center;

    justify-content: center;

    font-size: 37px;

    background:
        rgba(217,182,91,.12);

    border:
        1px solid
        rgba(217,182,91,.30);

    color: #f1d17a;

}


/* ÍCONE COMPARTILHAR */

.share-icon {

    font-family: Arial, sans-serif;

    font-size: 48px;

    font-weight: normal;

}


/* TÍTULO */

h1 {

    text-align: center;

    font-size: 25px;

    line-height: 1.35;

    margin:
        0 0 25px;

}


/* INTRODUÇÃO */

.intro {

    text-align: center;

}

.intro h1 {

    font-size: 29px;

}

.intro p {

    color: #c9c9d2;

    line-height: 1.65;

    font-size: 16px;

}


/* OPÇÕES */

.option {

    display: block;

    margin: 11px 0;

    cursor: pointer;

}

.option input {

    display: none;

}

.option span {

    display: block;

    padding: 16px;

    border:
        1px solid
        rgba(255,255,255,.14);

    border-radius: 15px;

    background:
        rgba(255,255,255,.045);

    color: #eeeeee;

    transition:
        all .2s ease;

}

.option span:hover {

    border-color: #d9b65b;

    transform:
        translateY(-1px);

}

.option input:checked + span {

    background:
        rgba(217,182,91,.16);

    border-color:
        #d9b65b;

    box-shadow:
        0 0 0 1px
        rgba(217,182,91,.15);

}


/* TEXTAREA */

textarea {

    width: 100%;

    min-height: 145px;

    resize: vertical;

    padding: 17px;

    border-radius: 15px;

    border:
        1px solid
        rgba(255,255,255,.14);

    background:
        rgba(255,255,255,.05);

    color: white;

    font-size: 16px;

    outline: none;

}

textarea:focus {

    border-color:
        #d9b65b;

}

textarea::placeholder {

    color: #999;

}


/* BOTÃO */

button {

    width: 100%;

    margin-top: 20px;

    padding: 17px;

    border: none;

    border-radius: 15px;

    background:
        linear-gradient(
            135deg,
            #b98b2f,
            #e5c66f
        );

    color: #17120a;

    font-size: 16px;

    font-weight: bold;

    cursor: pointer;

    transition:
        all .2s ease;

}

button:hover {

    filter: brightness(1.08);

    transform:
        translateY(-1px);

}


/* RODAPÉ */

.footer {

    text-align: center;

    color: #858592;

    font-size: 12px;

    margin-top: 18px;

}


/* MOBILE */

@media(max-width:500px) {

    .card {

        padding:
            25px 18px;

    }

    h1 {

        font-size: 22px;

    }

    .intro h1 {

        font-size: 26px;

    }

}

</style>

</head>


<body>

<div class="container">


<div class="brand">

Caminho com Cristo

</div>


{% if etapa > 0 and etapa < 6 %}

<div class="progress-area">

<div class="progress-bar">

<div
class="progress"
style="width: {{ progresso }}%;">
</div>

</div>

<div class="progress-text">

{{ etapa }} de 5

</div>

</div>

{% endif %}


<div class="card">


{% if etapa == 0 %}


<div class="icon">

✨

</div>


<div class="intro">

<h1>

Sua jornada também faz parte deste caminho

</h1>


<p>

Você acabou de conhecer o
<b>Caminho com Cristo</b>,
e sua opinião é muito importante para nós.

</p>


<p>

Leva menos de 2 minutos.

</p>


<form method="POST">

<input
type="hidden"
name="etapa"
value="1">

<button>

COMEÇAR PESQUISA →

</button>

</form>

</div>


{% elif etapa >= 1 and etapa <= 4 %}


<div
class="icon
{% if etapa == 4 %}
share-icon
{% endif %}">

{{ pergunta.icone }}

</div>


<h1>

{{ pergunta.titulo }}

</h1>


<form method="POST">

<input
type="hidden"
name="etapa"
value="{{ etapa + 1 }}">


{% for opcao in pergunta.opcoes %}

<label class="option">

<input
type="radio"
name="resposta"
value="{{ opcao }}"
required>

<span>

{{ opcao }}

</span>

</label>

{% endfor %}


<button>

CONTINUAR →

</button>

</form>


{% elif etapa == 5 %}


<div class="icon">

💬

</div>


<h1>

Se pudesse deixar uma mensagem para o autor,
o que diria?

</h1>


<form method="POST">

<input
type="hidden"
name="etapa"
value="6">


<textarea
name="resposta"
placeholder="Escreva livremente. Pode ser apenas uma frase."
required></textarea>


<button>

ENVIAR MINHA MENSAGEM →

</button>

</form>


{% else %}


<div class="icon">

🙌

</div>


<div class="intro">

<h1>

Obrigado por compartilhar sua experiência!

</h1>


<p>

Cada resposta ajuda o
<b>Caminho com Cristo</b>
a melhorar e a servir melhor seus leitores.

</p>


<p>

Que Deus abençoe sua caminhada. ❤️

</p>


<p>

<b>— Ricardo Sousa da Silva</b>

<br>

Autor de Caminho com Cristo

</p>

</div>


{% endif %}


</div>


<div class="footer">

Sua opinião é muito importante para nós.

</div>


</div>

</body>

</html>
"""


# =========================================================
# SALVAR RESPOSTAS
# =========================================================

def salvar_respostas(respostas):

    arquivo_novo = not ARQUIVO.exists()

    with open(
        ARQUIVO,
        "a",
        newline="",
        encoding="utf-8"
    ) as arquivo:

        escritor = csv.writer(arquivo)

        if arquivo_novo:

            escritor.writerow([
                "Data",
                "Primeira impressão",
                "Mensagem marcante",
                "Tema",
                "Indicaria",
                "Mensagem para o autor"
            ])

        escritor.writerow([
            datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S"
            ),
            respostas.get("q1", ""),
            respostas.get("q2", ""),
            respostas.get("q3", ""),
            respostas.get("q4", ""),
            respostas.get("q5", "")
        ])
    dados_google = {
        "primeira_impressao": respostas.get("q1", ""),
        "mensagem_marcante": respostas.get("q2", ""),
        "tema": respostas.get("q3", ""),
        "indicaria": respostas.get("q4", ""),
        "mensagem_autor": respostas.get("q5", "")
    }

    requisicao = urllib.request.Request(
        URL_GOOGLE,
        data=json.dumps(dados_google).encode("utf-8"),
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        urllib.request.urlopen(
            requisicao,
            timeout=10
        )
    except Exception as erro:
        print("Erro ao enviar para Google Sheets:", erro)

# =========================================================
# PÁGINA
# =========================================================

@app.route("/", methods=["GET", "POST"])
def pesquisa():

    if request.method == "GET":

        return render_template_string(
            HTML,
            etapa=0,
            pergunta=None,
            progresso=0
        )


    etapa = int(
        request.form.get(
            "etapa",
            1
        )
    )


    # PRIMEIRA TELA
    if etapa == 1:

        return render_template_string(
            HTML,
            etapa=1,
            pergunta=PERGUNTAS[0],
            progresso=20
        )


    # PERGUNTAS 1 A 4
    if 2 <= etapa <= 5:

        respostas = {}

        # Recupera as respostas que foram enviadas
        for i in range(1, etapa):

            respostas[f"q{i}"] = request.form.get(
                f"q{i}",
                ""
            )

        # Guarda a resposta anterior
        resposta = request.form.get(
            "resposta",
            ""
        )

        respostas[f"q{etapa-1}"] = resposta


        # Envia os dados através dos campos ocultos
        campos = ""

        for chave, valor in respostas.items():

            campos += f'''
            <input
                type="hidden"
                name="{chave}"
                value="{valor}">
            '''


        pagina = HTML.replace(
            '<input type="hidden" name="etapa" value="{{ etapa + 1 }}">',
            '<input type="hidden" name="etapa" value="{{ etapa + 1 }}">' + campos
        )


        return render_template_string(
            pagina,
            etapa=etapa,
            pergunta=PERGUNTAS[etapa-1] if etapa <= 4 else None,
            progresso=etapa * 20
        )


    # FINAL — SALVAR
    if etapa == 6:

        respostas = {}

        for i in range(1, 5):

            respostas[f"q{i}"] = request.form.get(
                f"q{i}",
                ""
            )

        respostas["q5"] = request.form.get(
            "resposta",
            ""
        )


        salvar_respostas(respostas)


        return render_template_string(
            HTML,
            etapa=6,
            pergunta=None,
            progresso=100
        )


if __name__ == "__main__":

    print()
    print("=" * 50)
    print(" CAMINHO COM CRISTO")
    print(" PESQUISA DE EXPERIÊNCIA")
    print("=" * 50)
    print()
    print("A pesquisa está funcionando.")
    print()
    print("Abra no navegador:")
    print("http://127.0.0.1:5000")
    print()
    print("As respostas serão salvas em:")
    print("respostas_pesquisa.csv")
    print()
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )

