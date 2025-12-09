from sys import exit
import datetime as dt
import json
import os

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



def krmení():
    bezdak["hlad"] += 10
    print(f"{bezdak["jmeno"]} vypadá se najedl.")

def hra():
    bezdak["šťastnost"] = True
    bezdak["energie"] -= 10
    bezdak["hlad"] -= 10
    bezdak["žizen"] -= 10
    print(f"Bezďák je šťastný")

def spanek():
    bezdak["energie"] = 100
    print(f"Zzz...Zzz...Zzz...")
    print(f"Bezďák je čilí")

def status():
    print(f"""
    Kapacita žízně bezďáka je {bezdak["žizen"]}
    Kapacita žaludku bezďáka je {bezdak["hlad"]}
    Energie bezďáka je {bezdak["energie"]}
    Životy bezďáka jsou {bezdak["životy"]}
    {bezdak["jmeno"]} je {"šťastný" if bezdak["šťastnost"] == False else "Nešťastný"}
""")

def zkontroluj_status():
    if bezdak["hlad"] > 120 or bezdak["hlad"] < -20:
        bezdak["životy"] -= 10

    if bezdak["životy"] <= 0:
        bezdak["žije"] = False
        print(f"{bezdak["jmeno"]} umřel")
        exit()

def hladoveni():
    global puvodni_cas
    ted = dt.datetime.now()
    if ted > puvodni_cas + dt.timedelta(seconds=3):
        bezdak["hlad"] -= 10
        puvodni_cas = ted

def starnuti():
    global puvodni_cas
    ted = dt.datetime.now()
    if ted > puvodni_cas + dt.timedelta(hours=1):
        bezdak["věk"] += 1
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

def main():
    load()
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
    while True:
        print(f"Pro doplnění bezďáka stiskni k. Jeho kapacita žaludku je {bezdak["hlad"]}\nPro ukončení napiš konec")
        print(f"Pro zlepšení nálady napiš hra")
        print(f"Pro doplnění energie napiš s")
        print(f"Pro zobrazení statusu napiš status")
        print(f"Pro restartování hry napiš reset")


        uziv_input = input()
        match uziv_input.lower():
            case  "konec":
                print("pa pá")
                save()
                break
            case "k":
                krmení()
            case "hra":
                hra()
            case "s":
                spanek()
            case "status":
                status()
            case "reset":
                reset()
        hladoveni()
        starnuti()
        zkontroluj_status()
        if bezdak["hlad"] < 50:
            print(f"{bezdak["jmeno"]} začíná mít hlad")


if __name__ == "__main__":
    main()