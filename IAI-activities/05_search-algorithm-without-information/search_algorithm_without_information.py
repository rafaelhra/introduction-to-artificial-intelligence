def acao(destino, custo):
    return {'destino': destino, 'custo': custo}

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
        no_atual = self
        solucao = [no_atual]
        while no_atual.pai is not None:
            no_atual = no_atual.pai
            solucao.insert(0, no_atual)
        return solucao

class Problema:
    def __init__(self, espaco_estados, inicial, objetivo):
        self.espaco_estados = espaco_estados
        self.inicial = inicial
        self.objetivo = objetivo

BUSCA_INICIANDO = 0
BUSCA_FALHOU = 1
BUSCA_SUCESSO = 2
BUSCA_EM_CURSO = 3

class BuscaLargura:
    def __init__(self, problema):
        self.problema = problema
        self.fronteira = [problema.inicial]
        self.visitados = {problema.inicial.estado}
        self.solucao = []
        self.situacao = BUSCA_INICIANDO

    def executar(self):
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
        if self.situacao in [BUSCA_FALHOU, BUSCA_SUCESSO]:
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

class BuscaProfundidade:
    def __init__(self, problema):
        self.problema = problema
        self.fronteira = [problema.inicial]
        self.visitados = {problema.inicial.estado}
        self.solucao = []
        self.situacao = BUSCA_INICIANDO

    def executar(self):
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
        if self.situacao in [BUSCA_FALHOU, BUSCA_SUCESSO]:
            return
        if not self.fronteira:
            self.situacao = BUSCA_FALHOU
            return
        no = self.fronteira.pop()
        print(f"  - Expandindo nó: {no.estado}")
        print(f"  - Fronteira antes: {[n.estado for n in self.fronteira]}")
        if self.problema.objetivo(no):
            self.situacao = BUSCA_SUCESSO
            self.solucao = no.constroi_solucao()
            return
        filhos = no.filhos(self.problema)
        filhos.reverse()
        for filho in filhos:
            if filho.estado not in self.visitados:
                self.visitados.add(filho.estado)
                self.fronteira.append(filho)
        print(f"  - Fronteira depois: {[n.estado for n in self.fronteira]}")
        print(f"  - Visitados: {self.visitados}")

class ProblemaJarros:
    def __init__(self, inicial, objetivo_litros):
        self.inicial = No(inicial, 0, None, "Início")
        self.objetivo_litros = objetivo_litros
        self.espaco_estados = [] 

    def objetivo(self, no):
        return self.objetivo_litros in no.estado

    def filhos(self, no):
        j3, j5 = no.estado
        capacidade = (3, 5)
        filhos = []
        filhos.append(No((capacidade[0], j5), no.custo + 1, no, "Encher J3"))
        filhos.append(No((j3, capacidade[1]), no.custo + 1, no, "Encher J5"))
        filhos.append(No((0, j5), no.custo + 1, no, "Esvaziar J3"))
        filhos.append(No((j3, 0), no.custo + 1, no, "Esvaziar J5"))
        quantidade_a_despejar = min(j3, capacidade[1] - j5)
        filhos.append(No((j3 - quantidade_a_despejar, j5 + quantidade_a_despejar), no.custo + 1, no, "J3 -> J5"))
        quantidade_a_despejar = min(j5, capacidade[0] - j3)
        filhos.append(No((j3 + quantidade_a_despejar, j5 - quantidade_a_despejar), no.custo + 1, no, "J5 -> J3"))
        return filhos

class BuscaLarguraJarros(BuscaLargura):
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

if __name__ == "__main__":
    print("==========================================================")
    print("QUESTÃO 1: Rota de Arad a Bucharest com Busca em Largura")
    print("==========================================================")
    no_arad_bfs = No('Arad', 0, None, None)
    problema_romenia_bfs = Problema(estados_romenia,
                                no_arad_bfs,
                                lambda no: no.estado == 'Bucharest')
    busca_bfs = BuscaLargura(problema_romenia_bfs)
    busca_bfs.executar()

    print("\n\n")

    print("==========================================================")
    print("QUESTÃO 3 e 4: Rota de Arad a Bucharest com Busca em Profundidade")
    print("==========================================================")
    no_arad_dfs = No('Arad', 0, None, None)
    problema_romenia_dfs = Problema(estados_romenia,
                                    no_arad_dfs,
                                    lambda no: no.estado == 'Bucharest')
    busca_dfs = BuscaProfundidade(problema_romenia_dfs)
    busca_dfs.executar()

    print("\n\n")

    print("==========================================================")
    print("QUESTÃO 5: Problema dos Jarros (obter 4 litros)")
    print("==========================================================")
    
    print("\n--- Resolvendo com Busca em Largura (Jarros) ---")
    problema_jarros_bfs = ProblemaJarros(inicial=(0, 0), objetivo_litros=4)
    busca_jarros_bfs = BuscaLarguraJarros(problema_jarros_bfs)
    busca_jarros_bfs.executar()
    if busca_jarros_bfs.solucao:
        print("\nSolução (passos):")
        for no in busca_jarros_bfs.solucao:
            print(f"  Ação: {no.acao:<10} -> Estado: (J3={no.estado[0]}L, J5={no.estado[1]}L)")

    print("\n\n")
    
    print("\n--- Resolvendo com Busca em Profundidade (Jarros) ---")
    problema_jarros_dfs = ProblemaJarros(inicial=(0, 0), objetivo_litros=4)
    busca_jarros_dfs = BuscaProfundidadeJarros(problema_jarros_dfs)
    busca_jarros_dfs.executar()
    if busca_jarros_dfs.solucao:
        print("\nSolução (passos):")
        for no in busca_jarros_dfs.solucao:
            print(f"  Ação: {no.acao:<10} -> Estado: (J3={no.estado[0]}L, J5={no.estado[1]}L)")
