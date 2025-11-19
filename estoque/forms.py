from django import forms
from .models import Produto, Movimentacao

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = '__all__'
        widgets = {
            'especificacoes': forms.Textarea(attrs={'rows': 3}),
        }

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['produto', 'tipo', 'quantidade', 'data']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }