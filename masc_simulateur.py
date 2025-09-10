import math
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Configuration de la page
st.set_page_config(
    page_title="Simulateur de Loyer d'Imprimantes",
    page_icon="🖨️",
    layout="wide"
)

# Fonction pour sauvegarder les simulations
def sauvegarder_simulation(data):
    # Créer le dossier de sauvegarde s'il n'existe pas
    if not os.path.exists("sauvegardes"):
        os.makedirs("sauvegardes")
    
    # Nom du fichier avec timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"sauvegardes/simulation_{timestamp}.json"
    
    # Sauvegarder les données
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    
    return filename

# Titre de l'application
st.title("🖨️ Simulateur de Loyer d'Imprimantes")
st.markdown("""
Cet outil vous permet de calculer le loyer mensuel à proposer à vos clients pour la location d'imprimantes,
en prenant en compte tous les coûts d'exploitation et d'installation.
""")

# Sidebar pour les paramètres généraux
with st.sidebar:
    st.header("Paramètres Généraux")
    devise = st.selectbox("Devise", ["CFA", "EUR"])
    duree_contrat = st.slider("Durée du contrat (mois)", 12, 60, 24)
    marge_beneficiaire = st.slider("Marge bénéficiaire (%)", 0, 50, 15)

# Section 1: Type d'imprimante
st.header("1. Configuration de l'Imprimante")
type_imprimante = st.radio("Type d'imprimante", ["Mono", "Couleur"])

# Section 2: Volume d'impression
st.header("2. Volume d'Impression")
pages_par_mois = st.number_input("Nombre total de pages par mois", min_value=100, max_value=100000, value=5000, step=100)

# Section 3: Coûts d'exploitation
st.header("3. Coûts d'Exploitation")

if type_imprimante == "Couleur":
    st.subheader("Répartition des pages")
    col1, col2 = st.columns(2)
    
    with col1:
        pages_couleur = st.number_input("Nombre de pages couleur", min_value=0, max_value=pages_par_mois, value=int(pages_par_mois * 0.3), step=100)
    
    with col2:
        pages_noir = st.number_input("Nombre de pages noir & blanc", min_value=0, max_value=pages_par_mois, value=int(pages_par_mois * 0.7), step=100)
    
    # Ajustement automatique pour que la somme ne dépasse pas le total
    if pages_couleur + pages_noir > pages_par_mois:
        st.warning(f"La somme des pages couleur et noir & blanc ({pages_couleur + pages_noir}) dépasse le total de pages ({pages_par_mois}). Ajustement automatique.")
        ratio = pages_par_mois / (pages_couleur + pages_noir)
        pages_couleur = int(pages_couleur * ratio)
        pages_noir = int(pages_noir * ratio)
        st.write(f"Pages couleur ajustées: {pages_couleur}")
        st.write(f"Pages noir & blanc ajustées: {pages_noir}")
    
    col1, col2 = st.columns(2)
    with col1:
        cout_page_couleur = st.number_input(f"Coût par page couleur ({devise})", min_value=0.0, value=0.08, step=0.01, format="%.3f")
    with col2:
        cout_page_noir = st.number_input(f"Coût par page noir & blanc ({devise})", min_value=0.0, value=0.03, step=0.01, format="%.3f")
else:
    # Pour les imprimantes mono, tout est en noir et blanc
    pages_noir = pages_par_mois
    pages_couleur = 0
    cout_page_noir = st.number_input(f"Coût par page ({devise})", min_value=0.0, value=0.03, step=0.01, format="%.3f")
    cout_page_couleur = 0

# Section 4: Coûts initiaux
st.header("4. Coûts Initiaux")
col1, col2, col3 = st.columns(3)

with col1:
    prix_machine = st.number_input(f"Prix d'achat de la machine ({devise})", min_value=0, value=5000, step=100)
    
with col2:
    fret_approche = st.number_input(f"Fret d'approche ({devise})", min_value=0, value=500, step=50)
    
with col3:
    transitaire = st.number_input(f"Frais de transitaire ({devise})", min_value=0, value=300, step=50)

# Section 5: Coûts d'installation et expertise
st.header("5. Installation et Expertise")
col1, col2 = st.columns(2)

with col1:
    cout_installation = st.number_input(f"Coût d'installation ({devise})", min_value=0, value=200, step=50)
    
with col2:
    salaire_expert = st.number_input(f"Quote par Expert ({devise})", min_value=0, value=400, step=50)

# Section 6: Coûts de consommables
st.header("6. Coûts de Consommables")
cout_consommables = st.number_input(f"Coût mensuel des consommables ({devise})", min_value=0, value=150, step=10)

