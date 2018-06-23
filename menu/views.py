from django.shortcuts import render, redirect
from django.http import Http404
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from .forms import *


def menu_list(request):
    """This will bring menus not expired"""
    all_menus = Menu.objects.prefetch_related(
        'items'
    ).filter(
        Q(expiration_date__gte=timezone.now()) | Q(expiration_date=None)
    ).order_by(
        '-expiration_date'
    )
    return render(request, 'menu/list_all_current_menus.html', {'menus': all_menus})


def menu_detail(request, pk):
    menu = Menu.objects.prefetch_related(
        'items'
    ).get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})


def item_detail(request, pk):
    try:
        item = Item.objects.select_related(
            'chef'
        ).prefetch_related(
            'ingredients'
        ).get(pk=pk)
    except ObjectDoesNotExist:
        raise Http404
    return render(request, 'menu/detail_item.html', {'item': item})


def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            # Now, save the many-to-many data for the form.
            form.save_m2m()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {
        'form': form,
    })


def edit_menu(request, pk):
    menu = Menu.objects.prefetch_related(
        'items'
    ).get(
        pk=pk
    )
    form = MenuForm(instance=menu)
    if request.method == "POST":
        form = MenuForm(instance=menu, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu_detail', pk=menu.pk)
    return render(request, 'menu/menu_edit.html', {
        'form': form
    })
