from user_interface import print_line


class CustomNetwork:
    def __init__(self):
        self.routers = []

    def add_router(self, router):
        self.routers.append(router)

    def print_network(self):
        print("Current network topology:")
        for i, r in enumerate(self.routers):
            print(f'{i}: {r.name}')
        print_line()
