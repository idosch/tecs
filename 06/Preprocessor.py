import os
import sys

class Preprocessor:
    """Creates a temporary file without whitespaces and comments."""

    def __init__(self):
        """Opens the input stream and gets ready to process it."""
        self._input_file = open(sys.argv[1], 'r')
        self._code = self._input_file.readlines()
        self._input_file.close()
        self._temp_file = None

    def __del__(self):
        """Removes the temporary file."""
        os.remove(sys.argv[1] + '.tmp')

    def remove_white_spaces_comments(self):
        """Removes white spaces and comments."""
        new_code = []
        for line in self._code:
            line = ''.join(line.rsplit())

            if '//' in line:
                pos = line.find('//')
                line = line[:pos]

            if line != '':
                new_code.append(line)

        self._code = new_code

    def write_temp_file(self):
        """Write the processed text to a temp file."""
        self._temp_file = open(sys.argv[1] + '.tmp', 'w')

        for line in self._code:
            self._temp_file.write(line + str('\n'))

        self._temp_file.close()
