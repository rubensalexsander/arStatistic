#Classes Conjunto
class Conjunto:
    def __init__(self, dados_iniciais=[], amostra=True, descricao=""):
        self.dados = dados_iniciais
        self.amostra = amostra
        self.descricao = descricao
    
    #Retorna dados brutos
    def Brutos(self):
        dadost = self.dados[:]
        dadost.sort()
        return dadost

    #Retorna dados ponderados
    def Ponderados(self):
        xi = []
        fi = []
        for i in self.dados:
            if not i in xi: 
                xi.append(i)
                fi.append(self.dados.count(i))
        xi.sort()

        Fi = []
        sumfi = 0
        for i in fi:
            sumfi += i
            Fi.append(sumfi)

        fri = [i/sumfi for i in fi]
        
        sumFri = 0
        Fri = []
        for i in fri:
            sumFri += i
            Fri.append(sumFri)
        
        return [xi, fi, fri, Fi, Fri]

    #Retorna dados em intervalo de classes
    def Intervalos(self):
        pass

    """#Retorna dados em rol
    def Rol(self):
        self.dados[:].sort()
        return dados"""

    #Retorna média Aritmética
    def Mx(self):
        sumXi = 0
        n = len(self.dados)
        for i in self.dados:
            sumXi += i
        return sumXi/n

    #Retorna média Geométrica
    def Mg(self):
        n = len(self.dados)
        multdados = 1
        for i in self.dados:
            multdados *= i
        return multdados ** (1/n)

    #Retorna média Harmônica
    def Mh(self):
        n = len(self.dados)
        sum1sobreXi = 0
        for i in self.dados:
            if i == 0:
                pass
            else:
                sum1sobreXi += (1/i)
        return n/sum1sobreXi

    #Retorna Amplitude H
    def H(self):
        if len(self.dados) > 0:
            li, ls = self.dados[0], self.dados[0]
            for i in self.dados:
                if i < li: li = i
                if i > ls: ls = i
            return ls - li

    #Retorna dados modais
    def Mo(self):
        if len(self.dados) > 0:
            list_itens = []
            for i in self.dados:
                if not i in list_itens:
                    list_itens.append(i)

            list_itens_fi = [[self.dados.count(i), i] for i in list_itens]
            list_itens_fi.sort()
            moda = [list_itens_fi[0]]
            
            for i in list_itens_fi:
                if i[0] > moda[0][0]:
                    moda = [i]
                elif i[0] == moda[0][0]:
                    moda.append(i)
            
            if len(moda) <= 2:
                return [i[1] for i in moda]

    #Retorna mediana
    def Me(self):
        def par(n): 
            if not int(n/2) < n/2: return True
        n = len(self.dados)
        self.dados.sort()
        if par(n):
            to_mean = Conjunto([self.dados[int(n/2)-1], self.dados[int(n/2)]])
            me = to_mean.Mx()
        else:
            me = float(self.dados[int((n+1)/2)-1])
        return me

    #Retorna Variância Var
    def Var(self):
        sumXimenosMxaoquad = 0
        Mx = self.Mx()
        n = len(self.dados)
        for i in self.dados:
            sumXimenosMxaoquad += ((i-Mx)**2)
        if not self.amostra:
            return sumXimenosMxaoquad/n
        return sumXimenosMxaoquad/(n-1)

    #Retorna Desvio-padrão DP
    def DP(self):
        return self.Var()**(1/2)

    #Retorna Coeficiênte de variação CV
    def CV(self):
        return self.DP()/self.Mx()

    def add(self, dados):
        self.dados += dados
    
    def Dados(self, tipo='brutos'):
        if tipo == 'brutos':
            return self.Brutos()

        elif tipo == 'ponderados':
            return self.Ponderados()

#Funções regressão linear
#Retorna covariância
def getCOV(dadosx, dadosy):
    mx = dadosx.Mx()
    my = dadosy.Mx()

    sumximenosxmvezesyimenosym = 0
    for i in range(len(dadosx)):
        sumximenosxmvezesyimenosym += (dadosx[i]-mx)*(dadosy[i]-my)
    return sumximenosxmvezesyimenosym/len(dadosx)

#Retorna correlação linear
def R(dadosx, dadosy):
    return getCOV(dadosx, dadosy)/(dadosx.DP()*dadosy.DP())

#Retorna variáveis a e b da equação linear (y = a+bx)
def getAb(dadosx, dadosy):
    b = getCOV(dadosx, dadosy) / dadosx.Var()
    a = dadosy.Mx() - (b*dadosx.Mx())

    return a, b

#Classe regressão linear simples
class RegressionL():
    def __init__(self, dadosx=[], dadosy=[]):
        self.dadosx = dadosx
        self.dadosy = dadosy
        self.fit(dadosx, dadosy)

    #Adiciona valores aos dados principais
    def fit(self, dadosx, dadosy):
        if len(dadosx)==0 or len(dadosy)==0: return None
        self.dadosx += dadosx
        self.dadosy += dadosy
        self.a, self.b = getAb(self.dadosx, self.dadosy)

    #Retorna a estimativa calculada
    def predict(self, x): 
        return [self.a + (self.b * i) for i in x]

if __name__ == '__main__':
    dadosx = [5, 10, 15, 3, 5, 15, 14, 20, 25]

    conjX = Conjunto(dadosx)
    
    print(conjX.Me())
