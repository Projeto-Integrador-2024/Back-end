![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
[![GitHub license](https://img.shields.io/github/license/Naereen/StrapDown.js.svg)](https://github.com/Naereen/StrapDown.js/blob/master/LICENSE)

# API PPE (Portal Pesquisa e Extensão):
**Descrição:** API criada em **Flask** para a disciplina Projeto Integrador do curso de Ciências da Computação da Universidade Tecnológica do Paraná (Ano/Semestre: 2024/2).<br> A API permite gerenciar Alunos, Professores e vagas de Pesquisa/Extensão, incluindo criar, listar, atualizar e deletar instâncias.

## Pré Requisitos para usar a API:
* Python 3
## Como Executar:
instale as dependencias necessárias com o comando:   
```bash
pip install -r requirements.txt
```
inicie a API com o comando (Linux/MacOS):  
```bash
python3 app.py
```
ou (Windows):  
```bash
python app.py
```
Para encerrar a API digite CTR+C no terminal 

## DOCUMENTAÇÃO:
A documentação está disponível, basta clicar <a href="https://documentacaoppe.netlify.app/" target="_blank">AQUI</a>

## Estrutura do projeto:
.<br>
├── app.py <br>
├── blueprints<br>
│   ├── Aluno<br>
│   │   ├── model.py<br>
│   │   └── routes.py<br>
│   ├── Professor<br>
│   │   ├── model.py<br>
│   │   └── routes.py<br>
│   └── Vagas<br>
│       ├── model.py<br>
│       └── routes.py<br>
├── extensions.py<br>
├── instance<br>
│   └── SISUNI.db<br>
├── migrations<br>
│   ├── alembic.ini<br>
│   ├── env.py<br>
│   ├── README<br>
│   ├── script.py.mako<br>
│   └── versions<br>
│       └── //Versões do Banco de Dados//<br>
├── README.md<br>
└── requirements.txt<br>


