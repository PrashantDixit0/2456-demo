import streamlit as st
import lancedb

@st.cache_resource
def get_db_connection():
    import lancedb
    try:
        db = lancedb.connect("./lancedb")
        return db
    except Exception as e:
        st.error(f"Database connection failed: {str(e)}")
        return None

# Page configuration
st.set_page_config(
    page_title="2456.ai - AI Directory Search Engine",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for results limit
if 'results_limit' not in st.session_state:
    st.session_state.results_limit = 5

# Initialize session state for total results count
if 'total_results' not in st.session_state:
    st.session_state.total_results = 0

db = get_db_connection()

# Only proceed with table operations if db connection successful
if db is not None:
    try:
        table_name = "wpai_7500_tools"
        table = db.open_table(table_name)
    except Exception as e:
        st.error(f"Error opening table: {str(e)}")
        table = None

# Custom CSS remains the same as your previous version
st.markdown("""
<style>
    /* All your existing CSS styles */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1f2c;
        color: white;
        border: 1px solid #2d3139;
        border-radius: 5px;
        padding: 15px;
    }
    
    .card {
        background-color: #1a1f2c;
        border-radius: 10px;
        padding: 20px;
        margin: 10px 0;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .logo-container h3 {
        margin: 0;
    }
    
    .button-container {
        display: flex;
        gap: 10px;
        margin-top: auto;
        padding-top: 15px;
    }
    
    .custom-button {
        padding: 5px 15px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
        text-decoration: none;
        display: inline-flex;
        align-items: center;
    }
    
    .save-button {
        background-color: transparent;
        border: 1px solid #ffd700;
        color: #ffd700;
    }
    
    .subscribe-button {
        background-color: transparent;
        border: 1px solid #2ecc71;
        color: #2ecc71;
    }
    
    .tag {
        background-color: #2d3139;
        padding: 5px 10px;
        border-radius: 15px;
        margin-right: 5px;
        font-size: 12px;
        display: inline-block;
        margin-bottom: 5px;
    }
    
    .show-more-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    .stButton button {
        background-color: transparent;
        color: #ffd700;
        border: 1px solid #ffd700;
        padding: 8px 20px;
        border-radius: 20px;
        cursor: pointer;
        font-size: 14px;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        background-color: #ffd700;
        color: #1a1f2c;
    }
            
    .custom-button:hover {
        color: #ffffff;
        transition: all 0.3s ease;
    }

    .save-button:hover {
        background-color: #ffd700;
        color: #1a1f2c;
    }

    .subscribe-button:hover {
        background-color: #2ecc71;
        color: #1a1f2c;
    }
</style>
""", unsafe_allow_html=True)

# Title and logo
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.markdown("<h1 style='text-align: center; color: #ffd700;'>2456.ai</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center;'>🔍 AI Directory Search Engine</h2>", unsafe_allow_html=True)

# Search box
search = st.text_input("", placeholder="AI tool", help="Enter your search term")

def create_card(tool):
    return f"""
    <div class="card">
        <div class="logo-container">
            <h3>{tool['Title']}</h3>
         </div>
        <p>{tool['content']}</p>
        <div class="tag-container">
            {' '.join(f'<span class="tag">{tag}</span>' for tag in tool['Features'].split(","))}
        </div>
        <div class="button-container">
            <a href="https://{tool['Website']}" class="custom-button save-button">🔍 Know More</a>
            <a href="#" class="custom-button save-button">💾 Save</a>
            <a href="#" class="custom-button subscribe-button">⭐ Subscribe</a>
        </div>
    </div>
    """

# Filter tools based on search
if search and table is not None:
    # First, get total count of results for this search
    total_results = len(table.search(search).to_list())
    st.session_state.total_results = total_results
    
    # Get results based on current limit
    result = table.search(search).limit(st.session_state.results_limit).to_list()
    
    # Display tools in rows of 3
    for i in range(0, len(result), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j < len(result):
                with cols[j]:
                    st.markdown(create_card(result[i + j]), unsafe_allow_html=True)
    
    # Show more button - only if there are more results to show
    if st.session_state.total_results > st.session_state.results_limit:
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("Show More Results"):
                st.session_state.results_limit += 5
        
        # Show results counter
        st.markdown(f"""
            <div style='text-align: center; color: #666; margin-top: 10px;'>
                Showing {min(st.session_state.results_limit, st.session_state.total_results)} 
                of {st.session_state.total_results} results
            </div>
        """, unsafe_allow_html=True)

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)