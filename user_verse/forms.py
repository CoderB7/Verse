from django import forms
from .models import Blog, Post

class BlogRegistrationForm(forms.ModelForm):
    
    blog_title = forms.CharField( 
        max_length=254,
        widget=forms.TextInput(
            attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Title',
            }
        )
    )

    class Meta:
        model = Blog
        fields = ['blog_title']

    def __init__(self, *args, **kwargs):
        super(BlogRegistrationForm, self).__init__(*args, **kwargs)

        self.fields['blog_title'].widget.attrs['class'] = 'form-control'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Blog.objects.filter(blog_title=title).exists():
            raise forms.ValidationError('Title already in use.')
        return title
    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'editor-title editor-content-title editor-placeholder',
                'placeholder': 'Post title...',
                'contenteditable': 'true',
            }),
            'content': forms.Textarea(attrs={
                'class': 'editor-content-body editor-placeholder',
                'placeholder': 'Start writing your content here...',
                'contenteditable': 'true',
                'rows': 10,
            }),
        }
    
