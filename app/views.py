from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.management import call_command
from django.views.decorators.http import require_POST

def index(request):
    return render(request, 'index.html')

@require_POST
def parse_links(request):
    call_command('parse_links')
    messages.add_message(request, messages.SUCCESS, 'Links parsing initiated.')
    return redirect('index')

@require_POST
def fetch_data(request):
    call_command('fetch_data')
    messages.add_message(request, messages.SUCCESS, 'Data fetching initiated.')
    return redirect('index')

@require_POST
def import_data(request):
    call_command('import_data')
    messages.add_message(request, messages.SUCCESS, 'Data import initiated.')
    return redirect('index')
