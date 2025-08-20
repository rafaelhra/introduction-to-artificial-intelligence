# -*- coding: utf-8 -*-

# =============================================================================
# DEFINIÇÕES BASE (FORNECIDAS NA ATIVIDADE)
# =============================================================================

def acao(destino, custo):
    """Cria um dicionário representando uma ação."""
    return {'destino': destino, 'custo': custo}

# Espaço de estados para o problema das cidades da Romênia
estados_romenia = [
    {'estado': 'Arad',
     'acoes': [acao('Zerind', 75), acao('Sibiu', 140), acao('Timisoara', 118)]},
    {'estado': 'Zerind',
     'acoes': [acao('Arad', 75), acao('Oradea', 71)]},
    {'estado': 'Timisoara',
     'acoes': [acao('Arad', 118), acao('Lugoj', 111)]},
    {'estado': 'Sibiu',
     'acoes': [acao('Arad', 140), acao('Oradea', 151), acao('Fagaras', 99),
               acao('Rimnicu Vilcea', 80)]},
    {'estado': 'Oradea',
     'acoes': [acao('Zerind', 71), acao('Sibiu', 151)]},
    {'estado': 'Lugoj',
     'acoes': [acao('Timisoara', 111), acao('Mehadia', 70)]},
    {'estado': 'Mehadia',
     'acoes': [acao('Lugoj', 70), acao('Drobeta', 75)]},
    {'estado': 'Drobeta',
     'acoes': [acao('Mehadia', 75), acao('Craiova', 120)]},
    {'estado': 'Craiova',
     'acoes': [acao('Drobeta', 120), acao('Rimnicu Vilcea', 146),
               acao('Pitesti', 138)]},
    {'estado': 'Rimnicu Vilcea',
     'acoes': [acao('Sibiu', 80), acao('Craiova', 146), acao('Pitesti', 97)]},
    {'estado': 'Fagaras',
     'acoes': [acao('Sibiu', 99), acao('Bucharest', 211)]},
    {'estado': 'Pitesti',
     'acoes': [acao('Rimnicu Vilcea', 97), acao('Craiova', 138), acao('Bucharest', 101)]},
    {'estado': 'Giurgiu',
     'acoes': [acao('Bucharest', 90)]},
    {'estado': 'Bucharest',
     'acoes': [acao('Fagaras', 211), acao('Pitesti', 101), acao('Giurgiu', 90),
               acao('Urziceni', 85)]},
    {'estado': 'Urziceni',
     'acoes': [acao('Bucharest', 85), acao('Vaslui', 142), acao('Hirsova', 98)]},
    {'estado': 'Hirsova',
     'acoes': [acao('Urziceni', 98), acao('Eforie', 86)]},
    {'estado': 'Eforie',
     'acoes': [acao('Hirsova', 86)]},
    {'estado': 'Vaslui',
     'acoes': [acao('Urziceni', 142), acao('Iasi', 92)]},
    {'estado': 'Iasi',
     'acoes': [acao('Vaslui', 92), acao('Neamt', 87)]},
    {'estado': 'Neamt',
     'acoes': [acao('Iasi', 87)]}
]

class No:
    """Classe que representa um nó na árvore de busca."""
    def __init__(self, estado, custo, pai, acao):
        self.estado = estado
        self.custo = custo
        self.pai = pai
        self.acao = acao

    def __str__(self):
        return f'({self.estado}, {self.custo})'

    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.estado == other.estado

    def filhos(self, problema):
        """Gera os nós filhos a partir do estado atual."""
        espaco_acoes = next((e for e in problema.espaco_estados if e['estado'] == self.estado), None)
        
        if espaco_acoes is None:
            return []

        resultado = []
        for acao_info in espaco_acoes['acoes']:
            filho = No(acao_info['destino'], self.custo + acao_info['custo'],
                       self, acao_info['destino'])
            resultado.append(filho)
        return resultado

    def constroi_solucao(self):
        """Retorna a sequência de nós do início até o nó atual."""
        no_atual = self
        solucao = [no_atual]
        while no_atual.pai is not None:
            no_atual = no_atual.pai
            solucao.insert(0, no_atual)
        return solucao

class Problema:
    """Classe que define o problema a ser resolvido."""
    def __init__(self, espaco_estados, inicial, objetivo):
        self.espaco_estados = espaco_estados
        self.inicial = inicial
        self.objetivo = objetivo

# Constantes para o status da busca
BUSCA_INICIANDO = 0
BUSCA_FALHOU = 1
BUSCA_SUCESSO = 2
BUSCA_EM_CURSO = 3

# =============================================================================
# QUESTÃO 1 e 3: IMPLEMENTAÇÃO DA BUSCA EM LARGURA (BFS)
# =============================================================================

