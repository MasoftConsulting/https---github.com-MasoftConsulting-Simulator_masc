import math
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Simulateur de Loyer d'Imprimantes",
    page_icon="🖨️",
    layout="wide"
)

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

# Section 1: Type d'imprimante et volume d'impression
st.header("1. Configuration de l'Imprimante")
col1, col2 = st.columns(2)

with col1:
    type_imprimante = st.radio("Type d'imprimante", ["Mono", "Couleur"])
    
with col2:
    pages_par_mois = st.number_input("Nombre de pages par mois", min_value=100, max_value=100000, value=5000, step=100)

# Section 2: Coûts initiaux
st.header("2. Coûts Initiaux")
col1, col2, col3 = st.columns(3)

with col1:
    prix_machine = st.number_input(f"Prix d'achat de la machine ({devise})", min_value=0, value=5000, step=100)
    
with col2:
    fret_approche = st.number_input(f"Fret d'approche ({devise})", min_value=0, value=500, step=50)
    
with col3:
    transitaire = st.number_input(f"Frais de transitaire ({devise})", min_value=0, value=300, step=50)

# Section 3: Coûts d'installation et expertise
st.header("3. Installation et Expertise")
col1, col2 = st.columns(2)

with col1:
    cout_installation = st.number_input(f"Coût d'installation ({devise})", min_value=0, value=200, step=50)
    
with col2:
    salaire_expert = st.number_input(f"Salaire de l'expert ({devise})", min_value=0, value=400, step=50)

# Section 4: Coûts d'exploitation
st.header("4. Coûts d'Exploitation")

# Coûts variables selon le type d'imprimante
if type_imprimante == "Mono":
    cout_par_page = st.number_input(f"Coût par page mono ({devise})", min_value=0.0, value=0.03, step=0.01, format="%.3f")
else:
    cout_par_page = st.number_input(f"Coût par page couleur ({devise})", min_value=0.0, value=0.08, step=0.01, format="%.3f")

# Calcul des coûts
cout_initial_total = prix_machine + fret_approche + transitaire + cout_installation + salaire_expert
cout_exploitation_mensuel = pages_par_mois * cout_par_page
cout_total_contrat = cout_initial_total + (cout_exploitation_mensuel * duree_contrat)
loyer_mensuel = cout_total_contrat / duree_contrat

# Affichage des résultats
st.header("Résultats du Calcul")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Coût initial total", f"{cout_initial_total:,.0f} {devise}")
    
with col2:
    st.metric("Coût d'exploitation mensuel", f"{cout_exploitation_mensuel:,.0f} {devise}")

with col3:
    st.metric("Loyer mensuel recommandé", f"{loyer_mensuel:,.0f} {devise}")

# Détails du calcul
with st.expander("Voir le détail du calcul"):
    st.subheader("Détail des coûts")
    st.write(f"- Prix de la machine: {prix_machine:,.0f} {devise}")
    st.write(f"- Fret d'approche: {fret_approche:,.0f} {devise}")
    st.write(f"- Frais de transitaire: {transitaire:,.0f} {devise}")
    st.write(f"- Coût d'installation: {cout_installation:,.0f} {devise}")
    st.write(f"- Salaire de l'expert: {salaire_expert:,.0f} {devise}")
    st.write(f"- **Total coûts initiaux: {cout_initial_total:,.0f} {devise}**")
    
    st.write(f"- Coût d'exploitation par page: {cout_par_page:.3f} {devise}")
    st.write(f"- Volume mensuel: {pages_par_mois:,.0f} pages")
    st.write(f"- **Coût d'exploitation mensuel: {cout_exploitation_mensuel:,.0f} {devise}**")
    
    st.write(f"- Durée du contrat: {duree_contrat} mois")
    st.write(f"- **Coût total sur la durée: {cout_total_contrat:,.0f} {devise}**")
    st.write(f"- **Loyer mensuel: {loyer_mensuel:,.0f} {devise}**")

# Recommandation de contrat
st.header("Recommandation de Contrat")
st.info(f"""
Pour une imprimante {type_imprimante.lower()} avec un volume de {pages_par_mois:,.0f} pages/mois sur {duree_contrat} mois,
nous recommandons un loyer mensuel de **{loyer_mensuel:,.0f} {devise}**.

Ce prix inclut:
- L'amortissement de la machine et des frais initiaux
- Tous les consommables et coûts d'exploitation
- La maintenance et le support technique
""")

# Footer
st.markdown("---")
st.markdown("© 2025 - Simulateur de Loyer d'Imprimantes MASC - Tous droits réservés")