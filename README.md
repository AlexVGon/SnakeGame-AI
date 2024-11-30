# Snake Game AI - Treinamento com Q-Learning

Este projeto é uma implementação simples de um agente inteligente para o clássico jogo da cobrinha (Snake Game), utilizando Q-Learning com redes neurais para aprender estratégias de movimentação e maximização de pontuação. O treinamento é conduzido em um ambiente simulado que o agente utiliza para aprimorar suas decisões com base em feedbacks (recompensas ou penalidades).

## Estrutura do Projeto

### 1. SnakeGameAI

O ambiente do jogo, implementado com Pygame, define as regras, o tabuleiro, e o comportamento da cobrinha. Ele fornece:

- Renderização do jogo com um design visual customizado (grid, comida, movimento da cobra).
- Movimentação e verificações de colisões e pontuação.
- Interface para o agente realizar ações e receber recompensas.

### 2. Agente Inteligente

O agente é responsável por tomar decisões no ambiente. Suas principais características incluem:

- **Estado do jogo:** Uma representação vetorial com informações sobre perigos, direção e localização da comida.
- **Decisões:** Movimentos baseados em exploração (ações aleatórias) ou exploração (previsões da rede neural).
- **Memória:** Uma fila de transições estado-ação-recompensa, utilizada para treinar o modelo.

### 3. Rede Neural Q-Learning

A rede neural, implementada com PyTorch, aprende a prever o melhor movimento para cada estado do jogo.

- **Modelo (Linear_QNet):** Rede simples com uma camada oculta para mapear os estados às ações (esquerda, frente, direita).
- **Treinamento (QTrainer):** Atualiza os pesos da rede para minimizar a perda entre os valores previstos e os alvos (baseados na fórmula Q-Learning).

### 4. Gráficos de Progresso

O progresso do treinamento é visualizado em tempo real:

- Pontuação por jogo.
- Pontuação média ao longo do tempo.

<hr />

## Resultado
<div> 
<pre>
                <b>Primeiras Gerações</b>                                 <b>Centésima Geração</b>
</pre>
<img src="https://github.com/AlexVGon/SnakeGame-AI/blob/main/assets/Initial.gif?raw=true" width="49%" align='left'> 
<img src="https://github.com/AlexVGon/SnakeGame-AI/blob/main/assets/Trained.gif?raw=true" width="49%" align='right'> 
</div>
