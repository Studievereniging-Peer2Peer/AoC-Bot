import dataclasses


@dataclasses.dataclass
class Day:
    get_star_1_ts: int | None
    get_star_2_ts: int | None


@dataclasses.dataclass
class User:
    name: str
    localScore: int
    globalScore: int
    stars_amount: int
    days: dict[int, Day]
    leaderboard_position: int = -1
