class CoderWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self):
        """Opens the output file and gets ready to write into it."""

    def __del__(self):
        """Closes the output file."""

    def set_file_name(self, file_name):
        """Informs the coder writer that the translation of a new VM file
           started"""

    def write_arithmetic(self, command):
        """Writes the assembly code that is the translation of the the given
           arithmetic command."""

    def write_push_pop(self, command, segment, index):
        """Writes the assembly code that is the translation of the given
           command where command is either C_PUSH or C_POP."""

    def close(self):
        """Cloes the output file."""
