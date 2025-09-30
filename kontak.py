def kontak():
    import streamlit as st

    st.title("Contact Page")

    st.write("You can reach me through the following channels:")

    # Link dengan logo
    st.markdown("""
    <table>
        <tr>
            <td><a href="mailto:irfadillahafninurvita@gmail.com" target="_blank">
                <img src="https://img.icons8.com/color/48/000000/gmail.png"/>
            </a></td>
            <td><a href="https://www.linkedin.com/in/irfadillahafninurvita05/" target="_blank">
                <img src="https://img.icons8.com/color/48/000000/linkedin.png"/>
            </a></td>
            <td><a href="https://github.com/irfadillah30/PortofolioDataScience" target="_blank">
                <img src="https://img.icons8.com/ios-glyphs/48/000000/github.png"/>
            </a></td>
            <td><a href="https://wa.me/6281239708989" target="_blank">
                <img src="https://img.icons8.com/color/48/000000/whatsapp.png"/>
            </a></td>
        </tr>
    </table>
    """, unsafe_allow_html=True)

    st.write("Click the icons to open the respective channel.")
