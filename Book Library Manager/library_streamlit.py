import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import base64

# Set up page config
st.set_page_config(page_title="📚 Personal Library Manager", layout="wide")

st.markdown("""
    <style>
    .title-box {
        background-color: #153D1A; /* Deep greenish-black background */
        color: #F5F5DC; /* Beige text */
        padding: 20px;
        text-align: center;
        border-radius: 12px;
        font-size: 40px;
        font-family: 'Courier New', monospace;
        font-weight: bold;
        border: 3px solid #FFD700;
        box-shadow: 0px 0px 15px rgba(255, 215, 0, 0.5);
        width: 80%;
        margin: auto;
    }
    .subtitle {
        font-size: 20px;
        font-weight: normal;
        text-shadow: 2px 2px 8px rgba(255, 215, 0, 0.8);
    }
    </style>
    <div class="title-box">
        📚 Eterna Library <br>
        <span class="subtitle">Your timeless personal books collection</span>
    </div>
""", unsafe_allow_html=True)



# 🌟 Apply Custom CSS for Sidebar and Buttons
custom_css = """
<style>
/* Sidebar Customization */
/* Input Field Label Styling */
.stTextInput label, .stNumberInput label, .stSelectbox label {
    color: #FFB07C !important; /* Change this to any color */
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #2D5D2F, #153D1A);
    color: white;
    border-right: 3px solid #FFD700;
    padding-top: 20px;
    box-shadow: 4px 0px 10px rgba(255, 215, 0, 0.3);
}

/* Sidebar Text Styling */
[data-testid="stSidebar"] * {
    color: #FFD700 !important; /* Bright gold text for better visibility */
    font-weight: bold;
}
[data-testid="stSidebar"] h1, 

[data-testid="stSidebar"] h2,
 
[data-testid="stSidebar"] h3 {
    
    color: white;
}

/* Sidebar Radio Button Styling */
[data-testid="stSidebar"] .stRadio > div {
    gap: 14px;
}

[data-testid="stSidebar"] .stRadio label {
    font-size: 17px;
    font-weight: bold;
    color: #FFD700 !important;
    transition: all 0.3s ease-in-out;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
    display: flex;
    align-items: center;
    gap: 12px;
    cursor: pointer;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label span {
    width: 18px;
    height: 18px;
    border-radius: 50%;
    border: 2px solid #FFD700;
    display: inline-block;
    transition: 0.3s ease-in-out;
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label:hover span {
    background-color: #FFD700;
    box-shadow: 0 0 10px rgba(255, 215, 0, 0.7);
}

[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label[aria-checked="true"] span {
    background-color: #FFD700;
    border: 2px solid white;
    box-shadow: 0 0 12px rgba(255, 215, 0, 1);
}

/* Sidebar Navigation Buttons */
[data-testid="stSidebarNav"] button {
    background: rgba(255, 215, 0, 0.15);
    color: white !important;
    border-radius: 10px;
    padding: 12px;
    font-size: 15px;
    transition: all 0.3s ease-in-out;
    border: 1px solid #FFD700;
}

[data-testid="stSidebarNav"] button:hover {
    background: rgba(255, 215, 0, 0.3);
    transform: scale(1.08);
    box-shadow: 0px 4px 10px rgba(255, 215, 0, 0.5);
}

/* Main Page Text Styling */
body, [data-testid="stAppViewContainer"] {
    color: #FFD700 !important; /* Match text color with sidebar */
}

/* Main Page Buttons */
.stButton>button {
    background: linear-gradient(90deg, #ffbb00, #ff8000);
    color: white;
    font-size: 17px;
    border: none;
    padding: 12px 24px;
    border-radius: 10px;
    transition: all 0.3s ease-in-out;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 1px;
    box-shadow: 0px 4px 10px rgba(255, 136, 0, 0.5);
}

.stButton>button:hover {
    background: linear-gradient(90deg, #ff8000, #ffbb00);
    transform: translateY(-4px);
    box-shadow: 0px 6px 12px rgba(255, 136, 0, 0.7);
}

/* Improve Table Styling */
[data-testid="stDataFrameContainer"] {
    border-radius: 10px;
    overflow: hidden;
    border: 2px solid #FFD700;
    box-shadow: 0px 4px 10px rgba(255, 215, 0, 0.3);
}
</style>
"""  


st.markdown(custom_css, unsafe_allow_html=True)

# Function to set Background Image
def set_background(image_file):
    """Set background image if the file exists."""
    if os.path.exists(image_file):
        with open(image_file, "rb") as img_file:
            encoded_string = base64.b64encode(img_file.read()).decode()
        bg_image = f'''
        <style>
        [data-testid="stAppViewContainer"] {{
            background-image: url("data:image/jpeg;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        '''
        st.markdown(bg_image, unsafe_allow_html=True)

# Apply background image if available
set_background("background.jpg")

