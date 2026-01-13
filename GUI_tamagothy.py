from sys import exit
import datetime as dt
import json
import os
from nicegui import ui
import asyncio
from PIL import Image


zprava = None
tabulka = True
spritesheet = Image.open("cat.png")
obrazek = None

bezdak = {}
default_bezdak = {
    "jmeno": "D-9341",
    "žizen": 0,
    "hlad": 50,
    "barva": "zelená",
    "životy": 100,
    "čistota": 100,
    "energie": 90,
    "žije": True,
    "věk": 0,
    "šťastnost": False,
    "poruchy": False,
    "rychlost": 0
}

puvodni_cas = dt.datetime.now()



async def krmeni():
    bezdak["hlad"] += 10
    obrazek.source = vystrihni_obrazek(3, 65)
    print(f"{bezdak["jmeno"]} se najedl.")
    zprava.content = f"{bezdak["jmeno"]} se najedl."
    print(f"{bezdak["jmeno"]} se najedl. Kapacita žaludku je {bezdak["hlad"]}")
    ui.notify(f"hlad +10", group=False, position="bottom-left", color="green")
    await asyncio.sleep(0.5)
    obrazek.source = vystrihni_obrazek(0, 28)
    allcontrol()

async def zizen():
    bezdak["žizen"] += 10
    obrazek.source = vystrihni_obrazek(3, 65)
    print(f"{bezdak["jmeno"]} se napil.")
    zprava.content = f"{bezdak["jmeno"]} se napil."
    print(f"{bezdak["jmeno"]} se najedl. Kapacita žízně je {bezdak["žizen"]}")
    ui.notify(f"žízeň +10", group=False, position="bottom-left", color="green")
    await asyncio.sleep(0.5)
    obrazek.source = vystrihni_obrazek(0, 28)
    allcontrol()

async def hra():
    obrazek.source = vystrihni_obrazek(3, 63)
    bezdak["šťastnost"] = True
    bezdak["energie"] -= 10
    bezdak["hlad"] -= 10
    bezdak["žizen"] -= 10
    print(f"Bezďák je šťastný")
    ui.notify(f"energie -10", group=False, position="bottom-left", color="pink")
    ui.notify(f"hlad -10", group=False, position="bottom-left", color="pink")
    ui.notify(f"žízeň -10", group=False, position="bottom-left", color="pink")
    zprava.content = f"Bezďák je šťastný"
    await asyncio.sleep(0.5)
    obrazek.source = vystrihni_obrazek(0, 0)
    allcontrol()


async def spanek():
    bezdak["energie"] = 100
    print(f"Zzz...Zzz...Zzz...")
    print(f"Bezďák je čilý")
    obrazek.source = vystrihni_obrazek(1, 49)
    zprava.content = f"Zzz...Zzz...Zzz..."
    await asyncio.sleep(1)
    zprava.content = f"Bezďák je čilý"
    ui.notify(f"energie FULL", group=False, position="bottom-left", color="blue")
    obrazek.source = vystrihni_obrazek(0, 20)
    allcontrol()


def status():

    print(f"""
    Kapacita žízně bezďáka je {bezdak["žizen"]}.
    Kapacita žaludku bezďáka je {bezdak["hlad"]}.
    Energie bezďáka je {bezdak["energie"]}.
    Životy bezďáka jsou {bezdak["životy"]}.
    {bezdak["jmeno"]} je {"šťastný" if bezdak["šťastnost"] == False else "Nešťastný"}.
""")
    tabulka = f"""
    Kapacita žízně bezďáka je {bezdak["žizen"]}.<br>
    Kapacita žaludku bezďáka je {bezdak["hlad"]}.<br>
    Energie bezďáka je {bezdak["energie"]}.<br>
    Životy bezďáka jsou {bezdak["životy"]}.<br>
    {bezdak["jmeno"]} je {"šťastný" if bezdak["šťastnost"] == False else "Nešťastný"}.<br>
"""
    allcontrol()

def zkontroluj_status():
    if bezdak["hlad"] > 120 or bezdak["hlad"] < -20:
        bezdak["životy"] -= 10
        ui.notify(f"Životy -10", group=False, position="top-right", color="red")

    if bezdak["žizen"] > 120 or bezdak["žizen"] < -20:
        bezdak["životy"] -= 10
        ui.notify(f"Životy -10", group=False, position="top-right", color="red")

    if bezdak["životy"] <= 0:
        bezdak["žije"] = False
        print(f"{bezdak["jmeno"]} umřel")
        zprava.content = f"{bezdak["jmeno"]} zemřel ve věku {bezdak["věk"]}"
        ui.shutdown()
        exit()
    
    if bezdak["hlad"] < 30:
        print(f"{bezdak["jmeno"]} začíná mít hlad")
        zprava.content = f"Bezďák začíná mít hlad"
    
    if bezdak["hlad"] < 0:
        print(f"{bezdak["jmeno"]} hladový")
        zprava.content = f"Bezďák hladový"

    if bezdak["žizen"] < 30:
        print(f"{bezdak["jmeno"]} začíná mít žízeň")
        zprava.content = f"Bezďák začíná mít žízeň"
    
    if bezdak["žizen"] < 0:
        print(f"{bezdak["jmeno"]} je žíznivý")
        zprava.content = f"Bezďák je žíznivý"

