from django.shortcuts import render, redirect
from .forms import CardForm
from .models import Cards
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import PasswordChangeView, PasswordResetDoneView
from django.contrib import messages
from .filters import CardFilter
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
import datetime
from django.http import JsonResponse, HttpResponse
import csv
from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile
from django.db.models import Sum
from django.core.paginator import Paginator



# Create your views here.

def log_in(request):
	# Check if the request method is POST
	if request.method == 'POST':
		# Retrieve the username and password from the POST data
		username = request.POST.get('username')
		password = request.POST.get('password')

		# Authenticate the user with the provided username and password
		user = authenticate(request, username=username, password=password)

		# If authentication is successful, log in the user and redirect to 'cards_list' page
		if user is not None:
			login(request, user)
			return redirect('cards_list')
		# If authentication fails, display an error message
		else:
			messages.info(request, 'Username OR password is incorrect')

	# If the request method is not POST, render the login page
	context = {}
	return render(request, "csdapp/login.html", context)



def log_out(request):
	 # Call Django's logout function to log out the current user
	logout(request)

	 # Redirect to the 'log_in' URL after logging out
	return redirect('log_in')


@login_required(login_url='log_in')
def cards_list(request):
	# Initialize an empty context dictionary
	context = {}

	# Retrieve all Card objects from the database, ordered by id in reverse order
	cards = Cards.objects.all().order_by('id').reverse()

	# Create a CardFilter instance with request.GET data and the queryset of cards
	myFilter = CardFilter(request.GET, queryset=cards)

	#context = {'cards_list': cards, 'myFilter': myFilter}
	context['myFilter'] = myFilter

	# Paginate the filtered queryset with 10 items per page
	p = Paginator(myFilter.qs, 10)
	page = request.GET.get('page')
	cards_page= p.get_page(page)
	
	# Add the paginated cards to the context
	context['cards_page'] = cards_page

	return render(request, "csdapp/cards_list.html", context=context)



@login_required(login_url='log_in')
def cards_form(request, id=0):
	# Check if the request method is GET
	if request.method == "GET":
		# If it's a GET request, determine whether to create a new card or edit an existing one
		if id==0:
			# If id is 0, create a new CardForm instance
			form = CardForm()
		else:
			# If id is not 0, retrieve the Card object with the specified ID from the database
			card = Cards.objects.get(pk=id)
			# Populate the form with the data from the retrieved Card object
			form = CardForm(instance=card)
		return render(request, "csdapp/cards_form.html", {'form':form})
	else:
		# If the request method is POST, process the form data
		if id == 0:
			 # If id is 0, create a new CardForm instance with the POST data
			form = CardForm(request.POST)
		else:
			 # If id is not 0, retrieve the Card object with the specified ID from the database
			card = Cards.objects.get(pk=id)
			# Populate the form with the POST data and the data from the retrieved Card object
			form = CardForm(request.POST,instance= card)
		if form.is_valid():
			form.save()
		return redirect('/list')


# This view requires the user to be logged in. If not it redirects to the login page
@login_required(login_url='log_in')
def cards_delete(request,id):
	# Retrieve the card object with the specified ID from the database
	card = Cards.objects.get(pk=id)
	if request.method == "POST":
		card.delete()
		return redirect('/list')

	# If the request method is not POST prepare the context with the card object
	context = {'card':card}
	return render(request, "csdapp/delete.html", context)


#Define a custom view for the password change functionality
class MyPasswordChangeView(PasswordChangeView):
	# Set the template to be used for rendering the password change page
	template_name = "csdapp/change_password.html"
	# Se the URL to redirect to after a successful password change
	success_url = reverse_lazy('password_done')


#Define a custom view for the password reset done page
class MyPasswordResetDoneView(PasswordResetDoneView):
	# Set the tamplate to be used for rendering the password reset done page
	template_name = 'csdapp/password_reseted.html'


# export cards obeject baseed on the filtered queryset using csv file format
def export_csv(request):
	cards = Cards.objects.all()
	filter = CardFilter(request.GET, queryset=cards).qs

	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename= Cards-Report ' + str(datetime.datetime.now()) +'.csv'

	writer = csv.writer(response)
	writer.writerow(['Card Number', 'Member Name', 'Entry Date', 'Requested', 'Embossed', 'Received', 'Collected', 'Branch'])

	#Iterate over each card object in the filter queryset
	for card in filter:
		#Write a roww containing card data to the CSV file
		writer.writerow([card.card_num, card.member_name, card.entry_date, card.requested, card.embossed, card.received, card.collected, card.branch])

	return response


# export cards obeject baseed on the filtered queryset using pdf file format

def export_pdf(request):
	#creates an instance of an HTTP response with contenet type set to application/pdf
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'inline; attachment; filename= Cards-Report ' + str(datetime.datetime.now()) +'.pdf'
	response['Content-Transfer-Encoding'] = 'binary'
	
	#Returns a queryset containing all the objects (instances) of the Cards model.
	cards = Cards.objects.all()
	filter = CardFilter(request.GET, queryset=cards).qs

	html_string=render_to_string('csdapp/pdf-report.html', {'cards': filter, 'total': 0})

	html = HTML(string=html_string)

	result = html.write_pdf()

	#Generate a temporary file to store the result data
	with tempfile.NamedTemporaryFile(delete=True) as output:
		output.write(result)
		output.flush()

		output = open(output.name, 'rb')
		response.write(output.read())

	return response


