from shell import Shell


# абстрактная сцена, такая, как главное меню или сама игра
class Scene:
    def __init__(self, shell: Shell):
        self.shell = shell

    def run(self):
        return None
