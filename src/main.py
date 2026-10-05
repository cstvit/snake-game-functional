import sys
from pathlib import Path

# Adiciona o diretório 'src' ao sys.path para garantir resolução dos pacotes
sys.path.append(str(Path(__file__).resolve().parent))

import curses
import time
from core.model import UP, DOWN, LEFT, RIGHT
from core.game import create_initial_state, change_direction, step
from shell.render import draw_state

# Roda loop contínuo para capturar os comandos do teclado, atualizar o estado da cobra conforme o tempo passa e desenhar o resultado na tela do terminal.
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(0)

    max_y, max_x = stdscr.getmaxyx()
    state = create_initial_state(max_y, max_x)
    last_step_time = time.time()

    running = True

    while running:
        key = stdscr.getch()

        # Encerramento do jogo
        if key in (ord('q'), ord('Q')):
            running = False

        # Reinício da partida
        elif state.game_over and key in (ord('r'), ord('R')):
            max_y, max_x = stdscr.getmaxyx()
            state = create_initial_state(max_y, max_x, high_score=state.high_score)
            last_step_time = time.time()

        # Ciclo de execução
        else:
            if key == curses.KEY_RESIZE:
                new_y, new_x = stdscr.getmaxyx()
                state = state._replace(grid_rows=new_y, grid_cols=new_x)

            if not state.game_over:
                if key in (curses.KEY_UP, ord('w'), ord('W')):
                    state = change_direction(state, UP)
                elif key in (curses.KEY_DOWN, ord('s'), ord('S')):
                    state = change_direction(state, DOWN)
                elif key in (curses.KEY_LEFT, ord('a'), ord('A')):
                    state = change_direction(state, LEFT)
                elif key in (curses.KEY_RIGHT, ord('d'), ord('D')):
                    state = change_direction(state, RIGHT)

            current_time = time.time()
            if current_time - last_step_time >= state.speed:
                state = step(state)
                last_step_time = current_time

            draw_state(stdscr, state)
            time.sleep(0.01)

if __name__ == "__main__":
    curses.wrapper(main)