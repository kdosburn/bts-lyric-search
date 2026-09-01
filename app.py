import streamlit as st
import os
import re
import nltk
import unicodedata

# Download tokenizer if not already present
nltk.download('punkt', quiet=True)

# Folder with your .txt files
TEXT_FOLDER = "texts"
files = sorted([f for f in os.listdir(TEXT_FOLDER) if f.endswith(".txt")])

# Dictionary for pretty book titles
SONG_TITLES = {
    "BTS_ARIRANG_English_01.txt": "ARIRANG (English) 01",
    "BTS_ARIRANG_English_02.txt": "ARIRANG (English) 02",
    "BTS_ARIRANG_English_03.txt": "ARIRANG (English) 03",
    "BTS_ARIRANG_English_04.txt": "ARIRANG (English) 04",
    "BTS_ARIRANG_English_05.txt": "ARIRANG (English) 05",
    "BTS_ARIRANG_English_06.txt": "ARIRANG (English) 06",
    "BTS_ARIRANG_English_07.txt": "ARIRANG (English) 07",
    "BTS_ARIRANG_English_08.txt": "ARIRANG (English) 08",
    "BTS_ARIRANG_English_09.txt": "ARIRANG (English) 09",
    "BTS_ARIRANG_English_10.txt": "ARIRANG (English) 10",
    "BTS_ARIRANG_English_11.txt": "ARIRANG (English) 11",
    "BTS_ARIRANG_English_12.txt": "ARIRANG (English) 12",
    "BTS_ARIRANG_English_13.txt": "ARIRANG (English) 13",
    "BTS_ARIRANG_English_14.txt": "ARIRANG (English) 14",
    "BTS_ARIRANG_English_15.txt": "ARIRANG (English) 15",
    "BTS_ARIRANG_Original_01.txt": "ARIRANG (Original) 01",
    "BTS_ARIRANG_Original_02.txt": "ARIRANG (Original) 02",
    "BTS_ARIRANG_Original_03.txt": "ARIRANG (Original) 03",
    "BTS_ARIRANG_Original_04.txt": "ARIRANG (Original) 04",
    "BTS_ARIRANG_Original_05.txt": "ARIRANG (Original) 05",
    "BTS_ARIRANG_Original_06.txt": "ARIRANG (Original) 06",
    "BTS_ARIRANG_Original_07.txt": "ARIRANG (Original) 07",
    "BTS_ARIRANG_Original_08.txt": "ARIRANG (Original) 08",
    "BTS_ARIRANG_Original_09.txt": "ARIRANG (Original) 09",
    "BTS_ARIRANG_Original_10.txt": "ARIRANG (Original) 10",
    "BTS_ARIRANG_Original_11.txt": "ARIRANG (Original) 11",
    "BTS_ARIRANG_Original_12.txt": "ARIRANG (Original) 12",
    "BTS_ARIRANG_Original_13.txt": "ARIRANG (Original) 13",
    "BTS_ARIRANG_Original_14.txt": "ARIRANG (Original) 14",
    "BTS_ARIRANG_Original_15.txt": "ARIRANG (Original) 15",
    "BTS_Wings_English_01.txt": "Wings (English) 01",
    "BTS_Wings_English_02.txt": "Wings (English) 02",
    "BTS_Wings_English_03.txt": "Wings (English) 03",
    "BTS_Wings_English_04.txt": "Wings (English) 04",
    "BTS_Wings_English_05.txt": "Wings (English) 05",
    "BTS_Wings_English_06.txt": "Wings (English) 06",
    "BTS_Wings_English_07.txt": "Wings (English) 07",
    "BTS_Wings_English_08.txt": "Wings (English) 08",
    "BTS_Wings_English_09.txt": "Wings (English) 09",
    "BTS_Wings_English_10.txt": "Wings (English) 10",
    "BTS_Wings_English_11.txt": "Wings (English) 11",
    "BTS_Wings_English_12.txt": "Wings (English) 12",
    "BTS_Wings_English_13.txt": "Wings (English) 13",
    "BTS_Wings_English_14.txt": "Wings (English) 14",
    "BTS_Wings_English_15.txt": "Wings (English) 15",
    "BTS_Wings_Original_01.txt": "Wings (Original) 01",
    "BTS_Wings_Original_02.txt": "Wings (Original) 02",
    "BTS_Wings_Original_03.txt": "Wings (Original) 03",
    "BTS_Wings_Original_04.txt": "Wings (Original) 04",
    "BTS_Wings_Original_05.txt": "Wings (Original) 05",
    "BTS_Wings_Original_06.txt": "Wings (Original) 06",
    "BTS_Wings_Original_07.txt": "Wings (Original) 07",
    "BTS_Wings_Original_08.txt": "Wings (Original) 08",
    "BTS_Wings_Original_09.txt": "Wings (Original) 09",
    "BTS_Wings_Original_10.txt": "Wings (Original) 10",
    "BTS_Wings_Original_11.txt": "Wings (Original) 11",
    "BTS_Wings_Original_12.txt": "Wings (Original) 12",
    "BTS_Wings_Original_13.txt": "Wings (Original) 13",
    "BTS_Wings_Original_14.txt": "Wings (Original) 14",
    "BTS_Wings_Original_15.txt": "Wings (Original) 15",

}

def normalize_text(s: str) -> str:
    """Normalize Unicode so smart quotes and dashes don't break search."""
    s = unicodedata.normalize("NFKD", s)
    s = s.replace("’", "'").replace("‘", "'")
    s = s.replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return s

def search_texts(query, window=200):
    """Search all books for query and return merged snippets with context."""
    results = []
    # Normalize query for matching
    norm_query = normalize_text(query)
    pattern = re.compile(re.escape(norm_query), re.IGNORECASE)

    for filename in files:
        with open(os.path.join(TEXT_FOLDER, filename), encoding="utf-8") as f:
            text = f.read()
            # Normalize text for consistent matching
            text = normalize_text(text)

            matches = list(pattern.finditer(text))
            if not matches:
                continue

            i = 0
            while i < len(matches):
                start_index = max(0, matches[i].start() - window)
                end_index = min(len(text), matches[i].end() + window)

                j = i + 1
                while j < len(matches) and matches[j].start() <= end_index:
                    end_index = min(len(text), matches[j].end() + window)
                    j += 1

                snippet = text[start_index:end_index].replace("\n", " ")
                results.append((filename, snippet))

                i = j

    return results

# --- Streamlit UI ---

st.title("BTS Lyric Search")
st.markdown(
    "### All credit goes to BTS and the brilliant "
    "[Army Project 529](https://www.armyproject529.com/)",
    unsafe_allow_html=False
)

# Slider for context size
context_chars = st.slider("Context characters", 20, 1000, 200, step=10)

# Search input
search = st.text_input("Enter a search term or phrase (ex: 'goddamnit, donut') and press Enter:")

# Button also triggers search
run_search = st.button("Search") or search

if run_search and search:
    results = search_texts(search, window=context_chars)
    if results:
        for fname, snippet in results:
            # Highlight search term(s)
            highlighted = re.sub(
                f"(?i)({re.escape(normalize_text(search))})",
                r"<mark>\1</mark>",
                snippet,
            )
            title = SONG_TITLES.get(fname, fname)
            st.markdown(f"**{title}:**")
            st.markdown(f"…{highlighted}…", unsafe_allow_html=True)
            st.divider()
    else:
        st.write("No matches found.")
