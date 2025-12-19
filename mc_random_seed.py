import argparse
import time

class JavaRandom:
    """
    A fully compatible implementation of java.util.Random
    """ 
    def __init__(self, seed):
        self.seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)

    def next(self, bits):
        self.seed = (self.seed * 0x5DEECE66D + 0xB) & ((1 << 48) - 1)
        return self.seed >> (48 - bits)

    def next_long(self):
        high = self.next(32)
        low = self.next(32)
        value = (high << 32) + low

        # Convert to signed long
        if value >= (1 << 63):
            value -= (1 << 64)
        return value


def generate_seeds(count):
    # Like Minecraft, initialize Random based on the current time (ms).
    base_seed = int(time.time() * 1000)
    rng = JavaRandom(base_seed)

    return [rng.next_long() for _ in range(count)]


def main():
    parser = argparse.ArgumentParser(
        description="Generates random seeds in the same way as Minecraft Java Edition"
    )
    parser.add_argument(
        "--seeds",
        type=int,
        default=1,
        help="Number of seeds to generate (default is 1)"
    )

    args = parser.parse_args()

    for seed in generate_seeds(args.seeds):
        print(seed)


if __name__ == "__main__":
    main()
