#Retorna dados brutos
def getBrutos(dados):
    dadost = dados[:]
    dadost.sort()
    return dadost

#Retorna dados ponderados
def getPonderados(dados):
    xi = []
    fi = []
    for i in dados:
        if not i in xi: 
            xi.append(i)
            fi.append(dados.count(i))
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
def getIntervalos(dados):
    pass

#Retorna dados em rol
def getRol(dados):
    dados[:].sort()
    return dados

#Retorna média Aritmética
def getMx(dados, floats=10):
    sumXi = 0
    n = len(dados)
    for i in dados:
        sumXi += i
    return round(sumXi/n, floats)

#Retorna média Geométrica
def getMg(dados, floats=10):
    n = len(dados)
    multdados = 1
    for i in dados:
        multdados *= i
    return round(multdados ** (1/n), floats)

#Retorna média Harmônica
def getMh(dados, floats=10):
    n = len(dados)
    sum1sobreXi = 0
    for i in dados:
        if i == 0:
            pass
        else:
            sum1sobreXi += (1/i)
    return round(n/sum1sobreXi, floats)

#Retorna Amplitude H
def getH(dados):
    if len(dados) > 0:
        li, ls = dados[0], dados[0]
        for i in dados:
            if i < li: li = i
            if i > ls: ls = i
        return ls - li

#Retorna dados modal
def getMo(dados):
    if len(dados) > 0:
        list_itens = []
        for i in dados:
            if not i in list_itens:
                list_itens.append(i)

        list_itens_fi = [[dados.count(i), i] for i in list_itens]
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
def getMe(dados):
    def par(n): 
        if not int(n/2) < n/2: return True
    n = len(dados)
    dados.sort()
    if par(n):
        me = getMx([dados[int(n/2)-1], dados[int((n/2)+1-1)]])
    else:
        me = dados[int((n+1)/2)-1]
    return me

#Retorna Variância Var
def getVar(dados, amostra=False, floats=10):
    sumXimenosMxaoquad = 0
    Mx = getMx(dados)
    n = len(dados)
    for i in dados:
        sumXimenosMxaoquad += ((i-Mx)**2)
    if not amostra:
        return round(sumXimenosMxaoquad/n, floats)
    return round(sumXimenosMxaoquad/(n-1), floats)

#Retorna Desvio-padrão DP
def getDP(dados, amostra=False, floats=10):
    return round(getVar(dados, amostra, floats)**(1/2), floats)

#Retorna Coeficiênte de variação CV
def getCV(dados, amostra=False, floats=10):
    return round(getDP(dados, amostra, floats)/getMx(dados), floats)

#Classes Conjunto
class Conjunto:
    def __init__(self, dados_iniciais=[], amostra=False, descricao=""):
        self.dados = dados_iniciais
        self.amostra = amostra
        self.descricao = descricao
        self.update()

    def update(self):
        if len(self.dados) == 0: return None

        #Define n
        self.n = len(self.dados)

        #Define Mx
        self.Mx = getMx(self.dados)

        #Define Mg
        self.Mg = getMg(self.dados)

        #Define Mh
        self.Mh = getMh(self.dados)

        #Define H
        self.H = getH(self.dados)

        #Define Mo
        self.Mo = getMo(self.dados)

        #Define Me
        self.Me = getMe(self.dados)

        #Define Var
        self.Var = getVar(self.dados, amostra=self.amostra)

        #Define DP
        self.DP = getDP(self.dados, amostra=self.amostra)

        #Define CV
        self.CV = getCV(self.dados, amostra=self.amostra)

    def add(self, dados):
        self.dados += dados
        self.update()
    
    def getDados(self, tipo='brutos'):
        if tipo == 'brutos':
            return getBrutos(self.dados)

        elif tipo == 'ponderados':
            return getPonderados(self.dados)

#Funções regressão linear
#Retorna covariância
def getCOV(dadosx, dadosy):
    mx = getMx(dadosx)
    my = getMx(dadosy)

    sumximenosxmvezesyimenosym = 0
    for i in range(len(dadosx)):
        sumximenosxmvezesyimenosym += (dadosx[i]-mx)*(dadosy[i]-my)
    return sumximenosxmvezesyimenosym/len(dadosx)

#Retorna correlação linear
def getR(dadosx, dadosy):
    return getCOV(dadosx, dadosy)/(getDP(dadosx)*getDP(dadosy))

#Retorna variáveis a e b da equação linear (y = a+bx)
def getAb(dadosx, dadosy):
    b = getCOV(dadosx, dadosy) / getVar(dadosx)
    a = getMx(dadosy) - (b*getMx(dadosx))

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
    dadosx = [5, 10, 15, 20, 25]
    dadosy = [10, 13, 18, 26, 40]

    regressao1 = RegressionL()
    regressao1.fit(dadosx, dadosy)

    print(regressao1.predict([20]))

