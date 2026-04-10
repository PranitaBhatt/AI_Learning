#All four pillars represented
from abc import ABC, abstractmethod

# Abstraction
class Animal(ABC):
   def __init__(self, name):
       self.name = name # Public attribute
   @abstractmethod
   def speak(self):
       pass

# Inheritance & Polymorphism
class Dog(Animal):
   species = "Canine" # Class variable
   def __init__(self, name, age):
       super().__init__(name)
       self._age = age # Protected attribute
   def speak(self):
       return "Woof!"
   # Encapsulation with getter/setter
   def get_age(self):
       return self._age
   def set_age(self, age):
       if age > 0:
           self._age = age

# Multiple Inheritance
class Friendly:
   def greet(self):
       return "Wags tail!"
class GoldenRetriever(Dog, Friendly):
   def speak(self):
       return "Happy Woof!"
# Usage
dog = GoldenRetriever("Buddy", 3)
print(dog.name, dog.species, dog.speak(), dog.greet())
dog.set_age(4)
print("Age:", dog.get_age())