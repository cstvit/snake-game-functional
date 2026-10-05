import pytest
from core.model import (
    GameState, Point, UP, DOWN, LEFT, RIGHT, wrap_around, check_self_collision
)
from core.game import (
    create_initial_state, generate_food, change_direction, step
)

# ==============================================================================
# 1. TESTES DE INICIALIZAÇÃO E GEOMETRIA (model.py / game.py)
# ==============================================================================

# Verifica se o estado inicial é construído com os valores padrão corretos.
def test_create_initial_state_defaults():
    state = create_initial_state(rows=20, cols=20, high_score=15)

    assert state.score == 0
    assert state.high_score == 15
    assert state.direction == RIGHT
    assert state.game_over is False
    assert state.is_new_high_score is False
    assert len(state.snake) == 2
    assert state.snake[0] == (10, 10)  # Centro da tela
    assert state.food not in state.snake  # Comida não pode nascer sobre a cobra

# Testa o transporte contínuo nas bordas.
def test_wrap_around_boundaries():
    grid_rows, grid_cols = 10, 10

    # Atravessar a borda direita -> deve voltar para a coluna 0
    assert wrap_around((5, 10), grid_rows, grid_cols) == (5, 0)
    # Atravessar a borda esquerda -> deve ir para a última coluna (9)
    assert wrap_around((5, -1), grid_rows, grid_cols) == (5, 9)
    # Atravessar a borda inferior -> deve voltar para a linha 0
    assert wrap_around((10, 5), grid_rows, grid_cols) == (0, 5)
    # Atravessar a borda superior -> deve ir para a última linha (9)
    assert wrap_around((-1, 5), grid_rows, grid_cols) == (9, 5)

# Garante que a comida gerada nunca ocupe a posição do corpo da cobra.
def test_generate_food_never_on_snake():
    rows, cols = 5, 5
    # Cobra ocupando quase o tabuleiro inteiro
    snake = [(0, 0), (0, 1), (0, 2), (0, 3)]
    
    for _ in range(20):  # Testa várias vezes devido ao caráter aleatório
        food = generate_food(snake, rows, cols)
        assert food not in snake

# ==============================================================================
# 2. TESTES DE MUDANÇA DE DIREÇÃO (change_direction)
# ==============================================================================

# Garante que viradas válidas de 90 graus alteram a direção
def test_change_direction_valid():
    state = create_initial_state(rows=10, cols=10) # Direção inicial é RIGHT
    
    state_up = change_direction(state, UP)
    assert state_up.direction == UP

    state_down = change_direction(state, DOWN)
    assert state_down.direction == DOWN

# Garante que a cobra não pode inverter 180 graus sobre o próprio corpo
def test_change_direction_prevents_180_degree_turn():
    state = create_initial_state(rows=10, cols=10) # Direção inicial é RIGHT

    # Tentar virar para LEFT (oposto direto) deve ser ignorado
    state_invalid = change_direction(state, LEFT)
    assert state_invalid.direction == RIGHT

# Manter a mesma direção não altera o estado.
def test_change_direction_same_direction_is_noop():
    state = create_initial_state(rows=10, cols=10)
    assert change_direction(state, RIGHT) == state

# ==============================================================================
# 3. TESTES DE EVOLUÇÃO TEMPORAL E REGRAS DO JOGO (step)
# ==============================================================================

# Verifica o movimento simples da cobra em um tick.
def test_step_moves_snake_forward():
    state = create_initial_state(rows=10, cols=10)
    head_r, head_c = state.snake[0]

    # Força a fruta para longe para testar apenas o movimento sem colisão/comida
    state = state._replace(food=(0, 0))
    next_state = step(state)

    # A cabeça deve ter avançado uma casa para a direita
    assert next_state.snake[0] == (head_r, head_c + 1)
    # O tamanho do corpo deve permanecer o mesmo
    assert len(next_state.snake) == len(state.snake)

# Testa consumo de fruta: ganha 1 ponto, cobra cresce e fruta regenera
def test_step_eating_food_increases_score_and_length():
    state = create_initial_state(rows=10, cols=10, high_score=5)
    head_r, head_c = state.snake[0]
    dir_r, dir_c = state.direction

    # Coloca a fruta exatamente no próximo passo da cabeça
    target_food = (head_r + dir_r, head_c + dir_c)
    state_with_food = state._replace(food=target_food)

    next_state = step(state_with_food)

    assert next_state.score == 1
    assert len(next_state.snake) == len(state.snake) + 1
    assert next_state.snake[0] == target_food
    assert next_state.food != target_food  # Nova fruta foi gerada

# Verifica se o recorde é atualizado ao superar o high_score anterior.
def test_step_high_score_update():
    state = create_initial_state(rows=10, cols=10, high_score=0)
    head_r, head_c = state.snake[0]
    
    target_food = (head_r, head_c + 1)
    state = state._replace(food=target_food)

    next_state = step(state)

    assert next_state.score == 1
    assert next_state.high_score == 1
    assert next_state.is_new_high_score is True

# Testa a colisão da cabeça com o próprio corpo gerando Game Over.
def test_step_self_collision_triggers_game_over():
    # Configura uma cobra de tamanho 5 dando volta sobre si mesma
    # Cabeça em (2, 2) movendo-se para a LEFT, onde o corpo está em (2, 1)
    snake = [(2, 2), (2, 3), (1, 3), (1, 1), (2, 1)]
    state = GameState(
        snake=snake,
        direction=LEFT,
        food=(0, 0),
        score=5,
        high_score=10,
        is_new_high_score=False,
        speed=0.15,
        game_over=False,
        grid_rows=10,
        grid_cols=10
    )

    next_state = step(state)

    assert next_state.game_over is True

#  Se o jogo já está em Game Over, o step não deve alterar o estado.
def test_step_when_game_over_is_noop():
    state = create_initial_state(rows=10, cols=10)._replace(game_over=True)
    assert step(state) == state