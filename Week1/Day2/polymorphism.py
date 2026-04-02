#polymorphism
class animal:
    def sound(self):
        print("sound")

class owl(animal):
    def sound(self):
        print("owl whoo's")

class cat(animal):
    def sound(self):
        print("cat meow's")

owl=owl()
cat=cat()
owl.sound()
cat.sound()