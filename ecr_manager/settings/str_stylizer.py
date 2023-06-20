from colorama import (
    Fore,
    Style,
)


class StrStylizer:
    @property
    def reset(self) -> str:
        return Style.RESET_ALL

    @property
    def DEBUG(self) -> str:
        return Fore.MAGENTA

    @property
    def INFO(self) -> str:
        return Fore.CYAN

    @property
    def WARNING(self) -> str:
        return Fore.YELLOW

    @property
    def ERROR(self) -> str:
        return Fore.RED

    @property
    def CRITICAL(self) -> str:
        return f"{Style.BRIGHT}{self.ERROR}"


str_stylizer: StrStylizer = StrStylizer()
