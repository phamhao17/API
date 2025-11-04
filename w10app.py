import streamlit as st
import requests

def search_artworks(query):
    url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
    params = {
        "q": query,
        "hasImages": True,
        "medium": "Paintings"
    }
    response = requests.get(url, params=params)
    return response.json().get("objectIDs", [])[:30]

def get_artwork_details(object_id):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    return requests.get(url).json()

st.set_page_config(page_title="Paintings Explorer – MET", layout="wide")
st.title("🎨 Browse Paintings from the MET")

query = st.text_input("Search for paintings:")
if query:
    ids = search_artworks(query)
    paintings = []
    for obj_id in ids:
        data = get_artwork_details(obj_id)
        img_url = data.get("primaryImageSmall") or data.get("primaryImage")
        if img_url:
            paintings.append({
                "title": data.get("title", "Unknown"),
                "artist": data.get("artistDisplayName", "Unknown"),
                "date": data.get("objectDate", "Unknown"),
                "image": img_url
            })

    # Masonry style layout: 3 cột
    cols = st.columns(3)
    for idx, p in enumerate(paintings):
        col = cols[idx % 3]
        col.image(p["image"], use_column_width=True)
        col.caption(f"{p['title']} — {p['artist']} ({p['date']})")