# Calcul des coûts
cout_initial_total = prix_machine + fret_approche + transitaire + cout_installation + (salaire_expert * duree_contrat)
cout_exploitation_mensuel = (pages_couleur * cout_page_couleur) + (pages_noir * cout_page_noir) + cout_consommables
cout_total_contrat = cout_initial_total + (cout_exploitation_mensuel * duree_contrat)
loyer_sans_marge = cout_total_contrat / duree_contrat
loyer_avec_marge = loyer_sans_marge * (1 + marge_beneficiaire / 100)

# Affichage des résultats
st.header("Résultats du Calcul")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Coût initial total", f"{cout_initial_total:,.0f} {devise}")
    
with col2:
    st.metric("Coût d'exploitation mensuel", f"{cout_exploitation_mensuel:,.0f} {devise}")

with col3:
    st.metric("Loyer mensuel (sans marge)", f"{loyer_sans_marge:,.0f} {devise}")

st.success(f"### Loyer mensuel recommandé (avec {marge_beneficiaire}% de marge): {loyer_avec_marge:,.0f} {devise}")

# Détails du calcul
with st.expander("Voir le détail du calcul"):
    st.subheader("Détail des coûts initiaux")
    st.write(f"- Prix de la machine: {prix_machine:,.0f} {devise}")
    st.write(f"- Fret d'approche: {fret_approche:,.0f} {devise}")
    st.write(f"- Frais de transitaire: {transitaire:,.0f} {devise}")
    st.write(f"- Coût d'installation: {cout_installation:,.0f} {devise}")
    st.write(f"- Salaire de l'expert: {salaire_expert:,.0f} {devise}")
    st.write(f"- **Total coûts initiaux: {cout_initial_total:,.0f} {devise}**")
    
    st.subheader("Détail des coûts d'exploitation mensuels")
    if type_imprimante == "Couleur":
        st.write(f"- Pages couleur: {pages_couleur:,.0f} × {cout_page_couleur} {devise} = {pages_couleur * cout_page_couleur:,.0f} {devise}")
        st.write(f"- Pages noir & blanc: {pages_noir:,.0f} × {cout_page_noir} {devise} = {pages_noir * cout_page_noir:,.0f} {devise}")
    else:
        st.write(f"- Pages: {pages_noir:,.0f} × {cout_page_noir} {devise} = {pages_noir * cout_page_noir:,.0f} {devise}")
    st.write(f"- Consommables: {cout_consommables:,.0f} {devise}")
    st.write(f"- **Coût d'exploitation mensuel: {cout_exploitation_mensuel:,.0f} {devise}**")
    
    st.subheader("Calcul du loyer")
    st.write(f"- Durée du contrat: {duree_contrat} mois")
    st.write(f"- Coût total sur la durée: {cout_total_contrat:,.0f} {devise}")
    st.write(f"- Loyer mensuel sans marge: {cout_total_contrat:,.0f} / {duree_contrat} = {loyer_sans_marge:,.0f} {devise}")
    st.write(f"- Marge bénéficiaire: {marge_beneficiaire}%")
    st.write(f"- **Loyer mensuel avec marge: {loyer_avec_marge:,.0f} {devise}**")

# Bouton de sauvegarde
if st.button("💾 Sauvegarder la simulation"):
    simulation_data = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type_imprimante": type_imprimante,
        "pages_par_mois": pages_par_mois,
        "prix_machine": prix_machine,
        "fret_approche": fret_approche,
        "transitaire": transitaire,
        "cout_installation": cout_installation,
        "salaire_expert": salaire_expert,
        "cout_consommables": cout_consommables,
        "duree_contrat": duree_contrat,
        "loyer_sans_marge": loyer_sans_marge,
        "marge_beneficiaire": marge_beneficiaire,
        "loyer_avec_marge": loyer_avec_marge,
        "devise": devise
    }
    
    if type_imprimante == "Couleur":
        simulation_data["pages_couleur"] = pages_couleur
        simulation_data["pages_noir"] = pages_noir
        simulation_data["cout_page_couleur"] = cout_page_couleur
        simulation_data["cout_page_noir"] = cout_page_noir
    
    filename = sauvegarder_simulation(simulation_data)
    st.success(f"Simulation sauvegardée dans {filename}")

# Recommandation de contrat
st.header("Recommandation de Contrat")
st.info(f"""
Pour une imprimante {type_imprimante.lower()} avec un volume de {pages_par_mois:,.0f} pages/mois sur {duree_contrat} mois,
nous recommandons un loyer mensuel de **{loyer_avec_marge:,.0f} {devise}** (incluant {marge_beneficiaire}% de marge).

Ce prix inclut:
- L'amortissement de la machine et des frais initiaux
- Tous les consommables et coûts d'exploitation
- La maintenance et le support technique
- Une marge bénéficiaire de {marge_beneficiaire}%
""")

# Footer
st.markdown("---")
st.markdown("© 2025 - Simulateur de Loyer d'Imprimantes - Tous droits réservés")