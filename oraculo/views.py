from django.shortcuts import render, redirect
from rolepermissions.checkers import has_permission
from django.http import Http404
from django.views.decorators.csrf import csrf_exempt
from .models import Treinamentos

def treinar_ia(request):
    if not has_permission(request.user, 'treinar_ia'):
        raise Http404()
    if request.method == 'GET':
        #tasks = Task.objects.all()
        return render(request, 'treinar_ia.html')
    elif request.method == 'POST':
        site = request.POST.get('site')
        conteudo = request.POST.get('conteudo')
        documento = request.FILES.get('documento')

        treinamento = Treinamentos(
            site=site,
            conteudo=conteudo,
            documento=documento
        )
        treinamento.save()

        return redirect('treinar_ia')


@csrf_exempt
def chat(request):
    if request.method == 'GET':
        return render(request, 'chat.html')
    elif request.method == 'POST':
        # TODO: Tarefa 6 - Criar uma pergunta
        ...
    
@csrf_exempt
def stream_response(request):
    # TODO: Usar IA para obter a resposta e enviar em tempo real
    ...

def ver_fontes(request, id):
    return render(request, 'ver_fontes.html')