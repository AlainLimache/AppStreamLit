# Configuration and Dependencies:
   1) Create a virtual environment (only on the first run, otherwise proceed to step 2):
       Use Python or Python3, depending on your installation:
           python3 -m venv venv
           or
           python -m venv venv

   2) Activate the virtual environment:
       On Linux/MacOS:
           source venv/bin/activate
       On Windows:
           # With cmd.exe:
               venv\Scripts\activate.bat
           # With PowerShell:
               venv\Scripts\Activate.ps1

   3) Install dependencies (only on the first run of the virtual environment, otherwise proceed to step 4):
       pip install -r requirements.txt
       pip install matplotlib
       pip install streamlit
       pip install scikit-learn
       pip install seaborn
       pip install plotly
       pip install streamlit-authenticator
       pip install statsmodels

   4) Launch the Streamlit application locally:
       streamlit run app.py


# Project Structure:
   Project Root:
     - graphes_deux_annees.py: contains functions for plotting graphs for two years
     - graphes_une_annees.py: contains functions for plotting graphs for one year
     - insight_plot.py: contains functions for plotting insight for your data
     - insight_page.py: contains functions for displaying the insight page
     - insight_calculation.py: contains functions for statistical tests
     - home.py: contains functions for displaying the home page
     - plot_functions_deux_annees.py: contains functions for creating graphs for two years
     - plot_functions_une_annee.py: contains functions for creating graphs for one year
     - app.py: main file of the application
     - Utils.py: contains utility functions used by other .py files

   auth Folder:
     - __init__.py/add_user.py/authenticator.py/database.py: authentication and user management

   data Folder:
     - Data1007.csv: data provided at the beginning of the project (unchanged)


# Using the application:
   1) Import the Data1007.csv file (for one year) and, if needed, the New_Data1007.csv file (for two years) located in the "data" folder
   2) Choose the variables to display in the application using the options on the left side of the page
   3) Hover over the various graphs with the mouse to get more precise information (exact value, corresponding category, etc.)
   4) If needed, display options (zoom, full screen) are available at the top right of each graph


# Generating a new CSV file:
   Run the generation.py script
   This will generate a new file named NewData1007.csv containing modified data.
   Note: - Only data related to averages will be modified; responses to questions will remain unchanged.
         - The CSV file separator is ";"