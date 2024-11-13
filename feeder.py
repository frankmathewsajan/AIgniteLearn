from learn.models import CodingQuestion  # Replace 'your_app' with the actual app name

problems = [
    # Easy Problems
    {
        "difficulty": "easy",
        "problem": "Write a program that prints 'Hello, World!'.",
        "input": "",
        "expected_output": "Hello, World!"
    },
    {
        "difficulty": "easy",
        "problem": "Accept two integers as input and print their sum.",
        "input": "3 5",
        "expected_output": "8"
    },
    {
        "difficulty": "easy",
        "problem": "Check if a given integer is odd or even.",
        "input": "4",
        "expected_output": "Even"
    },
    {
        "difficulty": "easy",
        "problem": "Take a string as input and print its reverse.",
        "input": "hello",
        "expected_output": "olleh"
    },
    {
        "difficulty": "easy",
        "problem": "Accept three integers and print the maximum.",
        "input": "3 7 5",
        "expected_output": "7"
    },
    {
        "difficulty": "easy",
        "problem": "Determine if a given year is a leap year.",
        "input": "2024",
        "expected_output": "Leap Year"
    },
    {
        "difficulty": "easy",
        "problem": "Count the number of vowels in a string.",
        "input": "education",
        "expected_output": "5"
    },
    {
        "difficulty": "easy",
        "problem": "Calculate the sum of digits of a given integer.",
        "input": "1234",
        "expected_output": "10"
    },
    {
        "difficulty": "easy",
        "problem": "Compute the factorial of a number.",
        "input": "5",
        "expected_output": "120"
    },
    {
        "difficulty": "easy",
        "problem": "Determine if a given string is a palindrome.",
        "input": "radar",
        "expected_output": "True"
    },
    {
        "difficulty": "easy",
        "problem": "Print the first N natural numbers.",
        "input": "5",
        "expected_output": "1 2 3 4 5"
    },
    {
        "difficulty": "easy",
        "problem": "Compute the area of a circle given its radius.",
        "input": "5",
        "expected_output": "78.54"
    },

    # Medium Problems
    {
        "difficulty": "medium",
        "problem": "Find the GCD of two integers.",
        "input": "24 36",
        "expected_output": "12"
    },
    {
        "difficulty": "medium",
        "problem": "Print all prime numbers less than a given number.",
        "input": "10",
        "expected_output": "2 3 5 7"
    },
    {
        "difficulty": "medium",
        "problem": "Find the second largest number in a list of integers.",
        "input": "1 3 5 7 9",
        "expected_output": "7"
    },
    {
        "difficulty": "medium",
        "problem": "Check if a number is an Armstrong number.",
        "input": "153",
        "expected_output": "True"
    },
    {
        "difficulty": "medium",
        "problem": "Sort a list of integers in ascending order.",
        "input": "9 3 1 5 7",
        "expected_output": "1 3 5 7 9"
    },
    {
        "difficulty": "medium",
        "problem": "Print the Fibonacci sequence up to a given number.",
        "input": "10",
        "expected_output": "0 1 1 2 3 5 8"
    },
    {
        "difficulty": "medium",
        "problem": "Calculate the sum of squares of the first N natural numbers.",
        "input": "5",
        "expected_output": "55"
    },

    # Hard Problem
    {
        "difficulty": "hard",
        "problem": "Solve the N-Queens problem for a given board size.",
        "input": "4",
        "expected_output": "[[1, 3, 0, 2], [2, 0, 3, 1]]"
    }
]

# Mapping difficulty to match the choices in the model
difficulty_mapping = {
    "easy": "Easy",
    "medium": "Medium",
    "hard": "Hard"
}

# Loop through each problem and create a CodingQuestion instance
for problem in problems:
    CodingQuestion.objects.create(
        title=problem["problem"][:50],  # Title truncated if needed
        description=problem["problem"],
        difficulty=difficulty_mapping[problem["difficulty"]],
        constraints="",
        example_input=problem["input"],
        example_output=problem["expected_output"]
    )
print("All problems have been added.")
