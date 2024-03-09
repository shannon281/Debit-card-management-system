from django.urls import path,include
from . import views
from .views import MyPasswordChangeView, MyPasswordResetDoneView
from django.contrib.auth import views as auth_views

# Created URL patterns for the various different views
urlpatterns = [
     # URL pattern for the login page, mapped to the log_in view
	path('', views.log_in, name='log_in'),
    # URL pattern for the logout page, mapped to the log_out view
	path('log_out/', views.log_out, name='logout'),
    # URL pattern for adding a debit card, mapped to the cards_form view
	path('debitcard/', views.cards_form, name='card_insert'),
     # URL pattern for updating a debit card, mapped to the cards_form view with an ID parameter
	path('<int:id>/', views.cards_form, name='card_update'),
     # URL pattern for deleting a debit card, mapped to the cards_delete view with an ID parameter
	path('delete/<int:id>/', views.cards_delete, name='cards_delete'),
    # URL pattern for listing all debit cards, mapped to the cards_list view
	path('list/', views.cards_list, name='cards_list'),
    # URL pattern for changing the password, mapped to MyPasswordChangeView
	path('password/', MyPasswordChangeView.as_view(), name='password_change'),
    # URL pattern for the password change done page, mapped to MyPasswordResetDoneView
	path('password/done/', MyPasswordResetDoneView.as_view(), name='password_done'),
    # URL pattern for exporting data to CSV format, mapped to the export_csv view
	path('export_csv', views.export_csv, name="export-csv"),
     # URL pattern for exporting data to PDF format, mapped to the export_pdf view
    path('export_pdf', views.export_pdf, name="export-pdf"),
]
