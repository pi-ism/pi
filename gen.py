from chess import *
from chess.pgn import *
from chess.engine import *
from polyglot_writer import *
from chess.polyglot import *
from torch import nn, Tensor

engine = SimpleEngine.popen_uci('../stockfish/stockfish-ubuntu-x86-64-avx2')
board = Board()
game = Game()
positions = []

softmin = nn.Softmin()
FACTOR = .5
THRESHOLD = .01
ANALYSE_DEPTH = 20

def build(prob):
    print(f'build({board.fen()}, {prob:.2f})')

    if board.is_game_over(claim_draw=True): return

    scores, moves = [], []
    for move in board.legal_moves:
        board.push(move)
        score = engine.analyse(board, Limit(depth=ANALYSE_DEPTH))['score'].relative.score()
        scores.append(score * FACTOR)
        moves.append(move)
        board.pop()

    scores = Tensor(scores).to('cuda')
    probabilities = softmin(scores)

    for i, move in enumerate(moves):
        probability = probabilities[i]
        weight = int(probability / THRESHOLD)
        if prob * probability < THRESHOLD: continue
        board.push(move)
        build(prob * probability)
        board.pop()
        positions.append(Polyglot_Position(zobrist_hash(board), Polyglot_Move.from_chess_move(board, move), weight, 0)) 

build(1)

Polyglot_Writer.write(positions, 'null.bin')