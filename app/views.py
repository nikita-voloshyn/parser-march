from django.shortcuts import render, redirect
from django.core.management import call_command
from django.contrib import messages

def import_products_view(request):
    if request.method == "POST":
        try:
            call_command('data_import', 'app/management/scripts/all_products_details.json')
            messages.success(request, 'Products were successfully imported.')
        except Exception as e:
            messages.error(request, f'An error occurred: {str(e)}')
        return redirect('index')

    return render(request, 'index.html')

def link_start(request):
    try:
        call_command('link_start')
        messages.success(request, "Links fetched successfully.")
    except Exception as e:
        messages.error(request, f"Error occurred: {str(e)}")

    return render(request, 'index.html')

def data_from_link_start(request):
    try:
        call_command('data_from_link')
        messages.success(request, "Data fetched successfully.")
    except Exception as e:
        messages.error(request, f"Error occurred: {str(e)}")

    return render(request, 'index.html')
