import random, pygame, math
from src.Brick import Brick

#patterns
NONE = 1
SINGLE_PYRAMID = 2
MULTI_PYRAMID = 3

SOLID = 1            # all colors the same in this row
ALTERNATE = 2        # alternative colors
SKIP = 3             # skip every other brick
NONE = 4             # no block this row


# Tier has no effects on the bricks toughness, only the scores
def weighted_tier(base_tier, highest_tier):
    """Return a weighted random tier with more common lower tiers."""
    if base_tier > highest_tier:
        highest_tier = base_tier  # Ensure base_tier is never higher than highest_tier
    
    # Create a list of tiers from base to highest
    tiers = list(range(base_tier, highest_tier))
    
    # Ensure there's always at least one tier in the range
    if len(tiers) == 0:
        tiers = [base_tier]  # Fall back to base_tier if something goes wrong

    # Define weights for tiers based on your new requirements
    # 90% for Tier 0, 6% for Tier 1, 3% for Tier 2, 1% for Tier 3
    tier_weights = [90, 6, 3, 1]
    
    # Slice the weights to match the number of tiers in the range
    weights_for_range = tier_weights[:len(tiers)]

    # Return a random tier based on the weights
    return random.choices(tiers, weights=weights_for_range, k=1)[0]

# Dynamically change the color depending on level
def weighted_color(base_color, highest_color, level):
    """Return a weighted random color based on the base and highest color range for the level."""
    # Define color range based on the input
    colors = list(range(base_color, highest_color + 1))

    # Adjust weights dynamically based on the number of colors
    if len(colors) == 2:
        color_weights = [80, 20]  # Two colors
    elif len(colors) == 3:
        color_weights = [60, 30, 10]  # Three colors
    elif len(colors) == 4:
        color_weights = [40, 30, 20, 10]  # Four colors
    elif len(colors) == 5:
        color_weights = [40, 25, 20, 10, 5]  # Five colors
    else:
        color_weights = [50]  # Fallback case if there is only 1 color

    # Trim weights to match the number of colors
    weights_for_range = color_weights[:len(colors)]

    # Return a random color based on the weights
    return random.choices(colors, weights=weights_for_range, k=1)[0]


def get_tier_range(level):
    """Determine the base and highest tier for a given level."""
    
    base_tier = 0
    highest_tier = 4

    return base_tier, highest_tier

# Set color range based on level
def get_color_range(level):
    if level <= 10:
        base_color = 1
        highest_color = 2  # Color range: 1, 2
    elif 11 <= level <= 20:
        base_color = 1
        highest_color = 3  # Color range: 1, 2, 3
    elif 21 <= level <= 30:
        base_color = 1
        highest_color = 4  # Color range: 1, 2, 3, 4
    elif 31 <= level <= 40:
        base_color = 2
        highest_color = 4  # Color range: 2, 3, 4
    elif 41 <= level <= 50:
        base_color = 2
        highest_color = 5  # Color range: 2, 3, 4, 5
    else:
        base_color = 3
        highest_color = 5  # Color range: 3, 4, 5

    print(f"Debug: Level {level} is generating with color range ({base_color}, {highest_color})")
    return base_color, highest_color


