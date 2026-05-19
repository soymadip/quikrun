from dataclasses import dataclass


@dataclass
class Config:
    name: str
    std: int


ss = Config("name", "std")


def main() -> None:
    print("work in progress")


if __name__ == "__main__":
    main()
