import termcolor

class Menu():
    def __init__(self):

        self.running = True

        self.commands = {
            "exit": self.stop,
            "help": self.help,
        }

    def start(self):
        while self.running:
            c = str(input(" -> "))
            if c in self.commands:
                self.commands[c]()
            else:
                print("invalid command \n")

    def stop(self):
        self.running = False

    def help(self):
        print("""
        exit: end the program
        help: display this prompt
        """)

if __name__ == "__main__":
    menu = Menu()
    menu.start()