from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import MenuCategory, MenuItem
from .forms import MenuCategoryForm, MenuItemForm
from django.contrib import messages


@login_required
def add_category(request):
    if request.method == 'POST':
        form = MenuCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category added.')
        else:
            messages.error(request, f"Couldn't add category: {form.errors}")
    return redirect('core:dashboard')


@login_required
def add_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    return redirect('core:dashboard')


@login_required
def edit_item(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
    return redirect('core:dashboard')

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(MenuCategory, pk=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, f'"{category.name}" deleted.')
    return redirect('core:dashboard')


@login_required
def delete_item(request, item_id):
    item = get_object_or_404(MenuItem, pk=item_id)
    if request.method == 'POST':
        item.delete()
        messages.success(request, f'"{item.name}" deleted.')
    return redirect('core:dashboard')