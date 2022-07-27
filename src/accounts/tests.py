from django.test import TestCase


class ClassA:
    def __init__(self, score_):
        self.colour = "black"
        self.score = score_

    def pechat(self):
        print("Pishet class A")

    def return_list(self, *args):
        listic = list()
        for el in args:
            listic.append(el)
        return listic


class ClassB(ClassA):
    def __init__(self, score_, mood_):
        super().__init__(score_)
        self.mood = mood_

    def pechat(self):
        super(ClassB, self).pechat()
        print("Pishet class B")


    def return_list(self, *args):
        a = super().return_list(*args)
        a.append("GRG")
        return a


a = ClassA(50)
print(a.colour)
print(a.score)
a.pechat()

b = ClassB(250, mood_="HIU")
print(b.score)
b.pechat()
print(b.mood)
# print(b.return_list("er","ef"))
print(b.return_list("Ef", "GER"))
