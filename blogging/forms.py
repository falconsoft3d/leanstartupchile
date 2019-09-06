from django import forms
from models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('image','category', 'title', 'text')
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6
            })

        }