class LevelMaker:
    def __init__(self):
        pass

    @classmethod
    def CreateMap(cls, level):
        """Creates a new level with randomized bricks."""
        bricks = []

        # Not gooood enough!!
        # OKKKK!! I'm improving this level generation too!!!

        num_rows = (min(3 + (level // 3), 7))
        num_cols = random.randint(7, 13)

        base_tier = 0
        highest_tier = 4

        base_color = 1 
        highest_color = 5  # Ensure highest_color is capped at 5

        # Randomly choose a pattern for this level
        # NOTE: Removed cluster level generation because the level looks ugly!!

        pattern_type = random.choice(['default', 'zigzag', 'diagonal', 'pyramid'])
        # pattern_type = random.choice(['default', 'zigzag', 'diagonal', 'pyramid', 'cluster'])

        # Use a special pattern every 5 levels
        if level % 5 == 0:
            pattern_type = 'pyramid'
        else:
            pattern_type = random.choice(['default', 'zigzag', 'diagonal'])
            # pattern_type = random.choice(['default', 'zigzag', 'diagonal', 'cluster'])


        # Apply pattern creation
        if pattern_type == 'default':
            cls.create_default_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level)
        elif pattern_type == 'zigzag':
            cls.create_zigzag_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level)
        elif pattern_type == 'diagonal':
            cls.create_diagonal_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level)
        elif pattern_type == 'pyramid':
            cls.create_pyramid_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level)
        elif pattern_type == 'cluster':
            cls.create_cluster_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level)

        return bricks


    @staticmethod
    def create_zigzag_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level):
        """Create a zigzag pattern with proper tier and color assignment."""
    
        print("Log: Current map pattern is Zigzag.")

        skip_pattern = False
        alternate_pattern = True

        skip_flag = True
        alternate_flag = False

        base_tier, highest_tier = get_tier_range(level)
        base_color, highest_color = get_color_range(level)

        # Debug print for base and highest values
        print(f"Base tier: {base_tier}, Highest tier: {highest_tier}")
        print(f"Base color: {base_color}, Highest color: {highest_color}")

        for y in range(num_rows):
            for x in range(num_cols):
                if (x + y) % 2 == 0:  # Create the zigzag effect
                    if skip_pattern and skip_flag:
                        skip_flag = not skip_flag
                        continue
                    else:
                        skip_flag = not skip_flag

                    brick_x = x * 96 + 24 + (13 - num_cols) * 48
                    brick_y = y * 48

                    # Use the weighted_tier function and randomize color within range
                    b = Brick(brick_x, brick_y, weighted_color(base_color, highest_color, level), weighted_tier(base_tier, highest_tier))

                    # Append brick to list
                    bricks.append(b)


    @staticmethod
    def create_diagonal_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level):
        """Create a diagonal pattern with alternating and solid color/tier options."""
        
        print("Log: Current map pattern is Diagonal.")

        skip_pattern = False
        alternate_pattern = True

        skip_flag = random.choice([True, False])
        alternate_flag = random.choice([True, False])

        base_tier, highest_tier = get_tier_range(level)
        base_color, highest_color = get_color_range(level)

        for d in range(10):  # Number of diagonal rows
            for y in range(num_rows):
                for x in range(num_cols):
                    if x == (y + d) % num_cols:  # Diagonal effect
                        if skip_pattern and skip_flag:
                            skip_flag = not skip_flag
                            continue
                        else:
                            skip_flag = not skip_flag

                        brick_x = x * 96 + 24 + (13 - num_cols) * 48
                        brick_y = y * 48

                        # Create the brick with the color and tier
                        b = Brick(brick_x, brick_y, weighted_color(base_color, highest_color, level), weighted_tier(base_tier, highest_tier))

                        bricks.append(b)


    @staticmethod
    def create_default_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level):
        """Create the default random pattern with individual tier randomization."""
        
        print("Log: Current map pattern is Default.")

        skip_pattern = False
        alternate_pattern = False

        skip_flag = random.choice([True, False])
        alternate_flag = random.choice([True, False])

        base_tier, highest_tier = get_tier_range(level)
        base_color, highest_color = get_color_range(level)

        for y in range(num_rows):
            for x in range(num_cols):
                if skip_pattern and skip_flag:
                    skip_flag = not skip_flag
                    continue
                else:
                    skip_flag = not skip_flag

                brick_x = x * 96 + 24 + (13 - num_cols) * 48
                brick_y = y * 48

                # Create the brick with the color and tier
                b = Brick(brick_x, brick_y, weighted_color(base_color, highest_color, level), weighted_tier(base_tier, highest_tier))

                bricks.append(b)


    @staticmethod
    def create_pyramid_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level):
        """Create a pyramid pattern with alternating and solid color/tier options."""
        
        print("Log: Current map pattern is Pyramid.")

        skip_pattern = False
        alternate_pattern = False

        skip_flag = random.choice([True, False])
        alternate_flag = random.choice([True, False])

        base_tier, highest_tier = get_tier_range(level)
        base_color, highest_color = get_color_range(level)

        for y in range(num_rows):
            for x in range(y, num_cols - y):  # Pyramid shape
                if skip_pattern and skip_flag:
                    skip_flag = not skip_flag
                    continue
                else:
                    skip_flag = not skip_flag

                brick_x = x * 96 + 24 + (13 - num_cols) * 48
                brick_y = y * 48

                # Create the brick with the color and tier
                b = Brick(brick_x, brick_y, weighted_color(base_color, highest_color, level), weighted_tier(base_tier, highest_tier))

                bricks.append(b)


    @staticmethod
    def create_cluster_pattern(bricks, num_rows, num_cols, base_color, highest_color, base_tier, highest_tier, level):
        """Create random clusters of bricks with alternating and solid color/tier options."""
    
        print("Log: Current map pattern is Cluster (Pure Random).")

        skip_pattern = random.choice([True, False])
        alternate_pattern = random.choice([True, False])

        skip_flag = random.choice([True, False])
        alternate_flag = random.choice([True, False])

        base_tier, highest_tier = get_tier_range(level)
        base_color, highest_color = get_color_range(level)

        for _ in range(random.randint(5, 9)):  # Random number of clusters
            cluster_x = random.randint(0, num_cols - 1)
            cluster_y = random.randint(0, num_rows - 1)
            for i in range(random.randint(3, 6)):  # Each cluster has random size
                x = cluster_x + random.randint(-1, 1)
                y = cluster_y + random.randint(-1, 1)
                if 0 <= x < num_cols and 0 <= y < num_rows:
                    if skip_pattern and skip_flag:
                        skip_flag = not skip_flag
                        continue
                    else:
                        skip_flag = not skip_flag

                    brick_x = x * 96 + 24 + (13 - num_cols) * 48
                    brick_y = y * 48

                    # Create the brick with the color and tier
                    b = Brick(brick_x, brick_y, weighted_color(base_color, highest_color, level), weighted_tier(base_tier, highest_tier))

                    bricks.append(b)
