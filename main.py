import os
import json
from colored import Fore, Style


class Task:
    def __init__(self, name, is_done, is_important):
        self.__name = name
        self.__is_done = is_done
        self.__is_important = is_important

    def name(self):
        return self.__name

    def is_done(self):
        return self.__is_done

    def is_important(self):
        return self.__is_important

    def set_name(self, name):
        self.__name = name

    def set_is_done(self, is_done):
        self.__is_done = is_done

    def set_is_important(self, is_important):
        self.__is_important = is_important

    def to_dict(self):
        return {
            "name": self.__name,
            "is_done": self.__is_done,
            "is_important": self.__is_important
        }

    @classmethod
    def from_dict(cls, task):
        return cls(task["name"], task["is_done"], task["is_important"])


class Tasks:
    def __init__(self, tasks):
        self.tasks = tasks

    def add(self, content, is_done=False, is_important=False):
        task = Task(content, is_done, is_important)
        self.tasks.append(task)

    def remove(self, index):
        if len(self.tasks) <= index:
            return False

        self.tasks.pop(index)
        return True

    def edit(self, index, new_content):
        if len(self.tasks) <= index:
            return False

        task = self.tasks[index]
        task.set_name(new_content)
        return True

    def done(self, index):
        return self.__set_is_done(index, True)

    def undone(self, index):
        return self.__set_is_done(index, False)

    def important(self, index):
        return self.__set_is_important(index, True)

    def not_important(self, index):
        return self.__set_is_important(index, False)

    def get_all(self):
        return self.tasks

    def save_to_file(self, file_path):
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def __set_is_done(self, index, is_done):
        if len(self.tasks) <= index:
            return False

        task = self.tasks[index]
        task.set_is_done(is_done)
        return True

    def __set_is_important(self, index, is_important):
        if len(self.tasks) <= index:
            return False

        task = self.tasks[index]
        task.set_is_important(is_important)
        return True

    @classmethod
    def from_file(cls, file_path):
        with open(file_path, "r", encoding="utf-8") as file:

            parsed_tasks = [Task.from_dict(raw_task) for raw_task in json.load(file)]
            return cls(parsed_tasks)


def print_all(tasks):
    print('Those are your tasks:')

    for i, task in enumerate(tasks.get_all()):
        content = task.name()
        is_done = task.is_done()
        is_important = task.is_important()

        if is_done:
            content = ''.join(map(lambda char: char + u'\u0336', content))

        if is_important:
            print(f"{Style.BOLD}{Fore.YELLOW}{i + 1}. {content}{Style.reset}")
        else:
            print(f"{i + 1}. {content}")

    print('\nWhat do you want to do with them?')


def create_if_not_found(file_path):
    if os.path.exists(file_path):
        return

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump([], file, indent=4)


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    filepath = os.path.join(dirname, "tasks.json")

    create_if_not_found(filepath)

    tasks = Tasks.from_file(filepath)

    while True:
        print_all(tasks)

        print("1. Add the task\n"
              "2. Remove the task\n"
              "3. Edit the task\n"
              "4. Mark the task as 'done'\n"
              "5. Mark the task as 'undone'\n"
              "6. Mark the task as important\n"
              "7. Mark the task as not important\n"
              "9. Exit\n")

        while True:
            try:
                option = int(input(">> "))
                break
            except ValueError:
                print("Please, enter just a number")

        if option == 1:
            content = input("Enter the name of the task: ")
            tasks.add(content)

        elif option == 2:
            index = int(input('Which one do you want to remove: '))
            if not tasks.remove(index-1):
                print("ERROR: Index out of range.")

        elif option == 3:
            index = int(input('Which one do you want to edit: '))
            new_content = input('What is the new name of this task? ')
            if not tasks.edit(index-1, new_content):
                print("ERROR: Index out of range.")

        elif option == 4:
            index = int(input("Which one do you want to mark as 'done': "))
            if not tasks.done(index-1):
                print("ERROR: Index out of range.")

        elif option == 5:
            index = int(input("Which one do you want to mark as 'undone': "))
            if not tasks.undone(index-1):
                print("ERROR: Index out of range.")

        elif option == 6:
            index = int(input("Which one do you want to mark as important: "))
            if not tasks.important(index-1):
                print("ERROR: Index out of range.")

        elif option == 7:
            index = int(input("Which one do you want to mark as not important: "))
            if not tasks.not_important(index-1):
                print("ERROR: Index out of range.")

        elif option == 9:
            break

        else:
            print("Please, enter one of numbers above\n")

    tasks.save_to_file(filepath)
