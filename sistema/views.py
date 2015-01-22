from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from sistema.forms import *
from sistema.models import *
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib import auth
from django.conf import settings
from django.contrib.formtools.wizard.views import SessionWizardView		#INCLUIR
import os
from os import path
from django.contrib.auth import authenticate, login, logout

# Create your views here.
FORMS = [("Pessoa", PessoaForm), 		#INCLUIR para usar templates diferentes para cada form
		 ("Projeto", ProjetoForm)]

TEMPLATES = {"Pessoa": "wizard_form.html", 	#INCLUIR para usar templates diferentes para cada form
			"Projeto": "wizard_form_versao2.html"}
#FormWizard
class SubClassFormWizard(SessionWizardView):		
	template_name = 'wizard_form.html' 		#atributo substituido
	
	#def get_template_names(self): 			#metodo substituido para diferentes templates para cada form. So deve ser ativado se a url formwizard_diferentes for usada
	#	return [TEMPLATES[self.steps.current]]
	
	def done(self, form_list, **kwargs): 	#metodo substituido
	    for form in form_list:
		    form.save()
	    return HttpResponseRedirect('/visualizar_pessoas/')

# Cadastrar, editar e excluir pessoas
def cadastro_pessoa(request):
	if request.method == 'GET':
		pessoa_form = PessoaForm()
	if request.method == 'POST':
		pessoa_form = PessoaForm(request.POST)
		if pessoa_form.is_valid():
			pessoa_form.save()
			sucesso = True
			return HttpResponseRedirect('/cadastro_pessoa/')
		else:
			dados_incorretos = True
			return render(request, 'cadastro_pessoa.html', locals())
	return render(request, 'cadastro_pessoa.html', locals())

def editar_pessoa(request, id_pessoa):
	objeto = Pessoa.objects.get(id = id_pessoa)
	if request.method == 'GET':
		pessoa_form = PessoaForm(instance = objeto)
	if request.method == 'POST':
		pessoa_form = PessoaForm(request.POST,instance = objeto)
		if pessoa_form.is_valid():
			pessoa_form.save()
			sucesso = True
			return HttpResponseRedirect('/editar_pessoa/%s' %id_pessoa)
		else:
			dados_incorretos = True
			return render(request, 'editar_pessoa.html', locals())
	return render(request, 'editar_pessoa.html', locals())

def visualizar_pessoas (request):
    pessoas = Pessoa.objects.all()
    return render(request, 'visualizar_pessoas.html', locals())

def excluir_pessoa(request, id_pessoa):
	objeto = Pessoa.objects.get(id = id_pessoa)
	objeto.delete()
	messages.success(request, 'O cadastro foi deletado')
	return HttpResponseRedirect('/visualizar_pessoas/')

def home(request):
	return render(request, 'home.html', locals())

def login(request):
	login_incorreto = False
	if request.method == 'POST':
		usuario = request.POST.get("username")
		senha = request.POST.get("password")
		user = authenticate(username=usuario, password=senha)
		if user is not None:
			auth.login(request, user)
			return HttpResponseRedirect('/home/')
		else:
			login_incorreto = True
			return render(request, 'login.html', locals())
	else:
		return render(request, 'login.html', locals())

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/login/')

#Cadastrar, editar e excluir projetos
def cadastro_projeto(request):
	if request.method == 'GET':
		projeto_form = ProjetoForm()
	if request.method == 'POST':
		projeto_form = ProjetoForm(request.POST)
		if projeto_form.is_valid():
			projeto_form.save()
			sucesso = True
		else: 
			dados_incorretos = True
			return render_to_response('cadastro_projeto.html', locals(), context_instance=RequestContext(request))
	return render_to_response('cadastro_projeto.html', locals(), context_instance=RequestContext(request))

def editar_projeto(request, id_projeto):
	objeto = Projeto.objects.get(id = id_projeto)
	if request.method == 'GET':
		projeto_form = ProjetoForm(instance = objeto)
	if request.method == 'POST':
		projeto_form = ProjetoForm(instance = objeto)
		if projeto_form.is_valid():
			projeto_form.save()
		else:
			dados_incorretos = True
			return render_to_response('cadastro_projeto.html', locals(), context_instance=RequestContext(request))
	return render_to_response('cadastro_projeto.html', locals(), context_instance=RequestContext(request))

def excluir_projeto(request, id_projeto):
	objeto = Projeto.objects.get(id = id_projeto)
	objeto.delete()


