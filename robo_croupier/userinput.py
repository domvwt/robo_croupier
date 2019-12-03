from typing import ClassVar


def get_valid_input(prompt: str, valid_class: ClassVar, invalid_msg: str):
    """
    Ask the user for input and ensure that their entry is valid.
    If the entry is invalid, prompt again for valid input.
    :param prompt: Command line prompt for input
    :param valid_class: A class type that the string input will be cast to
    :param invalid_msg: What to display when the user input is invalid
    :return: the user input cast as the requested type
    """
    while True:
        response = input(prompt)
        try:
            result = valid_class(response)
            return result
        except TypeError:
            print(invalid_msg)


def select_menu(
    prompt: str, select_from: list, invalid_msg: str = "Invalid selection."
):
    print(prompt)
    list_index = range(1, len(select_from) + 1)

    while True:
        for num, value in zip(list_index, select_from):
            print(f"{num}: {value}")
        user_input = get_valid_input(
            f"Please choose an option {list(list_index)}: ",
            valid_class=int,
            invalid_msg=invalid_msg,
        )
        if user_input in list_index:
            selection = select_from[user_input - 1]
            print(selection)
            return selection
        else:
            print(invalid_msg)


def main():
    select_menu("Hello", ["cake", "crisps", "jelly"])


if __name__ == "__main__":
    main()
