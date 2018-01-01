from classes.post.Post import Post
from classes.post.Leitura import Leitura
from classes.post.Escrita import Escrita
from classes.post.Desvio import Desvio

from excecoes.ConvercaoException import ConversaoException


class Conversor:
    contadorID = 0
    turing = None
    post = None
    
    def __init__(self, turing):
        self.turing = turing
        self.post = Post(turing.todosSimbolos)
        self.incrementarContador()
        self.incrementarContador()
        for estado in self.turing.estados:
            turing.estados[estado].equivalentePost = None
        for transicao in self.turing.transicoes:
            transicao.usada = False
            
        self.converter(self.turing.estadoInicial)
        
    def converter(self, estadoAtual):
        if(estadoAtual == None):
            return None
        
        transicao = self.encontraProximaTransicao(estadoAtual)
        # se houver retorno, significa que a transicao retornada deve ser transformada para POST
        if(transicao != None):
            if(estadoAtual.equivalentePost == None):
                estadoAtual.equivalentePost = Leitura(str(self.contadorID))
                self.incrementarContador()
            leitura = estadoAtual.equivalentePost
            if(transicao.estadoOrigem == transicao.estadoDestino):
                self.criaEquivalentePost(transicao, leitura, leitura)
                self.converter(estadoAtual)
                return
            if(transicao.estadoDestino.equivalentePost == None):
                self.converter(transicao.estadoDestino)
            self.criaEquivalentePost(transicao, leitura, transicao.estadoDestino.equivalentePost)
            return
                
        self.converter(self.getOrigemTransicaoNaoUsada())
            
    
    # Cria um conjunto de desvios, leituras e escritas equivalentes a transicao
    def criaEquivalentePost(self, transicao, leitura, destinoEscrita):
        if(transicao.movimento == 'D'):
            self.criaMovimentoDireita(leitura, transicao.simboloLido, transicao.simboloEscrito,
                                      destinoEscrita)
            return
        if(transicao.movimento == 'E'):
            print("***********")
            print(self.contadorID)
            self.criaMovimentoEsquerda(leitura, transicao.simboloLido, transicao.simboloEscrito,
                                       destinoEscrita)
    
    # cria o desvio e a instruçao de escrita e os adiciona, junto a leitura, a maquina de POST
    def criaMovimentoDireita(self, leitura, simboloLido, simboloEscrito, destinoEscrita):
        escrita = Escrita(str(self.contadorID), simboloEscrito, destinoEscrita)
        self.incrementarContador()
        desvio = Desvio(leitura, simboloLido, escrita)
        self.post.adicionarLeitura(leitura)
        self.post.adicionarEscrita(escrita)
        self.post.adicionarDesvio(desvio)

    #cria um conjunto de instruçoes de escrita e leitura, alem de desvios,
    #para simular o movimento a esquerda
    def criaMovimentoEsquerda(self, origem, simboloLido, simboloEscrito, destinoEscrita):
        
        #cria instrucoes e desvios auxiliares que irao encontrar um caracter
        # utilizado como identificador
        print(origem.id)
        print("acho que eu ja sabia disso")
        print(destinoEscrita.id)
        destinoBase = self.criaEstadosIdentificadores(destinoEscrita)
        escrita = Escrita(str(self.contadorID), simboloEscrito, destinoBase)
        self.incrementarContador()
        self.post.adicionarEscrita(escrita)
        escritaIdentificador = Escrita(str(self.contadorID), self.post.identificadorEsquerda,
                                       escrita)
        self.post.adicionarEscrita(escritaIdentificador)
        if (origem.id != destinoEscrita.id):
            desvio = Desvio(origem, simboloLido, escritaIdentificador)
            self.post.adicionarDesvio(desvio)
        else:
            desvioCujoDestinoEhOrigem = self.buscaDesvioPorSimboloEOrigem(simboloLido, destinoBase)
            desvio = Desvio(desvioCujoDestinoEhOrigem.destino, self.post.identificadorEsquerda, escritaIdentificador)
            self.post.adicionarDesvio(desvio)
            

        print(escritaIdentificador.id)
        self.incrementarContador()
        
        
        
        
        
        
        
    def criaEstadosIdentificadores(self, destinoEscrita):
        leituraBase = Leitura(str(self.contadorID))
        self.incrementarContador()
        self.post.adicionarLeitura(leituraBase)
        
        vetorLeiturasAux = {}
        for letra in self.post.alfabeto:
            leitura = Leitura(str(self.contadorID))
            self.incrementarContador()
            self.post.adicionarLeitura(leitura)
            desvio = Desvio(leituraBase, letra, leitura)
            self.post.adicionarDesvio(desvio)
            vetorLeiturasAux[letra] = leitura
        
        for letraLeituraAux in vetorLeiturasAux:
            for l in self.post.alfabeto:
                escrita = Escrita(str(self.contadorID), letraLeituraAux,
                                  vetorLeiturasAux[l])
                self.incrementarContador()
                self.post.adicionarEscrita(escrita)
                desvio = Desvio(vetorLeiturasAux[letraLeituraAux], l, escrita)
                self.post.adicionarDesvio(desvio)
            
            desvioEquivalente = self.buscaDesvioPorSimboloEOrigem(letraLeituraAux, destinoEscrita)
            if(desvioEquivalente != None) :
                desvio = Desvio(vetorLeiturasAux[letraLeituraAux], self.post.identificadorEsquerda,
                                desvioEquivalente.destino)
                self.post.adicionarDesvio(desvio)
                print("aqui")
                
        return leituraBase
    
    
    # retorna a primeira transicao encontrada que ainda nao foi transformada em POST
    # e a marca como usada
    def encontraProximaTransicao(self, estado):
        for transicao in self.turing.transicoes:
            if(not(transicao.usada) and transicao.estadoOrigem == estado):
                transicao.usada = True
                return transicao
            
        return None
    
    #retorna o primeiro estado encontrado de forma que tal estado seja origem de uma transicao
    #ainda nao transformada para POST
    def getOrigemTransicaoNaoUsada(self):
        for transicao in self.turing.transicoes:
            if(not(transicao.usada)):
                return transicao.estadoOrigem
        
        return None

    def buscaDesvioPorSimboloEOrigem(self, simbolo, origem):
        for desvio in self.post.desvios:
            if(desvio.origem.id == origem.id and desvio.simbolo == simbolo):
                return desvio
        return None
        
    def incrementarContador(self):
        if(self.contadorID == 20):
            d = self.buscaDesvioPorSimboloEOrigem(self.post.identificadorEsquerda, self.post.escritas[str(self.contadorID - 1)])
            if(d == None):
                print("Escrita")
        self.contadorID += 1


    

    
