class CommandParser:
    @staticmethod
    def is_command(user_prompt: str) -> bool:
        if user_prompt == '/exit':
            return True
        # TODO: Implement command parsing within a CLI application
        return False
