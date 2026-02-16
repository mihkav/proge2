def roomanumbriks(nr: int) -> str:

    #kui arv valjaspool 1-1000 vahemikku viskab errori
    if not (1 <= nr <= 1000):
        raise ValueError("Lubatud on ainult arvud vahemikus 1–1000")

    # anname igale arvugrupile võimalikud väärtused
    tuhanded = ["", "M"]
    sajad = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
    kymned = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
    yhed = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

    # jagame numbri tuhandeteks, sadadeks, kümneteks ja ühtedeks ning liidame vastavad Rooma numbrid kokku

    return (
        tuhanded[nr // 1000] +
        sajad[(nr % 1000) // 100] +
        kymned[(nr % 100) // 10] +
        yhed[nr % 10]
    )

while True: #while loop et saaks erinevaid numbreid mugavalt testida
    sisend = input("Sisesta täisarv vahemikus 1–1000 (või 'exit' lõpetamiseks): ")

    # kui kasutaja tahab väljuda
    if sisend.lower() == "exit":
        print("Head aega!")
        break

    try:
        number = int(sisend)
        rooma = roomanumbriks(number)
        print(f"{number} Rooma numbrites on: {rooma}\n")

    #error management
    except ValueError as e:
        print("Viga:", e)
        print("Proovi uuesti.\n")