import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import random
import numpy as np

# Cores
VERMELHO_CLARO = '#FF6347'  # Tomato Red
AZUL_ESCURO = '#00008B'     # Dark Blue

# Plano de fundo
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #fff0f0, #ffeaea);
    }
    div.stButton > button:first-child {
        background-color: #FF6347;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
    }
    div.stButton > button:hover {
        background-color: #e5533d;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Estado da sessão
if "resposta_correta" not in st.session_state:
    st.session_state.resposta_correta = None
if "resposta_clicada" not in st.session_state:
    st.session_state.resposta_clicada = None

# Criando o grafo
pista = nx.Graph()
checkpoints = [f'Checkpoint {i}' for i in range(1, 11)]
pista.add_nodes_from(checkpoints)

arestas = [
    ('Checkpoint 1', 'Checkpoint 2', 3),
    ('Checkpoint 1', 'Checkpoint 3', 1),
    ('Checkpoint 2', 'Checkpoint 3', 1),
    ('Checkpoint 2', 'Checkpoint 4', 4),
    ('Checkpoint 3', 'Checkpoint 4', 1),
    ('Checkpoint 4', 'Checkpoint 5', 2),
    ('Checkpoint 5', 'Checkpoint 6', 3),
    ('Checkpoint 6', 'Checkpoint 7', 2),
    ('Checkpoint 7', 'Checkpoint 8', 4),
    ('Checkpoint 8', 'Checkpoint 9', 1),
    ('Checkpoint 9', 'Checkpoint 10', 2),
    ('Checkpoint 6', 'Checkpoint 9', 3),
    ('Checkpoint 3', 'Checkpoint 7', 5),
    ('Checkpoint 2', 'Checkpoint 8', 6),
]
for origem, destino, peso in arestas:
    pista.add_edge(origem, destino, weight=peso)

# Posição oval
def gerar_posicoes_ovais(pontos, centro=(0, 0), raio_x=10, raio_y=5):
    angulos = np.linspace(0, 2 * np.pi, len(pontos) + 1)[:-1]
    return {
        ponto: (centro[0] + raio_x * np.cos(ang), centro[1] + raio_y * np.sin(ang))
        for ponto, ang in zip(pontos, angulos)
    }

posicoes = gerar_posicoes_ovais(checkpoints, centro=(0, 0), raio_x=10, raio_y=5)

# Interface
st.markdown(f"<h1 style='color:{VERMELHO_CLARO}'>🏎️ Jogo: Qual é o Caminho do Dijkstra?</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='color:{VERMELHO_CLARO}'>Escolha os checkpoints e tente adivinhar o caminho mais curto!</h3>", unsafe_allow_html=True)

st.markdown(f"<h4 style='color:{VERMELHO_CLARO}'>Escolha os checkpoints:</h4>", unsafe_allow_html=True)
col_inicio, col_meio, col_fim = st.columns(3)
with col_inicio:
    ponto_inicio = st.selectbox("🏁 Partida", checkpoints)
with col_meio:
    ponto_intermediario = st.selectbox("🛑 Intermediário (opcional)", ["Nenhum"] + checkpoints)
with col_fim:
    ponto_final = st.selectbox("🏁 Chegada", checkpoints)

# Mostra o grafo
fig, ax = plt.subplots(figsize=(10, 6))
nx.draw_networkx_edges(pista, posicoes, ax=ax, edge_color='gray', width=6)
nx.draw_networkx_nodes(
    pista, posicoes, ax=ax,
    node_color=AZUL_ESCURO, node_size=1600, edgecolors='black'
)
nx.draw_networkx_labels(
    pista, posicoes, ax=ax,
    font_size=10, font_weight='bold', font_color=VERMELHO_CLARO
)
nx.draw_networkx_edge_labels(
    pista, posicoes, edge_labels=nx.get_edge_attributes(pista, 'weight'),
    font_color=VERMELHO_CLARO, font_size=9, ax=ax
)
ax.set_facecolor("#FFF8F8")
ax.set_axis_off()
st.pyplot(fig)

# Sidebar com dica
st.sidebar.markdown("""
    <div style='background-color:#000000; padding:15px; border-radius:10px; box-shadow: 0 0 10px rgba(0,0,0,0.1)'>
        <h3 style='color:#FF6347'>💡 Dica: Como funciona o Dijkstra?</h3>
        <p style='color:white;'>O algoritmo calcula o <b>menor caminho</b> somando os pesos (valores) das conexões entre os checkpoints.</p>
        <hr style="border:1px solid #FF6347">
        <b style='color:white;'>Exemplo:</b><br>
        <span style='color:white;'>- Checkpoint 1 ➡️ 3 (peso 1)<br>
        - Checkpoint 3 ➡️ 4 (peso 1)<br>
        - Checkpoint 4 ➡️ 5 (peso 2)<br>
        Total = 1 + 1 + 2 = <b>4</b><br><br>
        Escolha o caminho com <b>menor soma!</b></span>
    </div>
""", unsafe_allow_html=True)

# Botão para desafio
if st.button("🎯 Gerar Desafio"):
    if ponto_inicio == ponto_final:
        st.warning("Escolha dois checkpoints diferentes!")
    else:
        try:
            if ponto_intermediario != "Nenhum":
                caminho1 = nx.dijkstra_path(pista, ponto_inicio, ponto_intermediario, weight='weight')
                caminho2 = nx.dijkstra_path(pista, ponto_intermediario, ponto_final, weight='weight')
                caminho_correto = caminho1[:-1] + caminho2
            else:
                caminho_correto = nx.dijkstra_path(pista, ponto_inicio, ponto_final, weight='weight')

            peso_correto = sum(
                pista[caminho_correto[i]][caminho_correto[i + 1]]["weight"]
                for i in range(len(caminho_correto) - 1)
            )

            todos_os_caminhos = list(nx.all_simple_paths(pista, ponto_inicio, ponto_final, cutoff=10))
            alternativas_erradas = []
            for caminho in todos_os_caminhos:
                if caminho != caminho_correto:
                    peso = sum(
                        pista[caminho[i]][caminho[i + 1]]["weight"]
                        for i in range(len(caminho) - 1)
                    )
                    if peso > peso_correto:
                        alternativas_erradas.append(caminho)

            if alternativas_erradas:
                caminho_errado = random.choice(alternativas_erradas)
            else:
                caminho_errado = caminho_correto[::-1]

            opcoes = [caminho_correto, caminho_errado]
            random.shuffle(opcoes)
            st.session_state.opcoes = opcoes
            st.session_state.resposta_correta = caminho_correto
            st.session_state.resposta_clicada = None
        except nx.NetworkXNoPath:
            st.error("Não há caminho entre os checkpoints selecionados.")

# Mostra as opções
if "opcoes" in st.session_state and st.session_state.resposta_correta:
    st.markdown(f"<h3 style='color:{VERMELHO_CLARO}'>Qual desses caminhos foi calculado com Dijkstra?</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    def mostrar_botao(caminho, coluna, chave):
        texto = " ➡️ ".join(caminho)
        cor = "lightgray"
        if st.session_state.resposta_clicada is not None:
            if caminho == st.session_state.resposta_correta:
                cor = "#4CAF50"
            elif caminho == st.session_state.resposta_clicada:
                cor = "#f44336"
        if coluna.button(texto, key=chave):
            if st.session_state.resposta_clicada is None:
                st.session_state.resposta_clicada = caminho
                st.rerun()

        html = f"""
        <div style='padding:10px;border-radius:8px;margin-top:10px;background-color:{cor};text-align:center;font-weight:bold'>
            <span style='color:{VERMELHO_CLARO}'>{texto}</span>
        </div>
        """
        if st.session_state.resposta_clicada is not None:
            coluna.markdown(html, unsafe_allow_html=True)

    mostrar_botao(st.session_state.opcoes[0], col1, "opcao1")
    mostrar_botao(st.session_state.opcoes[1], col2, "opcao2")

    if st.session_state.resposta_clicada is not None:
        if st.session_state.resposta_clicada == st.session_state.resposta_correta:
            st.success("🎉 Parabéns! Você acertou o caminho calculado com Dijkstra.", icon="✅")
        else:
            st.error("🚫 Opa! Esse não era o caminho com Dijkstra.", icon="❌")
