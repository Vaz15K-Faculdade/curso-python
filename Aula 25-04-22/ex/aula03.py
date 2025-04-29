import matplotlib.pyplot as plt  
import numpy as np

x = np.linspace(0, 10, 100)  
y = np.sin(x)  
plt.plot(x, y)  
plt.title("Gráfico de Seno")  
plt.xlabel("Eixo X")  
plt.ylabel("Eixo Y") 
plt.plot(x, y, color='red', linestyle='--', marker='o', label='Seno')  
plt.legend()
plt.savefig('./2025/analise de dados/00_grafico_seno.png')
plt.close() 


# Barras  
categorias = ['A', 'B', 'C', 'D']  
valores = [10, 25, 15, 30]  
plt.bar(categorias, valores, color='skyblue') 
plt.savefig('./2025/analise de dados/00_grafico_barras.png')
plt.close() 

# Dispersão  
x = np.random.rand(50)  
y = np.random.rand(50)  
plt.scatter(x, y, color='green', marker='x')  
plt.savefig('./2025/analise de dados/00_scatterplot.png')
plt.close()

# Dispersão com múltiplas variáveis
data = {'a': np.arange(50),
        'c': np.random.randint(0, 50, 50),
        'd': np.random.randn(50)}
data['b'] = data['a'] + 10 * np.random.randn(50)
data['d'] = np.abs(data['d']) * 100

plt.scatter('a', 'b', c='c', s='d', data=data)
plt.xlabel('entry a')
plt.ylabel('entry b')
plt.savefig('./2025/analise de dados/00_scatterplot2.png')
plt.close()

# Histograma
dados = np.random.randn(1000)  
plt.hist(dados, bins=20, color='purple', alpha=0.7)  
plt.savefig('./2025/analise de dados/00_histograma.png')
plt.close()



# Trabalhando com múltiplos gráficos
def f(t):
    return np.exp(-t) * np.cos(2*np.pi*t)

t1 = np.arange(0.0, 5.0, 0.1)
t2 = np.arange(0.0, 5.0, 0.02)

plt.figure()
plt.subplot(211)
plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

plt.subplot(212)
plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
plt.savefig('./2025/analise de dados/00_subplots.png')
plt.close()



# Trabalhando com texto

mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)

# Histograma
plt.hist(x, 50, density=True, facecolor='g', alpha=0.75)

plt.xlabel('QI')
plt.ylabel('Probabilidade')
plt.title('Histograma de QI')
plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
plt.axis([40, 160, 0, 0.03])
plt.grid(True)
plt.savefig('./2025/analise de dados/00_texto.png')
plt.close()


# Anotações

ax = plt.subplot()

t = np.arange(0.0, 5.0, 0.01)
s = np.cos(2*np.pi*t)
line, = plt.plot(t, s, lw=2)

plt.annotate('local max', xy=(2, 1), xytext=(3, 1.5),
             arrowprops=dict(facecolor='black', shrink=0.05),
             )

plt.ylim(-2, 2)
plt.savefig('./2025/analise de dados/00_anotacoes.png')
plt.close()