class BuscaLargura:
    """Implementação da Busca em Largura (Breadth-First Search)."""
    def __init__(self, problema):
        self.problema = problema
        self.fronteira = [problema.inicial]
        self.visitados = {problema.inicial.estado} # Usar um set para busca mais rápida
        self.solucao = []
        self.situacao = BUSCA_INICIANDO

    def executar(self):
        """Executa a busca em largura passo a passo até encontrar a solução ou falhar."""
        print("--- Iniciando Busca em Largura ---")
        passo = 0
        while self.situacao not in [BUSCA_FALHOU, BUSCA_SUCESSO]:
            print(f"\nPasso {passo}:")
            self.passo_busca()
            passo += 1

        if self.situacao == BUSCA_FALHOU:
            print("\nBusca falhou: Não foi possível encontrar uma solução.")
        elif self.situacao == BUSCA_SUCESSO:
            print("\nBusca teve sucesso!")
            custo_total = self.solucao[-1].custo
            print(f"Solução encontrada: {[no.estado for no in self.solucao]}")
            print(f"Custo total: {custo_total}")
        return

    def passo_busca(self):
        """Executa um único passo da busca."""
        if self.situacao == BUSCA_FALHOU:
            return
        if self.situacao == BUSCA_SUCESSO:
            return

        if not self.fronteira:
            self.situacao = BUSCA_FALHOU
            return

        no = self.fronteira.pop(0)
        print(f"  - Expandindo nó: {no.estado}")
        print(f"  - Fronteira antes: {[n.estado for n in self.fronteira]}")


        if self.problema.objetivo(no):
            self.situacao = BUSCA_SUCESSO
            self.solucao = no.constroi_solucao()
            return

        for filho in no.filhos(self.problema):
            if filho.estado not in self.visitados:
                self.visitados.add(filho.estado)
                self.fronteira.append(filho)
        
        print(f"  - Fronteira depois: {[n.estado for n in self.fronteira]}")
        print(f"  - Visitados: {self.visitados}")


# =============================================================================
# QUESTÃO 2 e 4: IMPLEMENTAÇÃO DA BUSCA EM PROFUNDIDADE (DFS)
# =============================================================================

class BuscaProfundidade:
    """Implementação da Busca em Profundidade (Depth-First Search)."""
    def __init__(self, problema):
        self.problema = problema
        # A fronteira em DFS funciona como uma pilha (LIFO)
        self.fronteira = [problema.inicial]
        self.visitados = {problema.inicial.estado}
        self.solucao = []
        self.situacao = BUSCA_INICIANDO

    def executar(self):
        """Executa a busca em profundidade passo a passo."""
        print("--- Iniciando Busca em Profundidade ---")
        passo = 0
        while self.situacao not in [BUSCA_FALHOU, BUSCA_SUCESSO]:
            print(f"\nPasso {passo}:")
            self.passo_busca()
            passo += 1

        if self.situacao == BUSCA_FALHOU:
            print("\nBusca falhou: Não foi possível encontrar uma solução.")
        elif self.situacao == BUSCA_SUCESSO:
            print("\nBusca teve sucesso!")
            custo_total = self.solucao[-1].custo
            print(f"Solução encontrada: {[no.estado for no in self.solucao]}")
            print(f"Custo total: {custo_total}")
        return

    def passo_busca(self):
        """Executa um único passo da busca."""
        if self.situacao == BUSCA_FALHOU or self.situacao == BUSCA_SUCESSO:
            return

        if not self.fronteira:
            self.situacao = BUSCA_FALHOU
            return

        # A ÚNICA MUDANÇA é aqui: .pop() remove o último elemento (pilha)
        # em vez de .pop(0) que remove o primeiro (fila).
        no = self.fronteira.pop()
        print(f"  - Expandindo nó: {no.estado}")
        print(f"  - Fronteira antes: {[n.estado for n in self.fronteira]}")

        if self.problema.objetivo(no):
            self.situacao = BUSCA_SUCESSO
            self.solucao = no.constroi_solucao()
            return

        # Adiciona os filhos ao início da fronteira para manter a ordem de pilha
        filhos = no.filhos(self.problema)
        filhos.reverse() # Inverte para explorar em ordem alfabética (opcional, mas bom para consistência)
        for filho in filhos:
            if filho.estado not in self.visitados:
                self.visitados.add(filho.estado)
                self.fronteira.append(filho)
        
        print(f"  - Fronteira depois: {[n.estado for n in self.fronteira]}")
        print(f"  - Visitados: {self.visitados}")


# =============================================================================
# QUESTÃO 5: PROBLEMA DOS JARROS DE ÁGUA
# =============================================================================

