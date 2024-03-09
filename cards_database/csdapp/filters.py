import django_filters
from django_filters import DateFilter, NumberFilter

from .models import *


# Define a Django filter set for the Cards model
class CardFilter(django_filters.FilterSet):
	# Define filters for card_num and entry_date fields
	card_num = NumberFilter(field_name="card_num", lookup_expr='icontains')
	entry_date = DateFilter(field_name="entry_date", lookup_expr='exact')

	# Define a nested Meta class to specify filter behavior
	class Meta:
		# Associate the filter set with the Cards model
		model = Cards
		# Include all fields from the Cards model in the filter set
		fields = '__all__'
		# Exclude specific fields from being included as filters
		exclude = ['member_name', 'requested', 'embossed', 'received', 'collected']
