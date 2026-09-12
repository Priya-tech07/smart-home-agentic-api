from app.agent import process_command


if __name__ == "__main__":
    command = "I'm going to bed, secure the house."

    result = process_command(command)

    print("\nFinal result:")
    print(result)