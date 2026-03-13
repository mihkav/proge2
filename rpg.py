
from abc import ABC, abstractmethod
import random
from time import sleep

class Tegelane(ABC):
    def __init__(self, nimi: str, hp: int):
        self._nimi = nimi #kapseldamine
        self._hp = hp #kapseldamine

    def on_elus(self):
        if self._hp > 0:
            return True
        else:
            return False

    def vota_kahju(self, kogus):
        self._hp = max(0, self._hp - kogus) #kui hp-kogus laheb alla nulli on null suurem arv ja tagastakse see

    def seisund(self):
        return f"{self._nimi} seisund: {self._hp} elu"

    @abstractmethod
    def runda(self, vastane): #abstraktsioon, seda hakkavad koik alamklassid ise muutma
        pass

class Sodalane(Tegelane):
    def __init__(self, nimi: str, hp: int):
        super().__init__(nimi, hp) #tegelase klassist nime ja hp pärimine

    def runda(self, vastane):
        dmg = random.randint(7, 35)
        print(f"{self._nimi} vehib mõõgaga ja tegi {dmg} DAMAGE")
        vastane.vota_kahju(dmg)

class Maag(Tegelane):
    def __init__(self, nimi: str, hp: int, mana: int):
        super().__init__(nimi, hp) #pärimine
        self._mana = mana #kapseldamine

    def seisund(self):
        return f"{self._nimi} seisund: {self._hp} elu, {self._mana} mana"

    def runda(self, vastane): #abstratksioon

        if self._mana > 5:
            dmg = random.randint(15, 30)
            self._mana = max(0, self._mana - 5)
            print(f"{self._nimi} vehib võlukepiga ja tegi {dmg} DAMAGE")
            vastane.vota_kahju(dmg)


        if self._mana <= 0:
            print(f"{self._nimi} rünnak ebaõnnestus! POLE PIISAVALT MANA")
            return

class Vibukytt(Tegelane):
    def __init__(self, nimi: str, hp: int, nooled: int):
        super().__init__(nimi, hp) #pärimine
        self._nooled = nooled #kapseldamine

    def seisund(self):
        return f"{self._nimi} seisund: {self._hp} elu, {self._nooled} noolt"

    def runda(self, vastane):

        if self._nooled > 0:
            dmg = random.randint(12, 31)
            self._nooled = max(0, self._nooled - 1)
            print(f"{self._nimi} laseb noole ja tegi {dmg} DAMAGE")
            vastane.vota_kahju(dmg)

        if self._nooled < 0:
            print(f"{self._nimi} rünnak ebaõnnestus! NOOLED OTSAS")



def lahing(p1, p2): #polümorfism

    print(f"\n---ALGAB LAHING: {p1._nimi} VS {p2._nimi}---")
    kord = 1

    while p1.on_elus() and p2.on_elus(): #lahingu loop kaib niikaua kuni üks player sureb

        print(f"\nKäik: {kord}")
        p1.runda(p2)
        if not p2.on_elus():
            print(f"{p2._nimi} on surnud. Lahingu võitis {p1._nimi}!")
            break

        p2.runda(p1)
        if not p1.on_elus():
            print(f"{p1._nimi} on surnud. Lahingu võitis {p2._nimi}!")
            break

        #peale mõlema playeri ründamist kuvatakse mõlemate seisundid
        print(f"{p1.seisund()} \n"
              f"{p2.seisund()}")

        kord += 1 #kaigu lopus lisame +1 korrale
        sleep(6) #lisasin sleep peale igat käiku, et terve lahing korraga ekraanile ei potsataks vaid peab ikka ootama pinges, et kumb võidab

def main():

    sodalane = Sodalane("Albert", 110)
    maag = Maag("Harry", 67, 30)
    vibur = Vibukytt("Taurus", 80, 12)

    lahing(vibur, maag)

if __name__ == "__main__":
    main()

#uue tegelase lisamiseks peab tegema lihtsalt uue Tegelase alamklassi ja andma talle oma voitlemisviis