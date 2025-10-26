"""
Módulo que define excepciones personalizadas para el juego de Backgammon.
"""


class BackgammonException(Exception):
    """Excepción base para errores del juego de Backgammon."""


class InvalidMoveException(BackgammonException):
    """Excepción para movimientos inválidos."""


class OutOfBoundsException(BackgammonException):
    """Excepción para movimientos fuera de los límites del tablero."""


class InsufficientDiceException(BackgammonException):
    """Excepción para cuando no hay dados disponibles para un movimiento."""


class NoPiecesException(BackgammonException):
    """Excepción para cuando no hay fichas para mover."""