def hladoveni():
    global puvodni_cas
    ted = dt.datetime.now()
    if ted > puvodni_cas + dt.timedelta(seconds=3):
        bezdak["hlad"] -= 10
        print("hlad -10")
        ui.notify(f"hlad -10", group=False, position="bottom-right", color="pink")
        bezdak["žizen"] -= 10
        print("žízeň -10")
        ui.notify(f"žízeň -10", group=False, position="bottom-right", color="pink")
        puvodni_cas = ted

def starnuti():
    global puvodni_cas
    ted = dt.datetime.now()
    if ted > puvodni_cas + dt.timedelta(hours=1):
        bezdak["věk"] += 1
        ui.notify(f"+1 rok", color="blue")
        puvodni_cas = ted

def load():
    global bezdak, default_bezdak

    if os.path.isfile("save.json"):
        with open("save.json", "r", encoding="utf-8") as f:
            bezdak = json.load(f)
    else :
        bezdak = default_bezdak
        save()

def save():
    global bezdak
    with open("save.json", "w", encoding="utf-8") as f:
        json.dump(bezdak, f, ensure_ascii=False, indent=4)

def reset():
    global bezdak, default_bezdak
    bezdak = default_bezdak
    save()

def vystrihni_obrazek(x, y):
    x = x * 64
    y = y * 64
    return spritesheet.crop((x, y, x + 64, y + 64))

def allcontrol():
    zkontroluj_status()
    hladoveni()
    starnuti()
def main():
    global zprava, obrazek

    tlacitka = {
        "Krmení": krmeni,
        "Hra": hra,
        "Spánek": spanek,
        "Status": status,
        "Pití": zizen
    }

    load()

    ui.query("body").style("background-color: pink")

    with ui.element("div").classes("w-full h-screen flex items-center justify-center flex-col gap-5"):
        tabulka = ui.markdown(f"""Kapacita žízně bezďáka je {bezdak["žizen"]}.<br>
    Kapacita žaludku bezďáka je {bezdak["hlad"]}.<br>
    Energie bezďáka je {bezdak["energie"]}.<br>
    Životy bezďáka jsou {bezdak["životy"]}.<br>
    {bezdak["jmeno"]} je {"šťastný" if bezdak["šťastnost"] == False else "Nešťastný"}.<br>""")
        obrazek = ui.image(vystrihni_obrazek(0, 0)).classes("h-32 w-32")
        zprava = ui.markdown("Vítej").classes("whitespace-pro-line")
        with ui.grid(columns=3):
            for jmeno, funkce in tlacitka.items():
                ui.button(jmeno, on_click=funkce).classes("!bg-purple-200 text-black rounded-full")



    print("""
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⣾⢿⣿⡟⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣱⣾⣱⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⢀⣿⣾⣿⣿⣷⣦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡔⠁⠠⢀⢠⣿⣿⣿⣿⣿⣿⣿⣿⣿⡖⠒⠠⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⡗⢉⣠⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠄⠠⣰⠀⠀⠀⠀
⠀⠀⠀⢀⣠⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⣿⣿⣿⣿⣷⣶⣾⡀⠀⠀⠀
⠀⠀⢀⣾⡿⢿⣿⣿⣿⣿⣿⣿⣿⡿⢏⣀⣱⣈⡿⣿⣿⣿⣿⡿⢿⡆⠀⠀
⠀⠀⠈⣿⣷⣄⡉⠙⡿⠿⠿⣿⣿⣶⣿⣷⣿⣏⣁⠀⣿⡉⠈⣱⡎⠃⠀⠀
⠀⠀⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⠋⠀⠀⠀⠀
⠀⢰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀
⠀⠀⢹⣿⣿⡿⠋⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⠻⡿⠁⠀⠀⠀
⠀⠀⠀⠹⣿⣇⠰⠀⢆⠈⡹⣿⣿⣿⠿⠹⣿⣿⣿⣿⠏⣀⠎⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠈⠉⠉⠉⠉⣆⢂⣽⢿⠀⠰⣟⡾⡍⢰⠊⠀⠀⠀⠀⠀⡀⠂
⡄⠂⠈⠄⠐⠀⠂⠀⡌⠤⣣⣾⣻⠁⠀⠀⠙⢽⣻⣄⠣⣄⠠⠈⠐⠠⠀⠄
""")
    print("         Vítej pod mostem!")

    print(f"Pro doplnění bezďáka stiskni k. Jeho kapacita žaludku je {bezdak["hlad"]}\nPro ukončení napiš konec")
    print(f"Pro zlepšení nálady napiš hra")
    print(f"Pro doplnění energie napiš s")
    print(f"Pro zobrazení statusu napiš status")
    print(f"Pro restartování hry napiš reset")

   
    hladoveni()
    starnuti()
    zkontroluj_status()
    ui.run(native=True)
main()