from pathlib import Path



def solve(p: Path) -> int:
    total_fuel = 0
    with p.open() as f:
        for line in f:
            mass = int(line.strip())
            total_fuel += mass // 3 + 2
    return total_fuel


def solve2(p: Path) -> int:
    total_fuel = 0
    with p.open() as f:
        for line in f:
            mass = int(line.strip())
            total_fuel += required_fuel(mass)
    return total_fuel


def required_fuel(mass: int) -> int:
    total_fuel = 0
    incremental_fuel = mass // 3 - 2
    while incremental_fuel >= 0:
        total_fuel += incremental_fuel
        incremental_fuel = incremental_fuel // 3 - 2
    return total_fuel



def main() -> None:
    src = Path("input_day1.txt")
    ans1 = solve(src)
    print(ans1)
    ans2 = solve2(src)
    print(ans2)


if __name__ == "__main__":
    main()
