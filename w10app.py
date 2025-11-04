import streamlit as st
import requests
import pandas as pd
from functools import lru_cache

st.set_page_config(page_title="MET Art Masonry Explorer", layout="wide")

st.title("Browse Artworks from the MET (Masonry Grid Style)")

query = st.sidebar.text_input("Search keyword", value="")
has_images = st.sidebar.checkbox("Only show items with images", value=True)
if st.sidebar.button("Search"):
    with st.spinner("Searching…"):
        search_url = "https://collectionapi.metmuseum.org/public/collection/v1/search"
        params = {"q": query, "hasImages": has_images}
        resp = requests.get(search_url, params=params)
        data = resp.json()
        object_ids = data.get("objectIDs", [])[:80]  # limit e.g. to 80 items

        results = []
        for oid in object_ids:
            detail = get_object_detail(oid)
            if detail.get("primaryImageSmall"):
                results.append(detail)

        # Build HTML for masonry
        cards_html = ""
        for obj in results:
            cards_html += f"""
            <div class="masonry-item">
              <img src="{obj["primaryImageSmall"]}" alt="{obj["title"]}" />
              <div class="caption">
                <strong>{obj["title"]}</strong><br>
                {obj["artistDisplayName"]}<br>
                {obj["objectDate"]}
              </div>
            </div>
            """

        st.markdown("""
        <style>
          .masonry { 
            columns: auto 4; 
            column-gap: 1rem;
          }
          .masonry-item {
            break-inside: avoid;
            margin-bottom: 1rem;
            background: #fff;
            padding: 0.5rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
          }
          .masonry-item img {
            width: 100%;
            height: auto;
            display: block;
          }
          .caption {
            padding-top: 0.5rem;
            font-size: 0.9rem;
            color: #333;
          }
        </style>
        """, unsafe_allow_html=True)

        st.markdown(f"<div class='masonry'>{cards_html}</div>", unsafe_allow_html=True)

@st.cache_data
def get_object_detail(object_id):
    url = f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{object_id}"
    resp = requests.get(url)
    return resp.json()
