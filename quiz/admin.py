from django.contrib import admin
from quiz.models import Questao, Prova, ItemProva


@admin.register(Questao)
class QuestaoAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'categoria', 'tipo', 'enunciado'
    )
    list_filter = ('categoria', 'tipo')
    search_fields = ('enunciado',)


class ItemProvaInline(admin.TabularInline):
    # Mostra os itens dentro da prova: útil para conferir o que foi salvo no banco
    model = ItemProva
    extra = 0


@admin.register(Prova)
class ProvaAdmin(admin.ModelAdmin):
    list_display = ('id', 'aluno', 'criado_em', 'finalizada')
    inlines = [ItemProvaInline]
