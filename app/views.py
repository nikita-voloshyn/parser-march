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


def call_update_availability_view(request):
    try:
        call_command('update_availability')
        messages.success(request, "Availability updated successfully.")
    except Exception as e:
        messages.error(request, f"Error occurred: {str(e)}")

    # Перенаправление на страницу (например, на главную)
    return render(request, 'index.html')
