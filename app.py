import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Criando o mapa da pista de corrida
pista = nx.Graph()

# Cidades (ou pontos da pista)
pista.add_nodes_from(['Ponto 1', 'Ponto 2', 'Ponto 3', 'Ponto 4', 'Ponto 5'])

# Ligação entre os pontos e as distâncias
pista.add_edge('Ponto 1', 'Ponto 2', weight=3)
pista.add_edge('Ponto 1', 'Ponto 3', weight=3)
pista.add_edge('Ponto 2', 'Ponto 3', weight=1)
pista.add_edge('Ponto 2', 'Ponto 4', weight=4)
pista.add_edge('Ponto 3', 'Ponto 4', weight=1)
pista.add_edge('Ponto 4', 'Ponto 5', weight=2)

# Localização dos pontos no mapa (pra manter o desenho fixo)
posicoes = {
    'Ponto 1': (0, 1),
    'Ponto 2': (1, 2),
    'Ponto 3': (2, 1),
    'Ponto 4': (3, 2),
    'Ponto 5': (4, 1)
}

# Título do site
st.title("Corrida Estratégica - Caminho Mais Curto 🚗💨")
st.subheader("Escolha onde começa e onde termina a corrida:")

# Escolha dos pontos pelo usuário
ponto_inicio = st.selectbox("Ponto de Largada", list(pista.nodes))
ponto_final = st.selectbox("Ponto de Chegada", list(pista.nodes))

# Mostra o mapa da pista sempre
figura, desenho = plt.subplots()
nx.draw(pista, posicoes, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray', ax=desenho)
nomes_das_distancias = nx.get_edge_attributes(pista, 'weight')
nx.draw_networkx_edge_labels(pista, posicoes, edge_labels=nomes_das_distancias, ax=desenho)
st.pyplot(figura)

# Quando clicar no botão, mostra o melhor caminho
if st.button("Mostrar Melhor Caminho"):
    if ponto_inicio != ponto_final:
        melhor_caminho = nx.dijkstra_path(pista, ponto_inicio, ponto_final, weight='weight')
        st.success(f"Caminho ideal: {' ➡️ '.join(melhor_caminho)}")

        # Redesenha o mapa com o caminho destacado
        figura, desenho = plt.subplots()
        nx.draw(pista, posicoes, with_labels=True, node_color='skyblue', node_size=800, edge_color='gray', ax=desenho)
        nx.draw_networkx_edge_labels(pista, posicoes, edge_labels=nomes_das_distancias, ax=desenho)

        caminho_em_vermelho = list(zip(melhor_caminho, melhor_caminho[1:]))
        nx.draw_networkx_edges(pista, posicoes, edgelist=caminho_em_vermelho, width=4, edge_color='red', ax=desenho)
        st.pyplot(figura)
    else:
        st.warning("Escolha pontos diferentes para traçar a rota.")