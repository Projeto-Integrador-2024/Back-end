# DOCUMENTAÇÃO DA API PPE (Poral Pesquisa e Extensão)
Descrição: Esta API permite gerenciar Alunos, Professores e vagas de Pesquisa/Extensão, incluindo criar, listar, atualizar e deletar instâncias.

## ENDPOINTS:

**ENDPOINTS DE ALUNOS:**

GET(Todos): 
    rota:/ALUNO/GET_ALL

    Descrição: Retorna todos os alunos.

    *Parâmetros: Nenhum.

    *Resposta de Sucesso:
    json

    [
        {
        "ra": a0000001,
        "nome": "nome_teste",
        "periodo": 2,
        "cpf": "00000000000",
        },
        {
        "ra": a0000002,
        "nome": "nome_teste",
        "periodo": "descricao_teste",
        "cpf": "00000000000",
        }
    ]

    Código de Status: 200 OK

GET(específico): 
    rota:/ALUNO/GET_BY_RA

    Descrição: Retorna aluno pelo RA.

    *Parâmetros:
    json

    {
	    "ra":"a0000001"
    }

    *Resposta de Sucesso:
    json

    {
    "ra": a0000001,
    "nome": "nome_teste",
    "periodo": 2,
    "cpf": "00000000000",
    }

    Código de Status: 200 OK

POST: 
    rota:/VAGA/CREATE

    Descrição: Cria um novo aluno.

    *Parâmetros:
    json

    {
    "nome": "string",
    "periodo": "string",
    "cpf": 0
    }

    Resposta de Sucesso:
    json

    {
    "message": "Vaga criada com sucesso"
    }

    Código de Status: 201 Created


## Modelos:
Aluno:

    ID: Inteiro, chave primária

    Nome: Texto, obrigatório

    Descrição: Texto, obrigatório

    Bolsa: Inteiro, obrigatório (0 = sem bolsa, 1 = possui bolsa)

    Tipo: Texto, obrigatório (Pesquisa ou Extensão)
