import streamlit as st
from auth.authenticator import Authenticator
from home import run_home

#authenticator = Authenticator()

def main():
    """name, authentication_status, username = authenticator.login()
    role = authenticator.get_role(username)

    if authentication_status:
        authenticator.logout()        
        run_home(authenticator, role)

    elif authentication_status is False:
        st.error('Nom d\'utilisateur/mot de passe incorrect')

    elif authentication_status is None:
        st.warning('Veuillez entrer votre nom d\'utilisateur et mot de passe')
    """
    run_home(None, 'admin')

if __name__ == '__main__':
    main()
