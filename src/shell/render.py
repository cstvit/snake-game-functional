import curses
from core.model import GameState

# Lê o estado imutável do jogo e pinta a cobra, a fruta, o placar e as mensagens de game over no terminal a cada quadro.
def draw_state(stdscr, state: GameState) -> None:
    stdscr.clear()

    def safe_addch(r: int, c: int, char: str, attr=curses.A_NORMAL):
        try:
            stdscr.addch(r, c, char, attr)
        except curses.error:
            pass

    def safe_addstr(r: int, c: int, text: str, attr=curses.A_NORMAL):
        try:
            stdscr.addstr(r, c, text, attr)
        except curses.error:
            pass

    # 1. Comida
    food_r, food_c = state.food
    safe_addch(food_r, food_c, "*", curses.A_BOLD)

    # 2. Cobra
    for i, (r, c) in enumerate(state.snake):
        char = "O" if i == 0 else "o"
        safe_addch(r, c, char)

    # 3. HUD (Placar)
    hud_str = f" Score: {state.score} | Recorde: {state.high_score} | Velocidade: {1 / state.speed:.1f}x | (Q: Sair) "
    safe_addstr(0, 0, hud_str, curses.A_REVERSE)

    # 4. Game Over
    if state.game_over:
        lines = [
            "==========================================",
            "               GAME OVER!                 ",
            f" Pontuação Final: {state.score}           ",
            f" Maior Recorde:   {state.high_score}      ",
        ]

        if state.is_new_high_score:
            lines.insert(3, " 🎉 NOVO RECORDE ALCANÇADO! 🎉 ")

        lines.extend([
            "------------------------------------------",
            "  Pressione 'R' para Jogar Novamente      ",
            "  Pressione 'Q' para Sair                 ",
            "==========================================",
        ])

        start_r = max(1, (state.grid_rows - len(lines)) // 2)

        for offset, line in enumerate(lines):
            c_pos = max(0, (state.grid_cols - len(line)) // 2)
            attr = curses.A_BOLD if "NOVO RECORDE" in line else curses.A_REVERSE
            safe_addstr(start_r + offset, c_pos, line, attr)

    stdscr.refresh()