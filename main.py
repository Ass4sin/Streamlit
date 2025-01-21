import streamlit as st
import pandas as pd
import mysql.connector

# Connexion à la base de données
conn = mysql.connector.connect(
    host='35.240.113.82',
    user='root',
    password='root',
    database='Streamlit_Info'
)
cursor = conn.cursor()

# Mapping des colonnes
COLUMN_MAPPING = {
    "Linked Url": "Linkedin",
    "Full Name": "Full_Name",
    "First Name": "First_Name",
    "Last Name": "Last_Name",
    "Job Title": "Job_Title",
    "Facebook Profile": "Facebook_Profile",
    "Location": "Location",
    "Company": "Company",
    "Company Website": "Company_Website",
    "Company Facebook": "Company_Facebook",
    "Company Email": "Company_Email",
    "Company Phone": "Company_Phone",
    "Industry": "Industry",
    "Team Size": "Team_Size",
    "Revenue Range": "Revenue_Range",
    "Total Funding": "Total_Funding",
    "Work Email #1": "Work_Email_1",
    "Work Email #1 Status": "Work_Email_1_Status",
    "Work Email #2": "Work_Email_2",
    "Work Email #2 Status": "Work_Email_2_Status",
    "Work Email #3": "Work_Email_3",
    "Work Email #3 Status": "Work_Email_3_Status",
    "Direct Email #1": "Direct_Email_1",
    "Direct Email #1 Status": "Direct_Email_1_Status",
    "Direct Email #2": "Direct_Email_2",
    "Direct Email #2 Status": "Direct_Email_2_Status",
    "Phone #1": "Phone_1"
}

def streamlit_app():
    st.title("Uploader et sauvegarder un fichier CSV dans la base de données")

    # Téléchargement du fichier
    uploaded_file = st.file_uploader("Mettez votre fichier CSV ou Excel", type=['csv', 'xlsx'])

    if uploaded_file:
        try:
            # Lire le fichier
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(".xlsx"):
                df = pd.read_excel(uploaded_file)

            # Ajouter une colonne "Source" vide
            df.insert(0, "Source", uploaded_file.name)

            # Nettoyer les colonnes et remplacer NaN
            df.columns = df.columns.str.strip()
            df = df.fillna("")

            # Renommer les colonnes
            df.rename(columns=COLUMN_MAPPING, inplace=True)

            # Afficher les données nettoyées
            st.success("Fichier téléchargé et nettoyé avec succès !")
            st.write(df.head())

            # Insérer les données dans la base
            for _, row in df.iterrows():
                sql = """
                    INSERT INTO CSV_Info (
                        Source, Linkedin, Full_Name, First_Name, Last_Name,
                        Job_Title, Facebook_Profile, Location, Company, Company_Website,
                        Company_Facebook, Company_Email, Company_Phone, Industry,
                        Revenue_Range, Total_Funding, Work_Email_1, Work_Email_1_Status,
                        Work_Email_2, Work_Email_2_Status, Work_Email_3, Work_Email_3_Status,
                        Direct_Email_1, Direct_Email_1_Status, Direct_Email_2,
                        Direct_Email_2_Status, Phone_1
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = tuple(row[col] for col in COLUMN_MAPPING.values())
                cursor.execute(sql, values)

            conn.commit()
            st.success("Données insérées avec succès dans la base de données !")

        except Exception as e:
            st.error(f"Une erreur s'est produite lors du traitement du fichier : {e}")

streamlit_app()
