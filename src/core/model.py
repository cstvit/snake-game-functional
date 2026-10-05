from typing import NamedTuple, List, Tuple

Point = Tuple[int, int]

# Vetores de direção no formato curses: (linha, coluna)
UP: Point = (-1, 0)
DOWN: Point = (1, 0)
LEFT: Point = (0, -1)
RIGHT: Point = (0, 1)

class GameState(NamedTuple):
    snake: List[Point]
    direction: Point
    food: Point
    score: int
    high_score: int
    is_new_high_score: bool
    speed: float
    game_over: bool
    grid_rows: int
    grid_cols: int

# Calcula a navegação em borda infinita, fazendo a cobra reaparecer no lado oposto do tabuleiro sempre que ela atravessa um dos limites da tela.
def wrap_around(position: Point, rows: int, cols: int) -> Point:
    r, c = position
    return (r % rows, c % cols)

# Verifica se a coordenada da cabeça da cobra coincide com qualquer parte do seu próprio corpo, indicando se houve uma colisão.
def check_self_collision(head: Point, body: List[Point]) -> bool:
    return head in body