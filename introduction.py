import streamlit as st

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Alcon Innovation Chatbot",
    page_icon="🤖",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://www.linkedin.com/in/your-profile/',
        'Report a bug': "https://www.linkedin.com/in/your-profile/",
        'About': "# This is the Alcon Innovation Chatbot"
    }
)

# Create a two-column layout
col1, col2 = st.columns(2)

# Display a resized image in the first column
with col1:
    st.image("images/logo.png", width=200)  # Adjust the width as needed

# Display header and text in the second column
with col2:
    st.header("Alcon Innovation Chatbot")
    st.markdown("By Innov8 AI Team")

st.markdown("""
    <h2 style="text-align:center;">Welcome to the Alcon Innovation Chatbot!</h2>
    <p style="font-size:18px;">👋 Hi there! This chatbot is designed to help you explore innovations from different companies. It uses OpenAI's GPT-3.5 model to generate responses based on your queries and relevant information from our database.</p>
    
    <h3 style="margin-top:30px;">🚀 Quick Guide on How to Use the App:</h3>
    <ul style="font-size:16px; line-height:1.6;">
        <li>💬 Type your question in the chat input box.</li>
        <li>🔍 The chatbot will search the database for relevant information and generate a response.</li>
        <li>📄 View the response and any additional information provided by the chatbot.</li>
    </ul>
    
    <p style="font-size:18px; margin-top:20px;">💡 Feel free to <strong>reach out</strong> for help or <strong>report any bugs</strong> using the links in the menu!</p>
    
    <h3 style="margin-top:30px;">🏢 Competitors:</h3>
    <p style="font-size:18px;">The chatbot also keeps track of innovations from our competitors by scraping the most recent articles from their websites daily.</p>
""", unsafe_allow_html=True)