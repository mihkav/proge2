import tkinter as tk
import math

alus = tk.Tk()
alus.title("Kettatelo")
alus.configure(background="#d9d9d9")
alus.resizable(width=False, height=False) #suurus lukus

#muutujad
rulli_nurk = 0.0 #praegune pöördenurk kraadides
lohistuse_alg = None #hiire nurk lohistuse alguses
alg_nurk = 0.0 # ratta_nurk vajutuse algpunktis
cx, cy = 260, 400 # rulliku keskpunkt
valitud_nr = ""

# näpuaugud
yhikud = ["0", "9", "8", "7", "6", "5", "4", "3", "2", "1"]
auk_kaug = 90 #kaugus keskpunktist iga auguni
auk_r = 16 #iga augu raadius
start_deg = 90 # esimese augu (number 0) asukoht kella 6 juurest

canvas = tk.Canvas(alus, width=800, height=600, bg="#1a1a1a", highlightthickness=0)
canvas.pack() # pack utleb et pane canvas alusele

# funktsioon et joonistada ümarate servadega kujundeid, teravad nurgad olid koledad
def draw_rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    # r = nurga raadius
    # igal nurgal 3 punkti, kaks äärtes 1 nurgas
    # smooth=True painutab nurga nende kolme punkti ymber
    # **kwargs laseb skippida praegu fill ja outline jms, need saab hiljem sisestada kui funktsiooni välja tood pmst placeholder

    punktid = [
        x1 + r, y1, x2 - r, y1,  # ylemine serv
        x2, y1, x2, y1 + r,  # parem ylemine nurk
        x2, y2 - r, x2, y2,  # parem serv
        x2 - r, y2, x1 + r, y2,  # alumine serv
        x1, y2, x1, y2 - r,  # vasak alumine nurk
        x1, y1 + r, x1, y1,  # vasak serv
        x1 + r, y1,  # tagasi algusesse
    ]
    return canvas.create_polygon(punktid, smooth=True, **kwargs)



#telo keha
draw_rounded_rect(canvas, 60,30,460,650, 40, fill="#2a1a0a", outline="#1c1008", width=3)
#heledam joon keha ümber ilu jaoks
draw_rounded_rect(canvas, 65, 35, 455, 645, 38,
                  fill="", outline="#5c3a1e", width=1)

# helistamise tekst
canvas.create_text(520, 250, text="", fill="#33ff66",
                   font=("Courier", 14, "bold"),
                   anchor="w",        # tekst joondub vasakust servast
                   tags="olek_tekst")

canvas.create_text(520, 280, text="", fill="#33ff66",
                   font=("Courier", 18, "bold"),
                   anchor="w",
                   tags="olek_nr")

#stop peg. fikseeritud, ei pöörle rulliku endaga, seega joonistatakse eraldi
def joonista_peg():
    peg_nurk = math.radians(50)  # 50 kraadi ehk laheb nullist paremale
    sise_r = 90
    valise_r = 125

    kx1 = cx + sise_r * math.cos(peg_nurk)
    ky1 = cy + sise_r * math.sin(peg_nurk)
    kx2 = cx + valise_r * math.cos(peg_nurk)
    ky2 = cy + valise_r * math.sin(peg_nurk)

    canvas.create_line(kx1, ky1, kx2, ky2,
                       fill="#aaaaaa", width=3)

#ekraan kus kuvatakse valitud numbrid
def joonista_ekraan():
    # ekraani taust
    canvas.create_rectangle(100, 80, 420, 140, fill="#0a1a0a", outline="#aaaaaa", width=2)

    # ekraani tekst — tühi alguses
    canvas.create_text(260, 110, text="", fill="#33ff66",font=("Courier", 22, "bold"),tags="ekraan") #tag teksti uuendamiseks


#hiire nurga arvutamine sõltuvalt rulliku keskpunktist
def hiire_nurk(event):
    #vahemaad keskpunktist
    dx = event.x - cx
    dy = event.y - cy
    #atan2 annab nurga radiaanides, teeme kraadideks
    return math.degrees(math.atan2(dy, dx))

