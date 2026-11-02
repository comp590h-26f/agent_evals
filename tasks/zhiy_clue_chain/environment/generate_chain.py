"""Build /app/chain.dat at image build time; deleted afterwards so answers stay hidden."""

import json

from next import CHAIN_PATH, INITIAL_KEY, check_value, derive_key, xor_with_key

FINAL_TOKEN = "CHAIN-5e8b1d47c2fa"

CLUES = [
    ("What is 7 times 8?", "56"),
    ("What is the opposite of hot?", "cold"),
    ("How many days are in a week?", "7"),
    ("What is the capital of France?", "paris"),
    ("What color do you get by mixing blue and yellow?", "green"),
    ("What is 15 plus 27?", "42"),
    ("Which planet is known as the Red Planet?", "mars"),
    ("How many legs does a spider have?", "8"),
    ("What is the past tense of the verb 'go'?", "went"),
    ("What is 100 divided by 4?", "25"),
    ("What is the two-letter chemical symbol for gold?", "au"),
    ("How many sides does a hexagon have?", "6"),
    ("What is the largest ocean on Earth?", "pacific"),
    ("What is the square root of 81?", "9"),
    ("What is the plural of 'mouse'?", "mice"),
    ("What is the next number: 2, 4, 8, 16, ...?", "32"),
    ("What is the first month of the year?", "january"),
    ("How many minutes are in an hour?", "60"),
    ("What is the opposite of 'up'?", "down"),
    ("What is 9 squared?", "81"),
    ("What is the capital of Japan?", "tokyo"),
    ("What is the last letter of the English alphabet?", "z"),
    ("In Python, which keyword defines a function?", "def"),
    ("How many continents are there?", "7"),
    ("What is 144 divided by 12?", "12"),
    ("What is frozen water called?", "ice"),
    ("Which git subcommand records staged changes?", "commit"),
    ("What is the third planet from the Sun?", "earth"),
    ("What is 13 plus 29?", "42"),
    ("What is the opposite of 'night'?", "day"),
    ("How many bits are in a byte?", "8"),
    ("Which shell command prints the current directory?", "pwd"),
    ("What is 6 factorial?", "720"),
    ("What is the capital of Italy?", "rome"),
    ("Which metal has the chemical symbol Fe?", "iron"),
    ("What is the next letter: a, c, e, g, ...?", "i"),
    ("What is 1000 minus 1?", "999"),
    ("How many strings does a standard violin have?", "4"),
    ("What is the past tense of 'eat'?", "ate"),
    ("Which animal is called the king of the jungle?", "lion"),
    ("What is 11 times 11?", "121"),
    ("What is the main language spoken in Brazil?", "portuguese"),
    ("At sea level, what is the boiling point of water in degrees Celsius?", "100"),
    ("Which HTTP status code means 'Not Found'?", "404"),
    ("What is the opposite of 'true' in boolean logic?", "false"),
    ("How many hours are in a day?", "24"),
    ("What is the largest planet in our solar system?", "jupiter"),
    ("What is half of 90?", "45"),
    ("Which season comes after winter?", "spring"),
    ("What is the capital of Spain?", "madrid"),
    ("What is 2 to the power of 10?", "1024"),
    ("What do bees make?", "honey"),
    ("Which shell command lists the files in a directory?", "ls"),
    ("How many sides does a triangle have?", "3"),
    ("What is the opposite of 'empty'?", "full"),
    ("What is 17 plus 38?", "55"),
    ("What is the fourth month of the year?", "april"),
    ("Which Python keyword starts a loop over the items in a sequence?", "for"),
    ("How many zeros are in one million?", "6"),
    ("What color is a clear daytime sky?", "blue"),
]

key = INITIAL_KEY
records = []
for index, (_, answer) in enumerate(CLUES):
    key = derive_key(key, answer)
    next_text = CLUES[index + 1][0] if index + 1 < len(CLUES) else FINAL_TOKEN
    records.append(
        {
            "check": check_value(key),
            "payload": xor_with_key(next_text.encode(), key).hex(),
        }
    )

CHAIN_PATH.write_text(json.dumps({"first_clue": CLUES[0][0], "records": records}))