# Sidebar Navigation
st.sidebar.title("📚 Library Manager")
menu = st.sidebar.radio(" 📌 Select a Section", ["Add Book", "View Books", "Search", "Statistics", "Settings"])

# Load or Initialize Books Database
DATA_FILE = "books.json"


def load_books():
    """Load books from books.json"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []  # Agar file corrupt hai to empty list return kare
    return []

# Call the function to load books
books = load_books()
print(books)  # Debugging ke liye books print karo

def save_books(books):
    """Save books to JSON file."""
    with open(DATA_FILE, "w") as file:
        json.dump(books, file, indent=4)

def delete_book(book_title):
    """Remove a book from the list by title"""
    books = st.session_state["books"]
    books = [b for b in books if b["title"] != book_title]
    st.session_state["books"] = books
    save_books(books)
    st.success(f"❌ '{book_title}' deleted successfully!")

# Initialize books in session state
if "books" not in st.session_state:
    st.session_state["books"] = load_books()

books = st.session_state["books"]

# 📌 Add Book Page
if menu == "Add Book":
    st.title("📖 Add a New Book")
    
    book_title = st.text_input("Book Title", placeholder="Enter the book title here...")
    author = st.text_input("Author",  placeholder="Enter the author's name...")
    publication_year = st.number_input("Publication Year", min_value=1000, max_value=2025, value=2023)
    genre = st.text_input("Genre",  placeholder="Enter the book genre (e.g., Fiction, Sci-Fi)...")
    read_status = st.selectbox("Reading Status", ["Wishlist", "Reading", "Completed"])
    progress = st.slider("Reading Progress", 0, 100, 0) if read_status == "Reading" else (100 if read_status == "Completed" else 0)

    if st.button("📥 Add Book"):
        if book_title and author and genre:
            new_book = {
                "title": book_title,
                "author": author,
                "year": publication_year,
                "genre": genre,
                "status": read_status,
                "progress": progress
            }
            st.session_state["books"].append(new_book)
            save_books(st.session_state["books"])
            st.success("✅ Book Added Successfully!")
            
            
        else:
            st.warning("⚠️ Please fill in all required fields!")
    

# 📖 View Books Page
elif menu == "View Books":
    st.title("📚 Your Book Collection")
    
    if books:
        df = pd.DataFrame(books)
        st.dataframe(df)
        
     # Delete Book Option
        book_to_delete = st.selectbox("🗑️ Select a Book to Delete", [b["title"] for b in books])
        if st.button("❌ Delete Book"):
            delete_book(book_to_delete)
            st.rerun()  # Refresh page after deletion
        
    else:
        st.info("📂 No books added yet!")

# 🔍 Search & Filters Page
elif menu == "Search":
    st.title("🔎 Search Books")
    search_query = st.text_input("Search by Title, Author, or Genre")

    if search_query:
        filtered_books = [b for b in books if search_query.lower() in b['title'].lower() or search_query.lower() in b['author'].lower() or search_query.lower() in b['genre'].lower()]
        if filtered_books:
            st.write(pd.DataFrame(filtered_books))
        else:
            st.warning("❌ No books found matching your search.")
    else:
        st.info("🔍 Enter a search term above to filter books.")

# 📊 Statistics & Analytics Page
elif menu == "Statistics":
    st.title("📊 Book Analytics Dashboard")

    if books:
        df = pd.DataFrame(books)

        # Genre Distribution
        if "genre" in df.columns and not df.empty:
            fig_genre = px.pie(df, names="genre", title="Most Read Genres")
            st.plotly_chart(fig_genre)
        
        # Reading Progress
        if "status" in df.columns and not df.empty:
            fig_status = px.bar(df, x="status", title="Reading Status Distribution")
            st.plotly_chart(fig_status)
    else:
        st.warning("📊 No data available for analytics!")

# ⚙️ Settings Page
elif menu == "Settings":
    st.title("⚙️ Settings")
    
    # 📤 Export Books as JSON
    st.write("### 📤 Export Books (JSON)")
    st.download_button("Download Books", json.dumps(books, indent=4), "books.json", "application/json")

    # 📥 Import Books Feature
    st.write("### 📥 Import Books (JSON)")
    uploaded_file = st.file_uploader("Upload a JSON file", type="json")

    def load_uploaded_books(uploaded_file):
        """Load books from uploaded JSON file and merge with existing books."""
        try:
            new_books = json.load(uploaded_file)
            if isinstance(new_books, list):
                # Avoid duplicates before adding
                existing_titles = {b["title"] for b in books}
                books_to_add = [b for b in new_books if b["title"] not in existing_titles]

                st.session_state["books"].extend(books_to_add)
                save_books(st.session_state["books"])

                st.success(f"📚 {len(books_to_add)} new books imported successfully!")
            else:
                st.error("❌ Invalid JSON format. Please upload a list of books.")
        except Exception as e:
            st.error(f"⚠️ Error loading file: {str(e)}")

    if uploaded_file:
        load_uploaded_books(uploaded_file)
