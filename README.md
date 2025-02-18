
# Encrypted Message Solver Project

## Description
This script is a client-side program that interacts with a remote server using a communication protocol based on encrypted or encoded messages. It utilizes several techniques to solve and decrypt messages, such as math operations, base decoding (Base64, Base32, Base85), Morse code, Braille, RGB color decoding, word searching in a list, and Caesar cipher encryption.

The script connects to a server via a TCP socket, exchanges messages, and solves puzzles using the server's responses. It saves the responses in a file, processes mathematical operations, decodes messages in different formats, and sends results back to the server.

## Features
- **Mathematical Operations**: Solve operations such as addition, subtraction, and multiplication.
- **Base64/Base32/Base85 Decoding**: Supports decoding messages encoded in various bases.
- **Morse Code**: Decode messages in Morse code.
- **Braille**: Decode messages in Braille.
- **RGB Colors**: Convert RGB values to color names.
- **Caesar Cipher**: Decode text encrypted using Caesar cipher (shift cipher).
- **Answer History**: Save responses in a text file and allow retrieval.

## Prerequisites
- Python 3.x
- The following Python modules must be installed:
  - `nltk`
  - `pycipher`
  - `webcolors`

### Installing Dependencies
1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # Activate the virtual environment
   ```

2. Install the dependencies:
   ```bash
   pip install nltk pycipher webcolors
   ```

3. Download the necessary NLTK corpora:
   ```python
   import nltk
   nltk.download('words')
   ```

## Usage

### Running the Script

The script can be run from the command line with options to specify the port for connecting to the remote server. Here’s the command to start the program:

```bash
python script.py --port <port>
```

Where `<port>` is the server port to connect to.

### Generated Files
- `counter.txt`: A file that keeps track of a counter for script execution.
- `answers.txt`: A file where the server responses and calculated answers are saved.
- `<name>.txt`: A file where the answers are stored, specific to each execution.

