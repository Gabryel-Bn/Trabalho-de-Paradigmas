class GerenciadorDeHeap:
    def __init__(self, tamanho, estrategia='best'):
        self.heap = [False] * tamanho
        self.lista_livre = [{'inicio': 0, 'tamanho': tamanho}] 
        self.alocacoes = {}
        self.estrategia = estrategia

    def definir_estrategia_heap(self, estrategia):
        self.estrategia = estrategia

    def encontrar_bloco_livre(self, tamanho):
        if self.estrategia == 'best':
            return self.melhor_encontro(tamanho)
        elif self.estrategia == 'worst':
            return self.pior_encontro(tamanho)
        elif self.estrategia == 'first':
            return self.primeiro_encontro(tamanho)
        elif self.estrategia == 'next':
            return self.proximo_encontro(tamanho)

    def melhor_encontro(self, tamanho):
        melhor_indice = None
        melhor_tamanho = float('inf')
        for i, bloco in enumerate(self.lista_livre):
            if bloco['tamanho'] >= tamanho and bloco['tamanho'] < melhor_tamanho:
                melhor_tamanho = bloco['tamanho']
                melhor_indice = i
        return melhor_indice

    def pior_encontro(self, tamanho):
        pior_indice = None
        pior_tamanho = -1
        for i, bloco in enumerate(self.lista_livre):
            if bloco['tamanho'] >= tamanho and bloco['tamanho'] > pior_tamanho:
                pior_tamanho = bloco['tamanho']
                pior_indice = i
        return pior_indice

    def primeiro_encontro(self, tamanho):
        for i, bloco in enumerate(self.lista_livre):
            if bloco['tamanho'] >= tamanho:
                return i
        return None

    def proximo_encontro(self, tamanho):
        return self.primeiro_encontro(tamanho)

    def alocar(self, id, tamanho):
        indice = self.encontrar_bloco_livre(tamanho)
        if indice is not None:
            bloco = self.lista_livre[indice]
            self.alocacoes[id] = {'inicio': bloco['inicio'], 'tamanho': tamanho}
            for i in range(bloco['inicio'], bloco['inicio'] + tamanho):
                self.heap[i] = True
            if bloco['tamanho'] == tamanho:
                self.lista_livre.pop(indice)
            else:
                bloco['inicio'] += tamanho
                bloco['tamanho'] -= tamanho
        else:
            print(f"Não foi possível alocar {tamanho} blocos para {id}.")

    def desalocar(self, id):
        if id in self.alocacoes:
            bloco = self.alocacoes.pop(id)
            for i in range(bloco['inicio'], bloco['inicio'] + bloco['tamanho']):
                self.heap[i] = False
            self.lista_livre.append({'inicio': bloco['inicio'], 'tamanho': bloco['tamanho']})
            self.fundir_lista_livre()

    def fundir_lista_livre(self):
        self.lista_livre.sort(key=lambda x: x['inicio'])
        lista_fundida = []
        atual = self.lista_livre[0]
        for i in range(1, len(self.lista_livre)):
            if atual['inicio'] + atual['tamanho'] == self.lista_livre[i]['inicio']:
                atual['tamanho'] += self.lista_livre[i]['tamanho']
            else:
                lista_fundida.append(atual)
                atual = self.lista_livre[i]
        lista_fundida.append(atual)
        self.lista_livre = lista_fundida

    def atribuir(self, id1, id2):
        if id2 in self.alocacoes:
            if id1 in self.alocacoes:
                self.desalocar(id1)
            self.alocacoes[id1] = self.alocacoes[id2].copy()

    def exibe(self):
        print(self.heap)

class MenuGerenciadorHeap:
    def __init__(self, tamanho_heap):
        self.gerenciador = GerenciadorDeHeap(tamanho_heap)

    def exibir_menu(self):
        print("\n--- Gerenciador de Heap ---")
        print("1. Definir estratégia de heap")
        print("2. Alocar bloco de memória")
        print("3. Desalocar bloco de memória")
        print("4. Atribuir memória de um ID a outro")
        print("5. Exibir estado do heap")
        print("6. Sair")

    def executar_opcao(self, opcao):
        if opcao == 1:
            estrategia = input("Digite a estratégia de heap (best, worst, first, next): ").strip().lower()
            self.gerenciador.definir_estrategia_heap(estrategia)
            print(f"Estratégia de heap definida para: {estrategia}")

        elif opcao == 2:
            id = input("Digite o identificador para a alocação: ").strip()
            tamanho = int(input("Digite o tamanho do bloco a ser alocado: "))
            self.gerenciador.alocar(id, tamanho)

        elif opcao == 3:
            id = input("Digite o identificador para desalocar: ").strip()
            self.gerenciador.desalocar(id)

        elif opcao == 4:
            id1 = input("Digite o identificador de destino: ").strip()
            id2 = input("Digite o identificador de origem: ").strip()
            self.gerenciador.atribuir(id1, id2)

        elif opcao == 5:
            self.gerenciador.exibe()

        elif opcao == 6:
            print("Saindo do programa...")
            return False

        else:
            print("Opção inválida. Tente novamente.")
        return True

    def iniciar(self):
        continuar = True
        while continuar:
            self.exibir_menu()
            try:
                opcao = int(input("Digite a opção desejada: "))
                continuar = self.executar_opcao(opcao)
            except ValueError:
                print("Entrada inválida. Por favor, digite um número.")

if __name__ == "__main__":
    tamanho_heap = 40
    menu = MenuGerenciadorHeap(tamanho_heap)
    menu.iniciar()