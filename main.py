# main.py
import streamlit as st
import tipy_qd

st.set_page_config(page_title="TiPy-QD Bemessungsumgebung", layout="wide")
st.title("TiPy-QD Bemessungsumgebung")

# Erzeugen von Tabs (z. B. Übersicht und Berechnung)
tab1, tab2 = st.tabs(["Übersicht", "Berechnung"])

with tab1:
    st.header("Übersicht")
    st.write("TiPy-QD ist eine Open-Source-Bemessungsumgebung in Python, welche als Grundlage für die parametrische Bemessung und Optimierung verschiedener Tragwerkskomponenten im Holzbau dient. Sie richtet sich explizit an Ingenieurinnen und Ingenieure, welche ihre Ideen frei entfalten möchten. Die Software ist quelloffen und die Nutzung ist zu Forschungs- und Entwicklungszwecken frei. TiPy-QD steht unter der GPL-Lizenz, wodurch der Quellcode angepasst und in beliebiger Form weiterverwendet werden darf. Zugleich verlangt die GPL, dass bei jeder Weiterentwicklung, die auf diesem Code beruht, das gleiche Lizenzmodell angewendet und der Code offen zugänglich gemacht wird.")

with tab2:
    st.header("Berechnung")
    st.subheader("Eingabeparameter")

    # Eingabewerte über Streamlit-Widgets
    Holzart = st.selectbox("Holzart", options=["Nadelholz", "Laubholz"])
    Vorbohrung = st.selectbox("Vorbohrung", options=["ja", "nein"])
    Kraft_Faser_Winkel_alpha = st.number_input("Kraft-Faser-Winkel (Grad)", value=37, min_value=1, max_value=89)
    rho_k = st.number_input("rho_k (kg/m³)", value=385)
    D = st.number_input("Durchmesser D (mm)", value=6, min_value=1)
    f_u_k = st.number_input("f_u_k (N/mm²)", value=360)
    M_u_k = st.number_input("M_u_k (Nmm, 0 falls nicht vorgegeben)", value=10800)
    t = st.number_input("Stahlblechdicke t (mm)", value=10)
    b_Holz = st.number_input("Holzbreite b_Holz (mm)", value=140)
    n_h = st.number_input("Anzahl VBM in Faserrichtung (n_h)", value=2, step=1)
    n_n = st.number_input("Anzahl VBM quer zur Faserrichtung (n_n)", value=2, step=1)
    a1 = st.number_input("Abstand der VBM in Faserrichtung (a1, mm)", value=50)
    Anzahl_Scherfugen = st.number_input("Anzahl Scherfugen", value=2, step=1)

    auswahl = st.selectbox("Auswahl der Lochleibungsfestigkeit", options=["0", "90", "alpha"])

    if st.button("Berechnung starten"):
        # Aufruf der Funktion mit den eingegebenen Parametern
        ergebnis = tipy_qd.run_bemessung(
            Holzart=Holzart,
            Vorbohrung=Vorbohrung,
            Kraft_Faser_Winkel_alpha=Kraft_Faser_Winkel_alpha,
            rho_k=rho_k,
            D=D,
            f_u_k=f_u_k,
            M_u_k=M_u_k,
            t=t,
            b_Holz=b_Holz,
            n_h=n_h,
            n_n=n_n,
            a1=a1,
            Anzahl_Scherfugen=Anzahl_Scherfugen,
            auswahl=auswahl
        )
        st.text(ergebnis)
