import requests
import sys

BASE_URL = 'http://localhost:5000'

def show_menu():
    print("\nМеню:")
    print("1. Создать")
    print("2. Показать")
    print("3. Изменить")
    print("4. Удалить")
    print("5. Выйти")
    return input("Выберите действие: ")

def create_url():
    normal_url = input("Введите полный URL: ")
    response = requests.post(BASE_URL, json={'normal_url': normal_url})
    if response.status_code == 201:
        print(f"Короткий URL: {response.json()['short_url']}")
    else:
        print(f"Ошибка: {response.json()['error']}")

def show_url():
    short_url = input("Введите короткий URL: ")
    response = requests.get(f"{BASE_URL}/{short_url}")
    if response.status_code == 200:
        print(f"Полный URL: {response.json()['normal_url']}")
    else:
        print(f"Ошибка: {response.json()['error']}")

def update_url():
    short_url = input("Введите короткий URL: ")
    new_url = input("Введите новый полный URL: ")
    response = requests.put(f"{BASE_URL}/{short_url}", json={'normal_url': new_url})
    if response.status_code == 200:
        print("URL успешно обновлен")
    else:
        print(f"Ошибка: {response.json()['error']}")

def delete_url():
    short_url = input("Введите короткий URL: ")
    response = requests.delete(f"{BASE_URL}/{short_url}")
    if response.status_code == 200:
        print("URL успешно удален")
    else:
        print(f"Ошибка: {response.json()['error']}")

def main():
    while True:
        choice = show_menu()
        if choice == '1':
            create_url()
        elif choice == '2':
            show_url()
        elif choice == '3':
            update_url()
        elif choice == '4':
            delete_url()
        elif choice == '5':
            print("Выход из программы")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == '__main__':
    main()