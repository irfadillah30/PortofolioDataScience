import streamlit as st

st.set_page_config(layout='wide')

st.markdown(
    """
    <style>
    /* Judul tengah */
    .judul-container {
        text-align: center;
        font-size: 3.5rem;
        font-weight: bold;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="judul-container">
        Portofolio Data Science
    </div>
    """,
    unsafe_allow_html=True,
)


page = st.radio(
    '',
    ['About Me', 'Project', 'Prediction', 'Contact'],
    horizontal=True
)


if page == 'About Me':
    import about_me
    about_me.about_me()
elif page == 'Project':
    import project
    project.project()
elif page == 'Prediction':
    import prediksi
    prediksi.prediction()
elif page == 'Contact':
    import kontak
    kontak.kontak()
