

class Helper:

    @staticmethod
    def parse_to_bool(input_str: str) -> bool:
        """
        Parses a string into a boolean value.

        Valid inputs: "0", "1", "true", "false", "True", "False"
        Invalid inputs will raise a ValueError.
        """
        # Clean the input by stripping whitespace and converting to lowercase
        input_str = input_str.strip().lower()

        # Handle various representations of true/false
        if input_str in {'1', 'true'}:
            return True
        elif input_str in {'0', 'false'}:
            return False
        else:
            # Raise an error for invalid inputs
            raise ValueError(f"Invalid input for boolean conversion: {input_str}")