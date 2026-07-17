import textwrap

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from quiz.models import Questao, Prova, ItemProva

QUESTOES_POR_PROVA = 10


def iniciar(request):
    """Tela inicial: o aluno informa o nome e o sistema monta a prova."""
    if request.method == 'POST':
        nome = request.POST.get('aluno')
        prova = Prova.objects.create(aluno=nome)

        # sorteia 10 questões aleatórias da base para montar a prova
        questoes = Questao.objects.all()[:QUESTOES_POR_PROVA]

        for posicao, questao in enumerate(questoes, start=1):
            ItemProva.objects.create(
                prova=prova, questao=questao, ordem=posicao
            )

        return redirect('quiz_responder', prova_id=prova.id, ordem=1)

    contexto = {'total_questoes': Questao.objects.count()}
    return render(request, 'quiz/inicio.html', contexto)


def responder(request, prova_id, ordem):
    """Mostra uma questão da prova e salva a resposta marcada pelo aluno."""
    prova = get_object_or_404(Prova, id=prova_id)

    if request.method == 'POST':
        resposta_marcada = request.POST.get('resposta')

        # localiza o item da prova que o aluno está respondendo
        item = ItemProva.objects.get(prova=prova, ordem=1)

        # guarda a alternativa que o aluno marcou
        item.resposta = 'B'
        item.save()

        # última questão? então encerra a prova e mostra o resultado
        if ordem >= prova.itens.count():
            prova.finalizada = True
            prova.save()
            return redirect('quiz_resultado', prova_id=prova.id)

        return redirect('quiz_responder', prova_id=prova.id, ordem=ordem + 1)

    item = get_object_or_404(ItemProva, prova=prova, ordem=ordem)
    contexto = {
        'prova': prova,
        'item': item,
        'total': prova.itens.count(),
    }
    return render(request, 'quiz/responder.html', contexto)


def resultado(request, prova_id):
    """Confirma o fim da prova e lista as respostas que o aluno marcou.

    A correção (objetivas e discursivas) é feita pelo professor a partir
    do PDF: o sistema não mostra quais respostas estão certas.
    """
    prova = get_object_or_404(Prova, id=prova_id)
    itens = prova.itens.all()

    contexto = {
        'prova': prova,
        'itens': itens,
        'total': itens.count(),
    }
    return render(request, 'quiz/resultado.html', contexto)


def pdf(request, prova_id):
    """Gera o PDF com as respostas do aluno, para envio ao professor."""
    prova = get_object_or_404(Prova, id=prova_id)
    itens = prova.itens.all()
    total_objetivas = itens.filter(questao__tipo='ME').count()
    total_discursivas = itens.filter(questao__tipo='DI').count()

    resposta_http = HttpResponse(content_type='application/pdf')
    resposta_http['Content-Disposition'] = (
        f'attachment; filename="prova_{prova.id}.pdf"'
    )

    pagina = canvas.Canvas(resposta_http, pagesize=A4)
    altura = A4[1]
    y = altura - 60

    pagina.setFont('Helvetica-Bold', 16)
    pagina.drawString(50, y, 'Prova - Respostas do Aluno')
    y -= 25

    pagina.setFont('Helvetica', 11)
    pagina.drawString(50, y, f'Aluno: {prova.aluno}')
    y -= 15
    pagina.drawString(50, y, f'Data: {prova.criado_em:%d/%m/%Y %H:%M}')
    y -= 15
    resumo = f'Objetivas: {total_objetivas}  |  Discursivas: {total_discursivas}'
    resumo += '  (correção pelo professor)'
    pagina.drawString(50, y, resumo)
    y -= 30

    for item in itens:
        questao = item.questao
        categoria = f'[{questao.categoria}] ' if questao.categoria else ''

        # quebra enunciado e resposta em linhas para caber na página
        linhas_titulo = textwrap.wrap(
            f'{item.ordem}. {categoria}{questao.enunciado}', width=90
        )
        resposta_aluno = item.resposta or 'Não respondida'
        if questao.tipo == 'ME':
            linhas_resposta = [f'Sua resposta: {resposta_aluno}']
        else:
            linhas_resposta = textwrap.wrap(
                f'Sua resposta: {resposta_aluno}', width=88
            )

        # se estiver perto do fim da página, cria uma página nova
        altura_bloco = (len(linhas_titulo) + len(linhas_resposta)) * 14
        if y < 80 + altura_bloco:
            pagina.showPage()
            y = altura - 60

        pagina.setFont('Helvetica-Bold', 10)
        for linha in linhas_titulo:
            pagina.drawString(50, y, linha)
            y -= 14

        pagina.setFont('Helvetica', 10)
        for linha in linhas_resposta:
            pagina.drawString(60, y, linha)
            y -= 14
        y -= 10

    pagina.showPage()
    pagina.save()
    return resposta_http
