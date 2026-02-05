import streamlit as st
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import requests
from bs4 import BeautifulSoup

# ----------------------------------
# Fetch image dynamically from product URL
# ----------------------------------
@st.cache_data(show_spinner=False)
def fetch_image_from_url(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")

        for prop in ["og:image", "twitter:image"]:
            tag = soup.find("meta", property=prop)
            if tag and tag.get("content"):
                return tag["content"]
        return None
    except:
        return None


# ----------------------------------
# Page config
# ----------------------------------
st.set_page_config(
    page_title="Skincare Recommendation System",
    layout="wide"
)

# ----------------------------------
# GLOBAL CSS (pink theme + FIXES)
# ----------------------------------
st.markdown("""
<style>
body, .main { background-color: #fff5f8; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #ffe4ec;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2 {
    color: #c2185b;
    font-weight: 600;
}

/* Multiselect pills */
section[data-testid="stSidebar"] span[data-baseweb="tag"] {
    background-color: #ec407a !important;
    color: white !important;
    border-radius: 8px !important;
}



/* Buttons */
.stButton > button,
button[kind="primary"] {
    background-color: #ec407a !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-size: 16px !important;
}
.stButton > button:hover {
    background-color: #d81b60 !important;
}

/* Product card */
.product-card {
    background: white;
    padding: 16px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0 6px 16px rgba(0,0,0,0.08);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}
.product-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 12px 24px rgba(236,64,122,0.25);
}

/* Image box */
.image-box {
    height: 220px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 10px;
}
.image-box img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
}
.no-img {
    height: 220px;
    background: #ffe4ec;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #c2185b;
    font-weight: 600;
}

/* View button */
.view-btn,
.view-btn:visited,
.view-btn:hover,
.view-btn:active {
    display: inline-block;
    margin-top: 12px;
    padding: 10px 16px;
    background-color: #ec407a;
    color: white !important;
    border-radius: 10px;
    text-decoration: none !important;
    font-weight: 600;
}
.view-btn:hover {
    background-color: #d81b60;
}
            


                        



</style>
""", unsafe_allow_html=True)

st.title("Personalized Skincare Recommendation System")

# ----------------------------------
# Load data
# ----------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("skinpro_with_product_type_v3.csv")
    df.fillna("", inplace=True)
    return df

df = load_data()

df["combined_text"] = (
    df["product_type"] + " " +
    df["product_type"] + " " +
    df["Skin type"] + " " +
    df["Concern"]
)

# ----------------------------------
# Model
# ----------------------------------
@st.cache_resource
def load_model():
    return SentenceTransformer("all-MiniLM-L6-v2")

model = load_model()
embeddings = model.encode(df["combined_text"].tolist(), convert_to_tensor=True)

# ----------------------------------
# Sidebar
# ----------------------------------
st.sidebar.header("Filter Preferences")

skin = st.sidebar.selectbox("Select Skin Type",
                            ["oily", "dry", "combination", "sensitive", "normal"])

concerns = st.sidebar.multiselect(
    "Select Skin Concerns",
    ["acne", "blackheads", "whiteheads", "open_pores",
     "pigmentation", "dark_under_eyes", "puffy_eyes",
     "dullness", "dryness", "oil_control",
     "anti_aging", "sun_protection"]
)

ptype = st.sidebar.selectbox(
    "Select Product Type",
    ["any"] + sorted(df["product_type"].unique())
)

top_n = st.sidebar.slider("Number of Recommendations", 5, 20, 6)

# ----------------------------------
# Recommendation logic
# ----------------------------------
def recommend(query):
    q_emb = model.encode([query], convert_to_tensor=True)
    sims = cosine_similarity(q_emb.cpu(), embeddings.cpu())[0]
    df2 = df.copy()
    df2["score"] = sims
    if ptype != "any":
        df2 = df2[df2["product_type"] == ptype]
    return df2.sort_values("score", ascending=False).head(top_n)

query = " ".join([skin] + concerns + ([] if ptype == "any" else [ptype]))

# ----------------------------------
# Results
# ----------------------------------
if st.button("Get Recommendations"):
    results = recommend(query)
    st.subheader("Recommended Products")

    cols = st.columns(3)
    for i, (_, row) in enumerate(results.iterrows()):
        img = fetch_image_from_url(row["product_url"])

        card_html = f"""
        <div class="product-card">
            <div class="image-box">
                {f"<img src='{img}'>" if img else "<div class='no-img'>Image unavailable</div>"}
            </div>
            <h4 style="color:#c2185b;">{row['Product']}</h4>
            <p><b>Type:</b> {row['product_type']}</p>
            <p><b>Skin:</b> {row['Skin type']}</p>
            <p><b>Concern:</b> {row['Concern']}</p>
            <a class="view-btn" href="{row['product_url']}" target="_blank">
                View Product
            </a>
        </div>
        """

        cols[i % 3].markdown(card_html, unsafe_allow_html=True)




