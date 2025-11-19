from django.db import models
from django.contrib.auth.models import User

class Produto(models.Model):
    nome = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    fabricante = models.CharField(max_length=100)
    
    cor = models.CharField(max_length=30, blank=True, null=True)
    voltagem = models.CharField(max_length=10, choices=[('110v', '110v'), ('220v', '220v'), ('bivolt', 'Bivolt')], blank=True)
    especificacoes = models.TextField(verbose_name="Especificações Técnicas", help_text="Processador, RAM, Tamanho Tela, Conectividade, etc.")
    
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    quantidade = models.IntegerField(default=0)
    estoque_minimo = models.IntegerField(default=5, verbose_name="Estoque Mínimo (Alerta)")
    
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nome} - {self.codigo}"

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