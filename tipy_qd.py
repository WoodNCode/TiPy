# tipy_qd.py

import math
import sys
import os
import io

class TeeImSpeicher:
    """
    Leitet alle write()-Aufrufe sowohl in die Konsole als auch in einen StringIO-Puffer.
    """
    def __init__(self, console, memory):
        self.console = console
        self.memory = memory

    def write(self, data):
        self.console.write(data)
        self.memory.write(data)

    def flush(self):
        self.console.flush()

def main():
    """
    Enthält die komplette Berechnungslogik inkl. Eingabeaufforderungen und Ausgaben.
    (Hinweis: In einer Streamlit-App sollten direkte input()-Aufrufe vermieden und stattdessen entsprechende Widgets eingesetzt werden.)
    """
    # Beispielhafte Eingabewerte
    Holzart = "Nadelholz"
    Vorbohrung = "ja"
    Kraft_Faser_Winkel_alpha = 37
    rho_k = 385
    D = 6
    f_u_k = 360
    M_u_k = 10800
    t = 10
    b_Holz = 140
    n_h = 2
    n_n = 2
    a1 = 50
    Anzahl_Scherfugen = 2

    print("----- EINGABEDATEN -----")
    print(f"Holzart = {Holzart}")
    print(f"Vorbohrung = {Vorbohrung}")
    print(f"Kraft_Faser_Winkel_alpha = {Kraft_Faser_Winkel_alpha}°")
    print(f"rho_k = {rho_k} kg/m³")
    print(f"D = {D} mm")
    print(f"f_u_k = {f_u_k} N/mm²")
    if M_u_k is not None:
        print(f"M_u_k (vorgegeben) = {M_u_k} Nmm")
    else:
        print("M_u_k = None")
    print(f"t = {t} mm (Stahlblechdicke)")
    print(f"b_Holz = {b_Holz} mm (Holzbreite)")
    print(f"n_h = {n_h}")
    print(f"n_n = {n_n}")
    print(f"a1 = {a1} mm")
    print(f"Anzahl_Scherfugen = {Anzahl_Scherfugen}\n")

    # Hilfsfunktion zur linearen Interpolation
    def interpoliere_linear(alpha_deg, f_h0, f_h90):
        if alpha_deg <= 0 or alpha_deg >= 90:
            return None
        return f_h0 + (f_h90 - f_h0) * (alpha_deg / 90.0)

    try:
        if Holzart == "Nadelholz":
            if Vorbohrung == "nein":
                f_h_0_k = 0.082 * (D ** -0.3) * rho_k
                f_h_90_k = 0.082 * (D ** -0.3) * rho_k
            elif Vorbohrung == "ja":
                f_h_0_k = 0.082 * (1 - 0.01 * D) * rho_k
                f_h_90_k = f_h_0_k / (1.35 + 0.015 * D)
            else:
                raise ValueError("Ungültiger Wert für 'Vorbohrung' bei Nadelholz!")
        elif Holzart == "Laubholz":
            if Vorbohrung == "nein":
                raise ValueError("FEHLER: Laubholz muss immer vorgebohrt werden!")
            elif Vorbohrung == "ja":
                f_h_0_k = 0.082 * (1 - 0.01 * D) * rho_k
                f_h_90_k = f_h_0_k / (0.90 + 0.015 * D)
            else:
                raise ValueError("Ungültiger Wert für 'Vorbohrung' bei Laubholz!")
        else:
            raise ValueError("Ungültige Holzart!")

        print("\nBerechnete Lochleibungsfestigkeiten:")
        print(f"f_h,0,k = {round(f_h_0_k, 3)} N/mm²")
        print(f"f_h,90,k = {round(f_h_90_k, 3)} N/mm²")

        f_h_alpha_k = interpoliere_linear(Kraft_Faser_Winkel_alpha, f_h_0_k, f_h_90_k)
        if f_h_alpha_k is not None:
            print(f"f_h,α,k (α={Kraft_Faser_Winkel_alpha}°): {round(f_h_alpha_k,3)} N/mm²")
        else:
            print(f"Kein interpolierter Wert für α={Kraft_Faser_Winkel_alpha}° (außerhalb 0-90).")

        # Hier wird im Original per input() abgefragt. In einer Streamlit-Umgebung sollten
        # diese Werte als Widgets übergeben werden. Für dieses Beispiel wird festgelegt:
        auswahl = "alpha"  # Beispiel: Auswahl auf den interpolierten Wert
        if auswahl == "0":
            f_h_k = f_h_0_k
            print("\nDu hast f_h,0,k ausgewählt.")
        elif auswahl == "90":
            f_h_k = f_h_90_k
            print("\nDu hast f_h,90,k ausgewählt.")
        elif auswahl.lower() == "alpha":
            if f_h_alpha_k is not None:
                f_h_k = f_h_alpha_k
                print("\nDu hast f_h,α,k (interpoliert) ausgewählt.")
            else:
                raise ValueError("Für den Winkel α existiert kein interpolierter Wert!")
        else:
            raise ValueError("Ungültige Eingabe! Bitte '0', '90' oder 'alpha'.")

        print(f"→ f_h,k = {round(f_h_k, 3)} N/mm² wird für die weitere Bemessung verwendet.")

    except ValueError as e:
        print(f"\nFehler bei der Eingabe/Berechnung: {e}")
        f_h_k = None
    except Exception as ex:
        print(f"\nAllgemeiner Fehler: {ex}")
        f_h_k = None

    # Weitere Berechnungen (z. B. Fließmoment, Ermittlung t_1, etc.)
    if D <= 4 or D >= 30:
        print(f"\nAchtung: Der Durchmesser D={D} mm liegt außerhalb des Gültigkeitsbereichs (4 < D < 30).")
    else:
        if M_u_k is not None:
            print(f"\nM_u,k (vorgegeben) = {M_u_k} Nmm")
        else:
            if f_u_k is not None:
                M_u_k = 0.3 * f_u_k * (D ** 2.6)
                print(f"\nM_u,k (berechnet) = {round(M_u_k, 2)} Nmm")
            else:
                print("\nWeder M_u_k noch f_u_k vorhanden. Fließmoment kann nicht berechnet werden.")
                M_u_k = None

    if f_h_k is not None and f_h_k > 0 and f_u_k is not None:
        t_1 = (b_Holz - t) / 2
        t_1_erf = 2.52 * math.sqrt(f_u_k / f_h_k) * (D ** 0.8)
        print(f"\nt_1 = {round(t_1, 2)} mm")
        print(f"t_1_erf = {round(t_1_erf, 2)} mm")

        if t_1 > t_1_erf:
            print("\nBedingung t_1 > t_1_erf erfüllt. Die Rechnung wird fortgesetzt...")
            d = D
            alpha = Kraft_Faser_Winkel_alpha
            p = Anzahl_Scherfugen
            k_beta = min(t_1 / t_1_erf, 1.0) * 2
            k_alpha = 0.73
            n_tot = n_h * n_n
            k_red = (n_h ** -0.1) * ((a1 / (10 * d)) ** 0.25) * ((90 - alpha) / 90) + (alpha / 90)
            print(f"k_red = {round(k_red, 3)}")
            if k_red < 1.0:
                print("k_red < 1.0 → Weitere Rechnung wird durchgeführt.")
                Rd = (k_alpha
                      * k_red
                      * n_tot
                      * p
                      * k_beta
                      * (0.3 * f_u_k * f_h_k) ** 0.5
                      * (d ** 1.8))
                Rd_Verb = Rd / 1000.0
                print(f"Widerstand (berechnet) = {round(Rd_Verb, 2)} kN")
            else:
                print("k_red >= 1.0 → Keine weitere Rechnung!")
        else:
            print("\nFEHLER: t_1 <= t_1_erf! Keine weitere Rechnung möglich.")
    else:
        print("\nEntweder f_h_k oder f_u_k fehlen/ungültig. Keine weitere Berechnung möglich.")

def run_bemessung():
    """
    Führt die Berechnung aus und gibt alle Ausgaben als String zurück.
    """
    # Speicher den alten stdout, leite alle print-Ausgaben in einen Puffer um.
    alter_stdout = sys.stdout
    speicher_puffer = io.StringIO()
    tee = TeeImSpeicher(alter_stdout, speicher_puffer)
    sys.stdout = tee

    try:
        main()
    finally:
        sys.stdout = alter_stdout

    return speicher_puffer.getvalue()

if __name__ == "__main__":
    ergebnis = run_bemessung()
    print(ergebnis)
