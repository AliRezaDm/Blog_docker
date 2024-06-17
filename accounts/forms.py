from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

class Customuser_creationform(UserCreationForm):
    
    class Meta:        
        model = get_user_model()
        fields = ['username', 'email', 'phone']


class Customuser_changeform(UserChangeForm):
    
    class Meta:        
        model = get_user_model()
        fields = ['username', 'email', 'phone']


