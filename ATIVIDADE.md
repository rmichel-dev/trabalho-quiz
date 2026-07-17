# 📝 Atividade de Recuperação — Questionário Online

O app `quiz` deste projeto é um questionário online: o aluno informa o nome,
responde **10 questões sorteadas** da base e no final baixa um **PDF com as
respostas que marcou**, para enviar ao professor.

A base tem dois tipos de questão:

- **Objetivas** (múltipla escolha A–D);
- **Discursivas** (você digita a resposta).

**Toda a correção é feita pelo professor a partir do PDF** — o sistema não
mostra quais respostas estão certas.

O sistema **roda sem apresentar nenhum erro**… mas está se comportando de
forma estranha. Foram relatados problemas pelos usuários, e a sua missão é
**encontrar e corrigir os defeitos**.

## Como rodar o projeto

```bash
# 1. Crie o ambiente virtual e instale as dependências
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Prepare o banco e carregue as questões
python manage.py migrate
python manage.py loaddata questoes_exemplo questoes_prova

# 3. Rode o servidor
python manage.py runserver
```

Acesse: <http://127.0.0.1:8000/>

## Reclamações dos usuários 🐞

> "Marquei a alternativa D em todas as questões (e escrevi um textão nas
> discursivas), mas no resultado apareceu outra coisa!"

> "Respondi as 10 questões, mas o resultado diz que só respondi uma…"

> "Fiz a prova três vezes e caíram **sempre as mesmas questões, na mesma
> ordem**. Cadê o sorteio?"

## O que deve funcionar quando você terminar ✅

1. A resposta que o aluno marca (ou digita) é exatamente a que fica salva
   no banco.
2. Cada resposta é salva na **sua** questão (as 10 aparecem respondidas no final).
3. Cada prova sorteia 10 questões **aleatórias** da base (provas diferentes
   tendem a ter questões/ordens diferentes — e as discursivas do professor
   precisam aparecer!).
4. O PDF traz as 10 questões com **exatamente** o que o aluno marcou ou
   digitou em cada uma.

## Dicas 💡

- Os defeitos estão todos em **`quiz/views.py`** — leia o código com atenção.
- O Django Admin (<http://127.0.0.1:8000/admin/>) mostra o que foi salvo no
  banco: cadastre um superusuário (`python manage.py createsuperuser`) e
  abra uma Prova para ver os itens e as respostas gravadas.
- Teste como um usuário de verdade: faça a prova marcando alternativas
  variadas e compare com o que aparece no resultado.

## Entrega

- O código corrigido (com commit para cada bug encontrado, explicando o
  defeito na mensagem do commit).
- O PDF de uma prova completa gerado pelo sistema já corrigido.
