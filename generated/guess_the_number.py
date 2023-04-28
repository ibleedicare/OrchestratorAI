import random

def guess_the_number():
    secret_number = random.randint(1, 100)
    attempts = 0
    while True:
        try:
            guess = int(input("Guess the secret number (between 1 and 100): "))
            if guess not in range(1, 101):
                raise ValueError("Invalid input. Enter a number between 1 and 100.")
            attempts += 1
            if guess == secret_number:
                print(f"Congratulations! You guessed the number in {attempts} attempts.")
                break
            elif guess < secret_number:
                print("Too low! Try a higher number.")
            else:
                print("Too high! Try a lower number.")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    guess_the_number()