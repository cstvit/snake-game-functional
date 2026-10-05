import random
from typing import List
from core.model import (
    GameState, Point, RIGHT, wrap_around, check_self_collision
)

# Gera estado zerado do jogo, posicionando a cobra e a fruta na tela enquanto preserva o recorde anterior.
def create_initial_state(rows: int, cols: int, high_score: int = 0) -> GameState:
    initial_snake = [(rows // 2, cols // 2), (rows // 2, cols // 2 - 1)]
    initial_direction = RIGHT
    food = generate_food(initial_snake, rows, cols)
    return GameState(
        snake=initial_snake,
        direction=initial_direction,
        food=food,
        score=0,
        high_score=high_score,
        is_new_high_score=False,
        speed=0.15,
        game_over=False,
        grid_rows=rows,
        grid_cols=cols
    )

# Escolhe aleatoriamente uma posição vazia no tabuleiro para colocar a fruta, garantindo que ela não apareça sobre o corpo da cobra.
def generate_food(snake: List[Point], rows: int, cols: int) -> Point:
    valid_positions = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if (r, c) not in snake
    ]
    return random.choice(valid_positions) if valid_positions else (0, 0)

# Valida nova direção informada e atualiza o estado do jogo, impedindo que a cobra faça curvas de 180 graus sobre si mesma.
def change_direction(state: GameState, new_direction: Point) -> GameState:
    opposite = (-state.direction[0], -state.direction[1])
    if new_direction == opposite or new_direction == state.direction:
        return state
    return state._replace(direction=new_direction)

# Calcula e devolve o próximo quadro do jogo, movimentando a cobra, tratando colisões, atualizando a pontuação ao comer a fruta e verificando o fim de jogo.
def step(state: GameState) -> GameState:
    if state.game_over:
        return state

    head_r, head_c = state.snake[0]
    dir_r, dir_c = state.direction

    new_head = wrap_around(
        (head_r + dir_r, head_c + dir_c),
        state.grid_rows,
        state.grid_cols
    )
    
    if check_self_collision(new_head, state.snake):
        return state._replace(game_over=True)

    if new_head == state.food:
        new_snake = [new_head] + state.snake
        new_score = state.score + 1
        new_speed = max(0.03, state.speed * 0.93)
        new_food = generate_food(new_snake, state.grid_rows, state.grid_cols)

        is_new_record = new_score > state.high_score
        updated_high_score = max(new_score, state.high_score)

        return state._replace(
            snake=new_snake,
            food=new_food,
            score=new_score,
            high_score=updated_high_score,
            is_new_high_score=is_new_record or state.is_new_high_score,
            speed=new_speed
        )

    new_snake = [new_head] + state.snake[:-1]
    return state._replace(snake=new_snake)