class ProblemaJarros:
    """Define o problema dos jarros de água."""
    def __init__(self, inicial, objetivo_litros):
        # O estado é uma tupla (jarro3L, jarro5L)
        self.inicial = No(inicial, 0, None, None)
        self.objetivo_litros = objetivo_litros
        # O espaço de estados é gerado dinamicamente, então não é armazenado aqui.
        self.espaco_estados = [] # Não usado diretamente, mas a classe No precisa dele.

    def objetivo(self, no):
        """Verifica se o estado do nó é o objetivo."""
        return self.objetivo_litros in no.estado

    def filhos(self, no):
        """Gera todos os estados possíveis a partir do estado atual."""
        j3, j5 = no.estado
        capacidade = (3, 5)
        filhos = []
        
        # Ações possíveis:
        # 1. Encher um jarro
        # 2. Esvaziar um jarro
        # 3. Despejar de um para outro
        
        # Encher J3
        if j3 < capacidade[0]:
            filhos.append(No((capacidade[0], j5), no.custo + 1, no, "Encher J3"))
        # Encher J5
        if j5 < capacidade[1]:
            filhos.append(No((j3, capacidade[1]), no.custo + 1, no, "Encher J5"))
        
        # Esvaziar J3
        if j3 > 0:
            filhos.append(No((0, j5), no.custo + 1, no, "Esvaziar J3"))
        # Esvaziar J5
        if j5 > 0:
            filhos.append(No((j3, 0), no.custo + 1, no, "Esvaziar J5"))
            
        # Despejar de J3 para J5
        if j3 > 0 and j5 < capacidade[1]:
            quantidade = min(j3, capacidade[1] - j5)
            filhos.append(No((j3 - quantidade, j5 + quantidade), no.custo + 1, no, "J3 -> J5"))

        # Despejar de J5 para J3
        if j5 > 0 and j3 < capacidade[0]:
            quantidade = min(j5, capacidade[0] - j3)
            filhos.append(No((j3 + quantidade, j5 - quantidade), no.custo + 1, no, "J5 -> J3"))
            
        return filhos

# Adaptando as classes de busca para o problema dos jarros
class BuscaLarguraJarros(BuscaLargura):
    def __init__(self, problema):
        super().__init__(problema)
        # Para o problema dos jarros, o 'estado' é uma tupla
        self.visitados = {problema.inicial.estado}

    def passo_busca(self):
        if not self.fronteira:
            self.situacao = BUSCA_FALHOU
            return
        no = self.fronteira.pop(0)

        if self.problema.objetivo(no):
            self.situacao = BUSCA_SUCESSO
            self.solucao = no.constroi_solucao()
            return
        
        for filho in self.problema.filhos(no):
            if filho.estado not in self.visitados:
                self.visitados.add(filho.estado)
                self.fronteira.append(filho)

class BuscaProfundidadeJarros(BuscaProfundidade):
    def __init__(self, problema):
        super().__init__(problema)
        self.visitados = {problema.inicial.estado}

    def passo_busca(self):
        if not self.fronteira:
            self.situacao = BUSCA_FALHOU
            return
        no = self.fronteira.pop()

        if self.problema.objetivo(no):
            self.situacao = BUSCA_SUCESSO
            self.solucao = no.constroi_solucao()
            return
        
        filhos = self.problema.filhos(no)
        filhos.reverse()
        for filho in filhos:
            if filho.estado not in self.visitados:
                self.visitados.add(filho.estado)
                self.fronteira.append(filho)

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================
if __name__ == "__main__":
    # --- QUESTÃO 1: Rota de Arad a Bucharest com BFS ---
    print("==========================================================")
    print("QUESTÃO 1: Rota de Arad a Bucharest com Busca em Largura")
    print("==========================================================")
    no_arad = No('Arad', 0, None, None)
    problema_romenia = Problema(estados_romenia,
                                no_arad,
                                lambda no: no.estado == 'Bucharest')
    
    busca_bfs = BuscaLargura(problema_romenia)
    busca_bfs.executar()

    print("\n\n")

    # --- QUESTÃO 3 e 4: Rota de Arad a Bucharest com DFS ---
    # (Usando o mesmo par de cidades da Questão 1, conforme a correção)
    print("==========================================================")
    print("QUESTÃO 3 e 4: Rota de Arad a Bucharest com Busca em Profundidade")
    print("==========================================================")
    
    # Reiniciando o problema para uma nova busca
    no_arad_dfs = No('Arad', 0, None, None)
    problema_romenia_dfs = Problema(estados_romenia,
                                    no_arad_dfs,
                                    lambda no: no.estado == 'Bucharest')
    
    busca_dfs = BuscaProfundidade(problema_romenia_dfs)
    busca_dfs.executar()

    print("\n\n")

    # --- QUESTÃO 5: Problema dos Jarros ---
    print("==========================================================")
    print("QUESTÃO 5: Problema dos Jarros (obter 4 litros)")
    print("==========================================================")
    
    # Resolvendo com BFS
    print("\n--- Resolvendo com Busca em Largura (Jarros) ---")
    problema_jarros_bfs = ProblemaJarros(inicial=(0, 0), objetivo_litros=4)
    busca_jarros_bfs = BuscaLarguraJarros(problema_jarros_bfs)
    busca_jarros_bfs.executar()
    print("\nSolução (passos):")
    for no in busca_jarros_bfs.solucao:
        print(f"  Estado: {no.estado}, Ação: {no.acao}")

    print("\n\n")
    
    # Resolvendo com DFS
    print("\n--- Resolvendo com Busca em Profundidade (Jarros) ---")
    problema_jarros_dfs = ProblemaJarros(inicial=(0, 0), objetivo_litros=4)
    busca_jarros_dfs = BuscaProfundidadeJarros(problema_jarros_dfs)
    busca_jarros_dfs.executar()
    print("\nSolução (passos):")
    for no in busca_jarros_dfs.solucao:
        print(f"  Estado: {no.estado}, Ação: {no.acao}")