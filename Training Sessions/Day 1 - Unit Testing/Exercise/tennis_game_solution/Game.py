from Player import Player
from DuplicatedPlayerError import DuplicatedPlayerError
from GameHasAlreadyBeenWonError import GameHasAlreadyBeenWonError


class Game:
    ADVANTAGE = 'Advantage'
    DEUCE = 'Deuce'
    SPACE = ' '
    DASH = '-'
    WINS = 'wins'

    def __init__(self, player_name_1: str, player_name_2: str):
        """
        Creates a game given the names of two players. At the beginning the two
        players have a score equal to zero.
        :param player_name_1:
        :param player_name_2:
        :raise DuplicatedPlayerError if the two players have the same name.
        """
        if player_name_1 == player_name_2:
            raise DuplicatedPlayerError

        self._player1 = Player(player_name_1, 0)
        self._player2 = Player(player_name_2, 0)
        self._game_status = ''
        self.update_game_status()

    @property
    def game_status(self) -> str:
        return self._game_status

    def get_player1_name(self) -> str:
        """
        Returns the name of the first player.
        :return: the name
        """
        return self._player1.name

    def get_player2_name(self) -> str:
        """
        Returns the name of the second player.
        :return: the name
        """
        return self._player2.name

    def increment_player_score(self, player_name: str) -> None:
        """
        Increments the score of a given player. Once the score has been incremented,
        this method updates the current status of this game.
        :param player_name:
        :return:
        """
        if not self.is_there_a_winner():
            if player_name == self.get_player1_name():
                self._player1.increment_score()
            elif player_name == self.get_player2_name():
                self._player2.increment_score()
            self.update_game_status()
        else:
            raise GameHasAlreadyBeenWonError

    def update_game_status(self) -> None:
        if self.is_deuce():
            result = self.DEUCE
        elif self.is_there_an_advantage_player():
            result = self.ADVANTAGE + self.SPACE + self.advantage_player().name
        elif self.is_there_a_winner():
            result = self.the_winner().name + self.SPACE + self.WINS
        else:
            result = self.get_player1_name() + self.SPACE + self._player1.get_score_as_string()
            result += self.SPACE + self.DASH + self.SPACE
            result += self.get_player2_name() + self.SPACE + self._player2.get_score_as_string()
        self._game_status = result

    def is_there_an_advantage_player(self) -> bool:
        return self.advantage_player() is not None

    def advantage_player(self) -> Player:
        result = None

        if self._player2.has_at_least_forty_points() and self._player1.has_at_least_forty_points():
            if self._player1.has_one_point_advantage_on(self._player2):
                result = self._player1
            elif self._player2.has_one_point_advantage_on(self._player1):
                result = self._player2

        return result

    def is_deuce(self):
        return self._player1.is_tied_with(self._player2) and self._player1.has_at_least_forty_points()

    def is_there_a_winner(self) -> bool:
        return self.the_winner() is not None

    def the_winner(self) -> Player:
        winner = None

        if self._player1.has_more_than_forty_points() and self._player1.has_at_least_two_points_advantage_on(self._player2):
            winner = self._player1
        elif self._player2.has_more_than_forty_points() and self._player2.has_at_least_two_points_advantage_on(self._player1):
            winner = self._player2

        return winner
