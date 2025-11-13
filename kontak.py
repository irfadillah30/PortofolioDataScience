def kontak():
    import streamlit as st

    st.title("Contact Page")
    st.write("If you are interested you can contact me through the following channels:")

    st.markdown("""
    <style>
        .contact-table td {
            text-align: center;
            padding: 15px;
        }
        .contact-text {
            margin-top: 5px;
            font-weight: bold;
        }
    </style>

    <table class="contact-table">
        <tr>
            <td>
                <a href="mailto:irfadillahafninurvita@gmail.com" target="_blank">
                    <img src="https://img.icons8.com/color/64/000000/gmail.png"/>
                </a>
                <div class="contact-text">Email</div>
            </td>
            <td>
                <a href="https://www.linkedin.com/in/irfadillahafninurvita05/" target="_blank">
                    <img src="https://img.icons8.com/color/64/000000/linkedin.png"/>
                </a>
                <div class="contact-text">LinkedIn</div>
            </td>
            <td>
                <a href="https://github.com/irfadillah30/PortofolioDataScience" target="_blank">
                    <img src="https://img.icons8.com/ios-glyphs/64/000000/github.png"/>
                </a>
                <div class="contact-text">GitHub</div>
            </td>
            <td>
                <a href="https://wa.me/6282123970898" target="_blank">
                    <img src="https://img.icons8.com/color/64/000000/whatsapp.png"/>
                </a>
                <div class="contact-text">WhatsApp</div>
            </td>
        </tr>
    </table>
    """, unsafe_allow_html=True)
