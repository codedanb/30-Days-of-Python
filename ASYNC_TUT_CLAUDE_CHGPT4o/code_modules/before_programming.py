"""
Module: Before Programming

This module introduces the concept of programming, how computers execute instructions, and what "waiting" means in computing.
"""

def what_is_programming():
    """Explain what programming is."""
    return "Programming is the process of giving clear and specific instructions to a computer to perform tasks."

def how_computers_execute_instructions():
    """Explain how computers execute instructions."""
    steps = [
        "1. Input: The computer receives data.",
        "2. Processing: It follows the instructions step by step.",
        "3. Output: It produces a result."
    ]
    return "\n".join(steps)

def what_is_waiting():
    """Explain what waiting means in computing."""
    return (
        "Waiting in computing happens when the computer is idle because it is waiting for something to happen, "
        "such as a file download or a response from a website."
    )

# Testable functions
def test_module():
    print("--- What is Programming? ---")
    print(what_is_programming())

    print("\n--- How Computers Execute Instructions ---")
    print(how_computers_execute_instructions())

    print("\n--- What is Waiting? ---")
    print(what_is_waiting())

if __name__ == "__main__":
    test_module()