def joonista_rullik():
    # rullik
    # create oval loob koordinaatiga ristküliku ja mahutab ringi selle sisse ehk praegu loob raadiusega 130 ringi keskpunkti ümber
    canvas.create_oval(cx - 130, cy - 130, cx + 130, cy + 130, fill="#1e1e1e", outline="#444444", width=1,
                       tags="rullik")
    # rulliku keskmine ring
    canvas.create_oval(cx - 42, cy - 42, cx + 42, cy + 42,
                       fill="#111111", outline="#444444", width=1, tags="rullik")

    for i, yhik in enumerate(yhikud):
        nurk_deg = start_deg - i * -30 + rulli_nurk  # 30 kraadi iga numbriaugu vahel
        nurk_rad = math.radians(nurk_deg)  # math tahab radiaane arvutamiseks

        # augu positsioon
        ax = cx + auk_kaug * math.cos(nurk_rad)
        ay = cy + auk_kaug * math.sin(nurk_rad)


        # augu ymbris
        canvas.create_oval(ax - auk_r, ay - auk_r, ax + auk_r, ay + auk_r, fill="#555555", outline="#444444", width=1,
                           tags="rullik")
        # augu sisemus
        canvas.create_oval(ax - auk_r + 3, ay - auk_r + 3, ax + auk_r - 3, ay + auk_r + 3, fill="#080808", outline="",
                           tags="rullik")
        # numbri tekst
        nr_r = auk_kaug + auk_r + 10
        nrx = cx + nr_r * math.cos(nurk_rad)
        nry = cy + nr_r * math.sin(nurk_rad)
        canvas.create_text(nrx, nry, text=yhik, fill="#ccbbaa", font=("Georgia", 9, "bold"), tags="rullik")

def vajutus(event):
    global lohistuse_alg, alg_nurk

    # vahemaa keskpunktist
    dx = event.x - cx
    dy = event.y - cy
    kaugus = math.hypot(dy, dx)

    #vajutus peab olema rulliku peal, mujal ei tohi töödata
    if 45 <= kaugus <= 140:
        lohistuse_alg = hiire_nurk(event)
        alg_nurk = rulli_nurk

def joonista_uuesti():
    canvas.delete("rullik")
    joonista_rullik() #rullik joonistatakse enne et see pegi ara ei kataks
    joonista_peg()

def lohistus(event):
    global rulli_nurk, lohistuse_alg, alg_nurk

    if lohistuse_alg is None:
        return

    praegune = hiire_nurk(event)

    #kui nurga muutus läheb üle 180 voi -180
    delta = praegune - lohistuse_alg
    if delta > 180: delta -= 360
    if delta < -180: delta += 360

    uus_nurk = rulli_nurk + delta

    #liikuda saab ainult vastupäeva, max 300 kraadi
    uus_nurk = max(-300.0, min(uus_nurk, 0.0))
    rulli_nurk = uus_nurk

    lohistuse_alg = praegune

    joonista_uuesti()


def vabastus(event):
    global lohistuse_alg

    lohistuse_alg = None

    # mitu sammu 30kraadist tõmmati
    sammud = int(abs(rulli_nurk) / 30)

    #sammutuvastus algab kui natukenegi tõmmati
    if sammud > 0:
        sammud = min(sammud, 10)
        nr = yhikud[sammud - 1]

        global valitud_nr
        valitud_nr += nr  # lisa number stringi lõppu
        canvas.itemconfig("ekraan", text=valitud_nr)  # uuenda ekraan

    poorle_tagasi()

#hiirevajutuste bindid
canvas.bind("<ButtonPress-1>",   vajutus)    #hiir alla
canvas.bind("<B1-Motion>",       lohistus)   #hiir all + liikumine
canvas.bind("<ButtonRelease-1>", vabastus)   #hiir yles

def poorle_tagasi():
    global rulli_nurk

    if rulli_nurk >= -0.1:
        #oleme alguses tagasi
        rulli_nurk = 0.0
        joonista_uuesti()
        return

    #liigu tiba tagasi alguse suunas, iga kord aeglasemini
    kiirus = abs(rulli_nurk) * 0.08 # sellega saab kiirust timmida
    kiirus = max(kiirus, 3.0) #minimaalne kiirus lõpu jaoks
    rulli_nurk += kiirus

    joonista_uuesti()
    alus.after(16, poorle_tagasi) #korda 16 millisekundi tagant


def helista():
    if valitud_nr == "":
        return
    canvas.itemconfig("olek_tekst", text="Helistatakse numbrile:")
    canvas.itemconfig("olek_nr", text=valitud_nr)

#helistamise nupp
nupp = tk.Button(canvas, text="HELISTA", command=helista,
                 bg="#1a3a1a", fg="#33ff66",
                 font=("Courier", 12, "bold"),
                 relief="raised", bd=3) #relief raised tõstatab selle esile, sellest tekivad need ääred nupu umber mida resetil pole

# nupp canvasele
canvas.create_window(260, 220, window=nupp)

#reset nupp
def reset():
    global valitud_nr
    valitud_nr = ""
    canvas.itemconfig("ekraan", text="")
    canvas.itemconfig("olek_tekst", text="")
    canvas.itemconfig("olek_nr", text="")

reset_nupp = tk.Button(canvas, text="reset", command=reset,
                       bg="#2a2a2a", fg="#888888",
                       font=("Courier", 8),
                       relief="flat", bd=1)
# nupp canvasele
canvas.create_window(260, 245, window=reset_nupp)

#alustab loopi
joonista_rullik()
joonista_peg()
joonista_ekraan()
alus.mainloop()


