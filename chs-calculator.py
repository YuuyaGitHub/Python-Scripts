import argparse
import sys

SECTOR_SIZE = 512
BYTES_PER_MB = 1024 * 1024

# Absolute limits
MAX_CYLINDER = 266305
MAX_HEAD = 255
MAX_SECTOR = 255

# IDE limits
IDE_MAX_CYLINDER = 65536
IDE_MAX_HEAD = 16
IDE_MAX_SECTOR = 255

class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(f"Error: {message}\n", file=sys.stderr)
        self.print_help()
        sys.exit(2)

def validate_range(name, value, min_val, max_val):
    if value < min_val or value > max_val:
        raise ValueError(f"{name} must be between {min_val} and {max_val}")

def main():
    parser = CustomArgumentParser(
        description="Calculate the capacity (MB) from the disk CHS.",
        add_help=False
    )

    parser.add_argument(
        "--help",
        action="help",
        help="Show this help message and exit"
    )

    parser.add_argument(
        "--ignore-ide-limit",
        action="store_true",
        help="Ignores the IDE limitations (C=65536, H=16, S=255) and allows for larger capacities to be calculated."
    )

    parser.add_argument(
        "-C", "--Cylinder", "-c", "--cylinder",
        type=int, required=True,
        help=f"Number of cylinders (1–{MAX_CYLINDER})"
    )
    parser.add_argument(
        "-H", "--Head", "-h", "--head",
        type=int, required=True,
        help=f"Number of heads (1–{MAX_HEAD})"
    )
    parser.add_argument(
        "-S", "--Sector", "-s", "--sector",
        type=int, required=True,
        help=f"Number of sectors per track (1–{MAX_SECTOR})"
    )

    args = parser.parse_args()

    # Absolute limit check
    try:
        validate_range("Cylinder", args.Cylinder, 1, MAX_CYLINDER)
        validate_range("Head", args.Head, 1, MAX_HEAD)
        validate_range("Sector", args.Sector, 1, MAX_SECTOR)
    except ValueError as e:
        parser.error(str(e))

    # IDE limit check (only if not ignored)
    if not args.ignore_ide_limit:
        if (
            args.Cylinder > IDE_MAX_CYLINDER or
            args.Head > IDE_MAX_HEAD or
            args.Sector > IDE_MAX_SECTOR
        ):
            parser.error("The specified CHS exceeds the IDE limit")

    capacity_bytes = args.Cylinder * args.Head * args.Sector * SECTOR_SIZE
    capacity_mb = capacity_bytes // BYTES_PER_MB

    if capacity_mb == 0:
        parser.error("The capacity result is 0MB")

    print(f"[Result]")
    print(f"Cylinder: {args.Cylinder}")    # Cylinder
    print(f"Head: {args.Head}")            # Head
    print(f"Sector: {args.Sector}")        # Sector
    print()
    print(f"Capacity: {capacity_mb} MB")   # Capacity

    notes = []

    if capacity_mb > 504:   # 504MB
        notes.append(
            "This capacity may not be recognized by Old BIOSes that do not support LBA."
        )
    if capacity_mb > 8400:  # 8.4GB
        notes.append(
            "This capacity may not be recognized by NEC PC-98 series."
        )
    if capacity_mb > 32768: # 32GB
        notes.append(
            "This capacity may not be recognized by some Award BIOS."
        )
    if capacity_mb > 65536: # 64GB
        notes.append(
            "This capacity may cause problems with FDISK in Microsoft Windows 98."
        )

    if notes:
        print()
        print("Note:")
        for note in notes:
            print(f"- {note}")

if __name__ == "__main__":
    main()
