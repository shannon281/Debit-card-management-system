from django.db import models

# Create your models here.

# Define a Django model representing a branch
class Branch(models.Model):

	# Define a field to store the branch name, with a maximum length of 50 characters
	branch_name = models.CharField(max_length=50, null=False, blank=False)

	# Define a string representation for the model instance
	def __str__(self):
		# Return the branch name as the string representation
		return self.branch_name


# Define a Django model representing cards
class Cards(models.Model):
	 # Define fields to store card details
	card_num = models.IntegerField(null= False, blank= False)
	member_name = models.CharField(max_length=100, null= True, blank= True)
	entry_date = models.DateField()
	requested = models.CharField(max_length=100, null= False, blank= False)

	# Define choices for select fields
	SELECT = (
		('Y', 'Yes'),
		('N', 'No'),
	)

	 # Define fields for embossed, received, and collected status with choices
	embossed = models.CharField(max_length=3, choices=SELECT)
	received = models.CharField(max_length=3, choices=SELECT)
	collected = models.CharField(max_length=3, choices=SELECT)

	 # Define a foreign key field to associate cards with branches
	branch = models.ForeignKey(Branch, on_delete=models.CASCADE)

	# Define a string representation for the model instance
	def __str__(self):
		# Return the card number as the string representation
		return str(self.card_num)

