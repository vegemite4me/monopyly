from .dice import Dice
from .player import Player
from .game_state import GameState


class Game(object):
    '''
    Manages one game of monopoly.

    Holds all the game state: the board, the cards and the players.
    It rolls the dice and moves the players. It calls into the player
    AIs when events occur and when there are decisions to be made.

    It keeps track of players' solvency and decides when a player is
    bankrupt and when the game is over.

    There is a turn limit (as otherwise the game could continue forever).
    When the limit is reached, all assets are liquidated (houses sold,
    properties mortgaged) and the winner is the player with the most money.
    '''

    class Action(object):
        '''
        An 'enum' for actions that can happen during the game.
        '''
        ROLL_AGAIN = 1
        DO_NOT_ROLL_AGAIN = 2

    def __init__(self):
        '''
        The 'constructor'.
        '''
        self.game_state = GameState()
        self.dice = Dice()

    def add_player(self, ai):
        '''
        Adds a player AI.
        '''
        # We wrap the AI up into a Player object...
        player_number = len(self.game_state.players) + 1
        self.game_state.players.append(Player(ai, player_number))

    def play_game(self):
        '''
        Plays a game of monopoly.
        '''
        # We tell the players that the game is starting, and which
        # player-number they are...
        for player in self.game_state.players:
            player.ai.start_of_game(player.number)

    def play_one_round(self):
        '''
        Plays one round of the game, ie one turn for each of
        the players.

        The round can come to an end before all players' turns
        are finished if one of the players wins.
        '''
        for player in self.game_state.players:
            self.play_one_turn(player)

    def play_one_turn(self, current_player):
        '''
        Plays one turn for one player.
        '''
        # We notify all players that this player's turn is starting...
        for player in self.game_state.players:
            game_state = self.game_state.copy()
            player.ai.start_of_turn(game_state, current_player.number)

        # TODO: Before the start of the turn we give the player an
        # option to perform deals or mortgage properties so that they
        # can raise money for house-building...

        # TODO: The player can build houses...

        # TODO: If the player is in jail, they can buy themselves out,
        # or play Get Out Of Jail Free.

        # This while loop manages rolling again if the player
        # rolls doubles...
        roll_again = Game.Action.ROLL_AGAIN
        number_of_doubles_rolled = 0
        while roll_again == Game.Action.ROLL_AGAIN:
            roll_again, number_of_doubles_rolled = self.roll_and_move(current_player, number_of_doubles_rolled)

    def roll_and_move(self, current_player, number_of_doubles_rolled):
        '''
        Rolls the dice, moves the player and takes the appropriate
        action for the square landed on.

        Returns whether we should roll again and the number of doubles rolled.
        '''
        # TODO: We roll the dice and move the player.
        # We notify all players that the player has landed
        # on the new square.
        roll1, roll2 = self.dice.roll()

        # We check if doubles was rolled...
        roll_again = Game.Action.DO_NOT_ROLL_AGAIN
        if(roll1 == roll2):
            # Doubles was rolled...
            number_of_doubles_rolled += 1
            if(number_of_doubles_rolled == 3):
                # TODO: Go to jail
                return Game.Action.DO_NOT_ROLL_AGAIN, number_of_doubles_rolled
            else:
                roll_again = Game.Action.ROLL_AGAIN

        # We move the player to the new square, and notify all players
        # that they are there...
        total_roll = roll1 + roll2



        # TODO: We perform the square's landed-on action...


        return roll_again, number_of_doubles_rolled

