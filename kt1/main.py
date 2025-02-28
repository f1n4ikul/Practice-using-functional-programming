lower_bound = None
upper_bound = None
current_guess = None

def start(n, m):
    global lower_bound, upper_bound, current_guess
    lower_bound = n
    upper_bound = m
    current_guess = (lower_bound + upper_bound) // 2
    return "Я готов..."

def guess_my_number():
    global current_guess
    if lower_bound is None or upper_bound is None:
        return "Сначала вызовите функцию start!"
    return current_guess

def smaller():
    global upper_bound, current_guess
    if lower_bound is None or upper_bound is None:
        return "Сначала вызовите функцию start!"
    upper_bound = current_guess - 1
    current_guess = (lower_bound + upper_bound) // 2
    return current_guess

def bigger():
    global lower_bound, current_guess
    if lower_bound is None or upper_bound is None:
        return "Сначала вызовите функцию start!"
    lower_bound = current_guess + 1
    current_guess = (lower_bound + upper_bound) // 2
    return current_guess

def play_game():
    print("Добро пожаловать в игру 'Угадай число наоборот'!")
    try:
        n = int(input("Введите нижнюю границу диапазона: "))
        m = int(input("Введите верхнюю границу диапазона: "))
        if n >= m:
            print("Нижняя граница должна быть меньше верхней границы!")
            return
    except ValueError:
        print("Пожалуйста, введите корректные числа.")
        return

    
    start(n, m)
    print(f"Я начал игру в диапазоне от {n} до {m}. Попробую угадать ваше число!")

    while True:
        guess = guess_my_number()
        print(f"Мое предположение: {guess}")
        user_input = input("Если я угадал, введите 'да'. Если ваше число меньше, введите '<'. Если больше, введите '>': ").strip().lower()

        if user_input == "да":
            print("Ура! Я угадал ваше число!")
            break
        elif user_input == "<":
            new_guess = smaller()
            if lower_bound > upper_bound:
                print("Похоже, вы дали противоречивые подсказки. Проверьте свои ответы!")
                break
        elif user_input == ">":
            new_guess = bigger()
            if lower_bound > upper_bound:
                print("Похоже, вы дали противоречивые подсказки. Проверьте свои ответы!")
                break
        else:
            print("Не понял ваш ответ. Пожалуйста, введите 'да', '<' или '>'.")


if __name__ == "__main__":
    play_game()
