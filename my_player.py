# First Author: Motassembellah Mohamed Bassiouni, 2136611
# Second Author: Hamza Boukaftane, 2183376
# Team: 4

from player_divercite import PlayerDivercite
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from game_state_divercite import GameStateDivercite

TEN_MINUTES = 10 * 60
FIVE_MINUTES = 5 * 60
HIGH_DEPTH = 4
MEDIUM_DEPTH = 3
LOW_DEPTH = 2

class MyPlayer(PlayerDivercite):
    """
    Player class for Divercite game that makes random moves.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "MyPlayer"):
        """
        Initialize the PlayerDivercite instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type, name)

    def get_opponent_id(self, current_state: GameStateDivercite):
        return next(id for id in current_state.get_scores() if id != self.get_id())

    def get_max_depth(self, remaining_time):
        if remaining_time >= TEN_MINUTES:
            return HIGH_DEPTH
        elif remaining_time >= FIVE_MINUTES:
            return MEDIUM_DEPTH
        else:
            return LOW_DEPTH

    def isTerminal(self, current_state: GameStateDivercite, depth, maxDepth):
        return depth == maxDepth or current_state.is_done()

    def minValue(self, current_state: GameStateDivercite, depth: int, maxDepth: int, alpha: float, beta: float):
        if self.isTerminal(current_state, depth, maxDepth):
            return self.heuristic_utility(current_state), None
        
        possible_actions = list(current_state.generate_possible_heavy_actions())
        best_score = float('inf')
        best_action = None

        for action in possible_actions:
            next_state = action.get_next_game_state()
            score, _ = self.maxValue(next_state, depth + 1, maxDepth, alpha, beta)
            if score < best_score:
                best_score = score
                best_action = action
            beta = min(beta, score)
            if beta <= alpha:
                break
        return best_score, best_action
    
    def maxValue(self, current_state: GameStateDivercite, depth: int, maxDepth: int, alpha: float, beta: float):
        if self.isTerminal(current_state, depth, maxDepth):
            return self.heuristic_utility(current_state), None
        
        possible_actions = list(current_state.generate_possible_heavy_actions())
        best_score = -float('inf')
        best_action = None
        for action in possible_actions:
            next_state = action.get_next_game_state()
            score, _ = self.minValue(next_state, depth + 1, maxDepth, alpha, beta)
            if score > best_score:
                best_score = score
                best_action = action
            alpha = max(alpha, score)
            if beta <= alpha:
                break
        return best_score, best_action
    
    def get_divercity_score(self, current_state: GameStateDivercite, player_id, opponent_id):
        player_divercity_score = 0
        board = current_state.get_rep().get_env()
        for pos, piece in board.items():
            piece_json = piece.to_json()
            if current_state.check_divercite(pos, piece_json["piece_type"], current_state.get_rep()):
                if piece_json["owner_id"] == player_id:
                    player_divercity_score += 1
        return player_divercity_score
    
    def get_center_score(self, current_state: GameStateDivercite, player_id, opponent_id):
        player_center_score = 0
        opponent_center_score = 0
        center_positions = [3, 5]

        board = current_state.get_rep().get_env() # Get the current board state
        for pos, piece in board.items():
            piece_json = piece.to_json()
            piece_type = piece_json["piece_type"][1]
            # Condition to check if the piece controls the center of the board AND that it is a city
            if pos[0] in center_positions and piece_type == "C":
                # Increment the score of the player who controls the center
                if piece_json["owner_id"] == player_id:
                    player_center_score += 1
                elif piece_json["owner_id"] == opponent_id:
                    opponent_center_score += 1

        central_control_score = player_center_score - opponent_center_score

        return central_control_score

    def heuristic_utility(self, current_state: GameStateDivercite):
        personal_id = self.get_id()
        opponent_id = self.get_opponent_id(current_state)

        player_score = current_state.get_player_score(self)
        opponent_score = current_state.get_scores()[opponent_id]

        # Calculate the three components of the heuristic value
        score_difference = player_score - opponent_score
        divercity_score = self.get_divercity_score(current_state, personal_id, opponent_id)
        center_control_score = self.get_center_score(current_state, personal_id, opponent_id) 

        # Considering the weights of the three components
        weight = {"score difference": 10, "divercity": 5, "center control": 5}
        weighted_score_difference = weight["score difference"] * score_difference
        weighted_divercity_score = weight["divercity"] * divercity_score
        weighted_center_control_score = weight["center control"] * center_control_score

        # Calculation of the heuristic value based on weighted sum of the three components
        heuristic_value = weighted_score_difference + weighted_divercity_score + weighted_center_control_score

        return heuristic_value


    def compute_action(self, current_state: GameState, remaining_time: int = 1e9, **kwargs) -> Action:
        """
        Use the minimax algorithm to choose the best action based on the heuristic evaluation of game states.

        Args:
            current_state (GameState): The current game state.

        Returns:
            Action: The best action as determined by minimax.
        """
        depth = 0
        alpha = -float('inf')
        beta = float('inf')
        its_my_turn = current_state.get_next_player() == self

        if its_my_turn:
            return self.maxValue(current_state, depth, self.get_max_depth(remaining_time), alpha, beta)[1]
        else:
            return self.minValue(current_state, depth, self.get_max_depth(remaining_time), alpha, beta)[1]
