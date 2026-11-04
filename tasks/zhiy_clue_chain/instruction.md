# Follow the clue chain

`/app/next.py` runs a chain of 60 short clues.

- `python /app/next.py` prints the current clue.
- `python /app/next.py <answer>` submits an answer to the current clue.

Each answer is a single lowercase word, or a number written in digits. A correct
answer reveals the next clue. An incorrect answer leaves you on the same clue,
and you can try again.

After the last clue is answered, the program prints a final token. Write that
token to `/app/result.txt`, with nothing else in the file.
