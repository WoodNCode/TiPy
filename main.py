import streamlit as st
import tipy_qd

st.set_page_config(page_title="TiPy-QD Bemessungsumgebung", layout="wide")
st.title("TiPy-QD Bemessungsumgebung")

# Erzeugen von Tabs (z. B. Tab 1: Übersicht, Tab 2: Berechnung)
tab1, tab2 = st.tabs(["Übersicht", "Berechnung"])

with tab1:
    st.header("Übersicht")
    st.write("Hier können allgemeine Informationen zur App stehen.")

with tab2:
    st.header("Berechnung")
    # Falls du tab-spezifische Eingabewerte benötigst, kannst du hier mit st.number_input etc. arbeiten.
    # Der gesamte Berechnungscode wird aus dem Modul importiert und ausgeführt.
    ergebnis = tipy_qd.run_bemessung()
    st.text(ergebnis)

# Hinweis:
# Der Sidebar-Bereich (st.sidebar) ist global und kann nicht pro Tab separat definiert werden.
# Du könntest jedoch innerhalb eines Tabs z. B. mit st.columns eine "zweigeteilte" Ansicht erzeugen,
# um tab-spezifische Eingabemöglichkeiten zu simulieren.
