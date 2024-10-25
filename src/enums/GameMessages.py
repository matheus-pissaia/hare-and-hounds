from enum import Enum


class GameMessages(Enum):
    WELCOME = "Bem vindo ao jogo Hare and Hounds!"
    START_DRAG = "Arraste e solte a peça para começar"
    INVALID_MOVE = "Movimento inválido!"
    INVALID_PIECE = "A peça escolhida não é sua!"
    YOUR_TURN = "Sua vez! Arraste e solte a peça para a posição desejada."
    WAITING_OPPONENT = "Esperando oponente..."
    YOU_WIN = "Voce venceu!"
    YOU_LOSE = "Voce perdeu :("
    ABANDONED = "O oponente abandonou a partida!"
