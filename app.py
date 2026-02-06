import streamlit as st
from PIL import Image
import base64
import io

# ========= PARAMS LOGIN =========
# Ici tu changes les noms d'utilisateurs et le mot de passe
VALID_USERS = {
    "Miguel": "030325",
    "Wendy": "030325",
}

# ========= FONCTIONS IMAGES =========
def img_to_base64(path, rotate_deg=0):
    img = Image.open(path)
    if rotate_deg != 0:
        img = img.rotate(rotate_deg, expand=True)  # rotation
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode(), img

# image3 = background, image1 = toi, image2 = copine
bg_base64, _ = img_to_base64("image1.jpeg", rotate_deg=90)
_, photo1_image   = img_to_base64("image2.jpeg")
_, photo2_image   = img_to_base64("image3.jpeg")

# ========= BACKGROUND GLOBAL =========
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: 100% auto;        /* remplit la largeur */
        background-position: center top;   /* centré horizontalement */
        background-repeat: no-repeat;
        min-height: 100vh;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.35);
        z-index: -1;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: 100% auto;
        background-position: center top;
        background-repeat: no-repeat;
        min-height: 100vh;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.55);  /* 0.55 plus sombre que 0.35 */
        z-index: -1;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ========= LOGIN MAISON =========
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "current_user" not in st.session_state:
    st.session_state.current_user = None

if not st.session_state.logged_in:
    with st.sidebar:
        st.markdown("## 🔐 Connection")
        username = st.text_input("Username", value="", placeholder="Miguel or Wendy")
        password = st.text_input("Password", type="password")

        if st.button("Connect yourself"):
            if username in VALID_USERS and VALID_USERS[username] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = username
                st.success("Connected ✅")
                st.rerun()   # <── remplace experimental_rerun par rerun
            else:
                st.error("Identifiants incorrects")

    st.stop()

# Footer de confidentialité dans la sidebar
st.markdown(
    """
    <style>
    .sidebar-footer {
        position: fixed;
        bottom: 10px;
        left: 0;
        width: 18rem;  /* ajuste si nécessaire */
        padding: 0 1rem;
        font-size: 0.75rem;
        color: #bbbbbb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-footer">
        <hr style="border-color:#444444;">
        <em>For confidentiality purpose, please do not share this website with anyone.</em>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ========= CONTENU APRÈS LOGIN =========
st.sidebar.success(f"Connecté en tant que {st.session_state.current_user}")
if st.sidebar.button("🚪 Se déconnecter"):
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.rerun()

# ========= TITRES =========
st.markdown("# 💖 WOULD YOU BE MY VALENTINE ?💖")

# ========= SESSION STATE POUR OUI/NON =========
if "oui_clique" not in st.session_state:
    st.session_state.oui_clique = False
if "compt_non" not in st.session_state:
    st.session_state.compt_non = 0

if not st.session_state.oui_clique:
    st.markdown("### **What do you choose:**")
    col1, col2 = st.columns(2, gap="large")

    with col1:
        if st.button("😢 **No**", use_container_width=True, type="secondary"):
            st.session_state.compt_non += 1
            st.balloons()
            st.rerun()

    with col2:
        if st.button("😍 **Yes !** 💕", use_container_width=True):
            st.session_state.oui_clique = True
            st.session_state.compt_non = 0
            st.rerun()

    if st.session_state.compt_non > 0:
        st.error(f"**Try again... ({st.session_state.compt_non} fois) 😏**")

else:
    st.markdown("## 🎊 **I'M THE HAPPIEST R.A IN THE WORLD !** 🎊")
    st.balloons()
    st.snow()
    st.markdown("**You are My Valentine for Life ❤️💍**")

    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.image(photo1_image, width=350, caption="Miguel ❤️")
    with col_p2:
        st.image(photo2_image, width=350, caption="Wendy 💖")

    if st.button("🔄 Recommencer ?"):
        st.session_state.oui_clique = False
        st.session_state.compt_non = 0
        st.rerun()
