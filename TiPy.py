import streamlit as st

# Create Tabs
tab1, tab2, tab3 = st.tabs(["TiPy", "Anschluss", "Querschnitt"])

with tab1:
    st.header("TiPy")
    st.write("TiPy-QD ist eine Open-Source-Bemessungsumgebung in Python, welche als Grundlage für die parametrische Bemessung und Optimierung verschiedener Tragwerkskomponenten im Holzbau dient. Sie richtet sich explizit an Ingenieurinnen und Ingenieure, welche ihre Ideen frei entfalten möchten. Die Software ist quelloffen und die Nutzung ist zu Forschungs- und Entwicklungszwecken frei. TiPy-QD steht unter der GPL-Lizenz, wodurch der Quellcode angepasst und in beliebiger Form weiterverwendet werden darf. Zugleich verlangt die GPL, dass bei jeder Weiterentwicklung, die auf diesem Code beruht, das gleiche Lizenzmodell angewendet und der Code offen zugänglich gemacht wird.")
with tab2:
    st.header("Zwsichnittiger Schlitzblech Anschluss")
    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)
with tab3:
    st.header("Querschnitt")
    st.image("https://loremflickr.com/320/240/cross-section", width=200)
