from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from .models import LostTable
# from .serializers import LostItemSerializer
from .forms import LostItemForm


def register_view(request):
    '''
    This is for registering new user.
    Make a POST request to post a new user.
    '''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('board')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    '''
    This is for login with user credentials.
    '''
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('board')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    '''
    This is for logout from user.
    This destroys current user session.
    '''
    logout(request)
    return redirect('login')

# Needs login for views below:
@login_required(login_url='/login/')
def board_view(request):
    '''
    This is the home path of the app. 
    Shows items that has not been 'claimed' (is_returned == False)
    '''
    items = LostTable.objects.filter(user=request.user, is_returned=False).order_by("-found_date")
    return render(request, 'board.html', {'items': items})

@login_required(login_url='/login/')
def add_item_view(request):
    '''
    This is the method to add ('report') an item,
    First, GET the add_item page
    After filling the information (name, location, description), posts to database
    After posts, returns back to home path ('board')
    '''
    if request.method == "POST":
        form = LostItemForm(request.POST)
        if form.is_valid():
            new_item = form.save(commit=False)
            new_item.user = request.user
            new_item.save()
            return redirect('board')
    else:
            form = LostItemForm()

    return render(request, 'add_item.html', {'form': form})

@login_required(login_url='/login/')
def claim_item(request, item_id):
    ''' 
    This is the method to change the boolean is_returned from False -> True
    '''
    item = get_object_or_404(LostTable, id = item_id, user=request.user)
    item.is_returned = True
    item.save()
    return redirect('board')

@login_required(login_url='/login/')
def history_view(request):
    '''
    This is the 'history/' of the app
    Opens a table of all the items stored in database ordered by found_date descending
    '''
    items = LostTable.objects.filter(user=request.user).order_by("-found_date")
    return render(request, 'history.html', {'items': items})

@login_required(login_url='/login/')
def delete_history(request, item_id):
    '''
    This is the method to delete history in 'history/'
    Deletes the row of selected item from 'LostTable' table
    '''
    item = get_object_or_404(LostTable, id=item_id, user=request.user)
    item.delete()
    return redirect('history')
