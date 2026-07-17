from django.db import models

ALTERNATIVAS = [
    ('A', 'Alternativa A'),
    ('B', 'Alternativa B'),
    ('C', 'Alternativa C'),
    ('D', 'Alternativa D'),
]

TIPOS = [
    ('ME', 'Múltipla escolha'),
    ('DI', 'Discursiva'),
]


class Questao(models.Model):
    """Uma questão da base. O professor cadastra pelo admin ou via fixture.

    Pode ser de múltipla escolha (alternativas A-D, corrigida pelo sistema)
    ou discursiva (o aluno digita a resposta, corrigida pelo professor).
    """
    categoria = models.CharField(max_length=50, blank=True, default='')
    tipo = models.CharField(max_length=2, choices=TIPOS, default='ME')
    enunciado = models.TextField()
    alternativa_a = models.CharField(max_length=200, blank=True, default='')
    alternativa_b = models.CharField(max_length=200, blank=True, default='')
    alternativa_c = models.CharField(max_length=200, blank=True, default='')
    alternativa_d = models.CharField(max_length=200, blank=True, default='')
    correta = models.CharField(
        max_length=1, choices=ALTERNATIVAS, blank=True, default=''
    )

    def __str__(self):
        return f'Questão {self.id} ({self.categoria}): {self.enunciado[:50]}'


class Prova(models.Model):
    """Uma tentativa de prova de um aluno: 10 questões sorteadas da base."""
    aluno = models.CharField(max_length=100)
    criado_em = models.DateTimeField(auto_now_add=True)
    finalizada = models.BooleanField(default=False)

    def __str__(self):
        return f'Prova de {self.aluno} em {self.criado_em:%d/%m/%Y %H:%M}'


class ItemProva(models.Model):
    """Liga uma questão sorteada a uma prova e guarda a resposta do aluno."""
    prova = models.ForeignKey(
        Prova, on_delete=models.CASCADE, related_name='itens'
    )
    questao = models.ForeignKey(Questao, on_delete=models.CASCADE)
    ordem = models.IntegerField()  # posição na prova (1 a 10)
    # objetivas guardam a letra (A-D); discursivas, o texto digitado
    resposta = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['ordem']

    def __str__(self):
        return f'{self.prova} - questão {self.ordem}'
