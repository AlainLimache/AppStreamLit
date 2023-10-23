import streamlit as st
import matplotlib.colors as mcolors
import seaborn as sns

class Utils:
    @staticmethod
    def getCategories_question():
        categories_questions = [
            'MOY_PRATIQUES_CARRIERE', 'MOY_CLIMAT_SANTE_SECURITE',
            'MOY_SOUTIEN_EQUILIBRE_VIEPRO_VIEPERO', 'MOY_RECONNAISSANCE',
            'MOY_COMMUNICATION', 'MOY_JUSTICE', 'MOY_PARTICIPATION',
            'MOY_DIALOGUE_SOCIAL', 'MOY_POV', 'MOY_PO_FIT',
            'MOY_ENGAGEMENT_AFFECTIF', 'MOY_CONFIANCE', 'MOY_OCBO',
            'MOY_OCBI', 'MOY_VITALITE', 'MOY_APPRENTISSAGE', 'MOY_CROISSANCEPRO',
            'MOY_PSYC_AUTO_EFFICACITE', 'MOY_PSYC_ESPOIR', 'MOY_PSYC_OPTIMISME',
            'MOY_PSYC_RESILIENCE', 'MOY_PSYCAP', 'MOY_EQUILIBRE', 'MOY_BESOIN_DE_RECUPERATION',
        ]
        return categories_questions
    
    @staticmethod
    def getVariables():
        variables = ['Sexe', 'Age', 'Situation familiale', 'Diplôme', 'Type de contrat',
                 'Temps plein/partiel', 'Niveau hiérarchique', 'Fonction d\'encadrement',
                 'Durée dans l\'organisation', 'Secteur', 'Nombre de personne dans le service'
        ]
        return variables

    @staticmethod
    def newLines(n):
        for _ in range(n):
            st.write("")

    @staticmethod
    def newLinesSidebar(n):
        newline_str = "".join(["<br>" for _ in range(n)])
        st.sidebar.markdown(newline_str, unsafe_allow_html=True)
    
    @staticmethod
    def add_separator():
        st.sidebar.markdown("---")


    # Convert Matplotlib colors to hexadecimal format
    @staticmethod
    def convert_color_to_hex(color):
        return mcolors.to_hex(color)
    
    # Formater les nom des catégories
    @staticmethod
    def format_category_name(category):
        return category.replace("MOY_", "").replace("_", " ")
    
    @staticmethod
    def format_variable_name(variable_name):
        return variable_name.replace('_', ' ').capitalize()
    
    @staticmethod
    def get_color_palette(n_colors):
        """
        Returns a list of n_colors colors from the default seaborn color palette.
        """
        return sns.color_palette(n_colors=n_colors).as_hex()