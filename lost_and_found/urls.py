from django.urls import path
from . import views

urlpatterns = [
    # The home path is "", goes to board.html
    path("", views.board_view, name='board'),
    # Method to add an item, needs three inputs (name, location, description)
    path("add/", views.add_item_view, name='add_item'),
    # Method to 'claim', to set is_returned boolean to True
    path("claim/<int:item_id>", views.claim_item, name='claim_item'),
    # Method to check history of items, same as Select * From LostTable
    path("history/", views.history_view, name='history'),
    # Method to delete history from /history/
    path('delete/<int:item_id>/', views.delete_history, name='delete_history'),

    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    ]
