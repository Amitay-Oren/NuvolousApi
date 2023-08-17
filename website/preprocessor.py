class Preprocessor:
    """
    A class for pre-processing the extracted text.
    """

    @staticmethod
    def remove_blank_lines(text: str) -> str:
        """
        Removes blank lines from the extracted text.
        """
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n".join(lines)
