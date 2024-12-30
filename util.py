from pathlib import Path


def load_inputs(day: str, has_test: bool = True) -> tuple[str, str]:
    intl_day = day.rjust(2, "0")
    path = Path(__file__).parent
    test = path / "test" / f"day{intl_day}.txt"
    input = path / "input" / f"day{intl_day}.txt"
    if has_test:
        with open(test, "r") as file:
            test_data = file.read()
    else:
        test_data = ""
    with open(input, "r") as file:
        input_data = file.read()
    return test_data, input_data
