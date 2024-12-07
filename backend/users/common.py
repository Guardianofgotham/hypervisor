from django.forms import ValidationError
from rest_framework import serializers


class ApiSerializer(serializers.Serializer):
    def __init__(self, data=None, **kwargs):
        """
        Initialize the serializer with data and validate it immediately.
        """
        # Pass the data to the parent constructor to handle serialization
        super().__init__(data=data, **kwargs)

    def get_validated_data(self):
        """
        This method returns the validated data if it is valid.
        If the data is invalid, it raises a ValidationError with the appropriate error details.
        """
        if self.is_valid():
            # Return the validated data if it is valid
            return self.validated_data
        else:
            # Raise ValidationError with the errors if data is invalid
            raise ValidationError(self.errors)
