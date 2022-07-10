from django import forms
from .models import NewDocument,Post,Comment,CommAddFranchise,UpdateDraftSpot

class DocumentForm(forms.ModelForm):
    class Meta:
        model = NewDocument
        fields = ('description', 'document', )




class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '1',
                    'columns': '12',
                    'placeholder': 'Title...'}
        ))   

    body = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say something...'}
        ))

    class Meta:
        model = Post
        fields = ['title','body']


class CommentForm(forms.ModelForm):
    comment = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                   'placeholder': 'Say something...'}
        ))

    class Meta:
        model = Comment
        fields = ['comment']

class FranchiseForm(forms.ModelForm):
    class Meta:
        model = CommAddFranchise
        fields = '__all__'

class UpdatePickForm(forms.ModelForm):
    class Meta:
        model = UpdateDraftSpot
        fields = '__all__'

class ThreadForm(forms.Form):
    username = forms.CharField(label='', max_length=100)

class MessageForm(forms.Form):
    message = forms.CharField(label='', max_length=1000)