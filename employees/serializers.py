from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'role', 'date_of_joining', 'supervised_by']
        

    def validate_supervised_by(self, value):
        """
        Validates the `supervised_by` field.
        - Raises an error if a non-super_admin user tries to modify it.
        """
        
        request = self.context.get('request')
        if request and request.user.role != 'super_admin':
            raise serializers.ValidationError("You do not have permission to modify this field.")
        return value