import random

def get_dice():
    try:
        dice_0 = random.randint(1, 6)
        dice_1 = random.randint(1, 6)
        if dice_0 == dice_1:
            # Doubles: return four dice of the same value
            return (dice_0, dice_1, dice_0, dice_1)
        else:
            # Normal roll: return two dice
            return (dice_0, dice_1)
    except Exception:
        # In case of error, return empty tuple
        return ()