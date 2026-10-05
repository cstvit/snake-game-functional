# Snake Game — Pure Functional Core & Imperative Shell

Este projeto consiste na implementação do clássico jogo Snake em Python, desenvolvido como requisito para a disciplina de Programação Funcional.
A arquitetura do projeto foi desenhada estritamente sobre a política Functional Core / Imperative Shell, garantindo a total separação entre regras de negócio puras (sem efeitos colaterais) e os mecanismos de entrada/saída (I/O).

## Arquitetura do Projeto

A aplicação segue uma divisão clara entre lógica imutável e infraestrutura de terminal.

## Princípios de Programação Funcional Aplicados

1. Functional Core / Imperative Shell
- Functional Core (src/core/): Concentra 100% da lógica de negócio. As funções aqui contidas são totalmente puras e determinísticas: para as mesmas entradas, sempre retornam exatamente as mesmas saídas, sem ler nem modificar qualquer estado global.

- Imperative Shell (src/shell/ e src/main.py): Atua na borda da aplicação. Gerencia efeitos colaterais (Side Effects) como captura de teclado, tempo do sistema (time.time()) e renderização no terminal via curses.

2. Imutabilidade e Transições de Estado
- O estado do jogo é representado pela estrutura imutável GameState (uma NamedTuple).

- O estado nunca é alterado diretamente. Em vez disso, funções de transição de estado como step(state) e change_direction(state, dir) tomam o estado atual, aplicam as regras de transformação e devolvem um novo objeto GameState (state._replace(...)).

## Responsabilidade dos Módulos

### core/model.py
Define os tipos imutáveis e primitivos geométricos puros:

- GameState: Declaração do estado imutável da aplicação.

- wrap_around: Função matemática que calcula o transporte continuo nas bordas (geometria toroidal).

- check_self_collision: Predicado para verificar colisão da cabeça com o corpo.

### core/game.py
Implementa o motor puramente funcional e as regras do jogo:

- create_initial_state: Fabrica o estado inicial zerado mantendo o recorde.

- generate_food: Função pura que calcula posições válidas disponíveis no grid.

- change_direction: Valida e aplica novos vetores de direção sem permitir inversão de 180°.

- step: Função de evolução temporal. Dado o tick, calcula deslocamento, colisão, consumo de fruta, pontuação e condição de Game Over.

### shell/render.py & main.py
A casca imperativa que conecta o usuário ao motor:

- draw_state: Desenha os elementos (O, o, *, HUD e pop-ups) no terminal com base no GameState recebido.

- main: Roda o Event Loop contínuo, captura entradas de teclado, controla a cadência dos quadros e gerencia o ciclo de vida do terminal.

## Como Executar

Pré-requisitos
Python 3.8+

Dependência de terminal para Windows (caso esteja executando em ambiente Windows):

```bash
pip install windows-curses
```

Rodando o Jogo
A partir do diretório raiz do projeto:

```bash
python src/main.py
```

## Comandos de Jogo

- Setas ou W / A / S / D: Alteram a direção da cobra.

- R: Reinicia a partida após o Game Over.

- Q: Sai do jogo com encerramento seguro do terminal.
