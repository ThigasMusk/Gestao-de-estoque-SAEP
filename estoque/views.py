from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Movimentacao
from .forms import ProdutoForm, MovimentacaoForm

# 5. Interface Principal
@login_required
def home(request):
    return render(request, 'home.html')

# 6. Cadastro de Produto (Listagem + Busca + CRUD)
@login_required
def produto_lista(request):
    termo = request.GET.get('busca')
    if termo:
        # Item 6.1.2: Busca
        produtos = Produto.objects.filter(nome__icontains=termo)
    else:
        # Item 6.1.1: Listagem Automática
        produtos = Produto.objects.all()
    
    return render(request, 'produto_lista.html', {'produtos': produtos})

@login_required
def produto_criar(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid(): # Item 6.1.6 Validações
            form.save()
            messages.success(request, "Produto criado com sucesso!")
            return redirect('produto_lista')
    else:
        form = ProdutoForm()
    return render(request, 'produto_form.html', {'form': form, 'titulo': 'Novo Produto'})

@login_required
def produto_editar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, "Produto atualizado!")
            return redirect('produto_lista')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produto_form.html', {'form': form, 'titulo': 'Editar Produto'})

@login_required
def produto_deletar(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        produto.delete()
        messages.success(request, "Produto excluído.")
        return redirect('produto_lista')
    return render(request, 'produto_confirm_delete.html', {'produto': produto})

# 7. Gestão de Estoque
@login_required
def gestao_estoque(request):
    lista_produtos = list(Produto.objects.all())
    lista_produtos.sort(key=lambda x: x.nome.lower())
    
    historico = Movimentacao.objects.all().order_by('-id')
    
    form = MovimentacaoForm()
    
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST)
        if form.is_valid():
            mov = form.save(commit=False)
            mov.responsavel = request.user
            produto = mov.produto
            
            
            # Lógica de Entrada/Saída
            if mov.tipo == 'E':
                produto.quantidade += mov.quantidade
                messages.success(request, f"Entrada de {mov.quantidade} itens em {produto.nome}.")
            elif mov.tipo == 'S':
                if produto.quantidade >= mov.quantidade:
                    produto.quantidade -= mov.quantidade
                    
                    # Item 7.1.4: Verificação de Estoque Mínimo com Alerta
                    if produto.quantidade < produto.estoque_minimo:
                        messages.warning(request, f"ALERTA: O estoque de {produto.nome} está abaixo do mínimo ({produto.estoque_minimo})!")
                    else:
                        messages.success(request, "Saída registrada com sucesso.")
                else:
                    messages.error(request, "Erro: Quantidade insuficiente em estoque.")
                    return redirect('gestao_estoque')
            
            produto.save()
            mov.save()
            return redirect('gestao_estoque')

    return render(request, 'gestao_estoque.html', {
    'produtos': lista_produtos, 
    'form': form, 
    'historico': historico
})