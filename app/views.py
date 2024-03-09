from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.management import call_command
from .forms import URLInputForm
from django.contrib import messages
def index(request):
    form = URLInputForm()
    return render(request, 'index.html', {'form': form})

@require_POST
def parse_links_view(request):
    form = URLInputForm(request.POST)
    if form.is_valid():
        url = form.cleaned_data['url']
        call_command('parse_links', url)
    return redirect('index')

@require_POST
def run_oxy_view(request):
    call_command('run_oxy')
    return redirect('index')

@require_POST
def import_products(request):
    try:
        # Предполагается, что файл данных находится в известном месте
        # Вы можете модифицировать это, чтобы загружать файл через веб-интерфейс
        file_path = 'response.json'
        call_command('import_from_oxy', file_path)
        messages.success(request, "Products have been successfully imported.")
    except Exception as e:
        messages.error(request, f"Failed to import products: {e}")
    return redirect('index')

@require_POST
def update_products_view(request):
    try:
        file_path = 'response.json'
        call_command('update_products', file_path)
        messages.success(request, "Products have been successfully updated.")
    except Exception as e:
        messages.error(request, f"Failed to update products: {e}")
    return redirect('index')
