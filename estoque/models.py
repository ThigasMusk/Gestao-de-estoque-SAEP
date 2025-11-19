from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    TIPOS_CHOICES = [
        ('SMARTPHONE', 'Smartphone'),
        ('NOTEBOOK', 'Notebook'),
        ('TABLET', 'Tablet'),
        ('SMARTTV', 'Smart TV'),
        ('ACESSORIO', 'Acessório'),
        ('OUTRO', 'Outro'),
    ]

    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    fabricante = models.CharField(max_length=100)
    
    # AQUI ESTÁ A SOLUÇÃO: Campo TIPO define o que é
    tipo = models.CharField(max_length=20, choices=TIPOS_CHOICES, default='OUTRO')
    
    # Especificações ficam em texto livre para flexibilidade total na prova
    # Ex: "RAM: 8GB, HD: 256SSD, Tela: 15pol"
    especificacoes = models.TextField(verbose_name="Especificações Técnicas", help_text="Descreva processador, RAM, cor, voltagem, etc.")
    
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=5)
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} ({self.get_tipo_display()})"

class Movimentacao(models.Model):
    TIPO_CHOICES = [
        ('E', 'Entrada'),
        ('S', 'Saída'),
    ]
    
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=1, choices=TIPO_CHOICES)
    quantidade = models.IntegerField()
    data = models.DateTimeField()
    responsavel = models.ForeignKey(User, on_delete=models.PROTECT)
    
    def __str__(self):
        return f"{self.tipo} - {self.produto.nome} ({self.quantidade})"