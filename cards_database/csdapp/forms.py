from django import forms
from .models import Cards

# Define a Django form for the Cards model
class CardForm(forms.ModelForm):

	# Define a nested Meta class to specify form behavior
	class Meta:
		# Associate the form with the Cards model
		model = Cards
		# Include all fields from the Cards model in the form
		fields = '__all__'
		# Customize labels for form fields
		labels = {
			'card_num': 'Card Number',
		}

