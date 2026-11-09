import streamlit as st
import gspread
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from google import genai
from google.genai import types
import datetime

# --- STEP 1: INITIALIZE UNIFIED CLOUD CONNECTION PIPELINES ---
@st.cache_resource
def init_unified_cloud_pipeline():
    # A. Establish Google Workspace API Scopes
    scope = [
        "https://googleapis.com",
        "https://googleapis.com",
        "https://googleapis.com"
    ]
    
    # Extract structural dictionary directly from safe Streamlit Secrets environment
    creds_dict = dict(st.secrets["gcp_service_account"])
    
    # Internal fix to clean raw newline characters within the private key safely
    if "private_key" in creds_dict:
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    
    # Initialize separate authenticated engine clients
    gspread_client = gspread.authorize(creds)
    drive_service = build("drive", "v3", credentials=creds)
    docs_service = build("docs", "v1", credentials=creds)
    
    # B. Initialize the Gemini Client
    ai_client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
    
    return gspread_client, drive_service, docs_service, ai_client

# Execute global integration initialization
try:
    gc, drive, docs, ai = init_unified_cloud_pipeline()
    st.success("☁️ Unified Pipeline Active: Google Workspace & Gemini AI Online!")
except Exception as e:
    st.error(f"Pipeline authentication matrix failed. Verify your Cloud Secrets console. Error: {e}")
    st.stop()

# --- STEP 2: USER INTERFACE DESIGN ---
st.title("Low-Code Technical Governance & AI Sandbox")
st.markdown("Operational control center managing data, reports, and simulated dialogue systems.")

# Partition the application into clear navigation modules
tab1, tab2, tab3 = st.tabs(["📊 Sheets Database Sync", "📝 Automated Docs Engine", "🤖 AI Dialogue Sandbox (D18/20)"])

# --- TAB 1: REAL-TIME SHEET MONITOR & INTAKE DB ---
with tab1:
    st.subheader("Google Sheets Live Registry Sync")
    sheet_url = st.text_input("Paste Shared Google Sheet URL:")
    
if sheet_url:
    try:
        import re
            # Safely extract the ID from the URL using regex
        match = re.search(r'/d/([a-zA-Z0-9-_]+)', sheet_url)
          if match:
               sheet_id = match.group(1)
               sheet = gc.open_by_key(sheet_id).get_worksheet(0)
               records = sheet.get_all_records()
            else:
                st.error("Invalid URL layout. Could not parse Spreadsheet ID.")
                records = []
        except Exception as e:
            st.error(f"Gspread Connection Error: {e}")
            records = []

        # Display current active database metrics grid
        if records:
            st.dataframe(records, use_container_width=True)
        else:
            st.info("Central database layer connected. The worksheet is currently empty.")
                
            # Entry input form for real-time validation tracking
            with st.form("database_append_form"):
                st.write("Log Production Metric / Placement Telemetry Entry")
                metric_id = st.text_input("Competency Code / Metric ID (e.g., NCTB-COMP-G5-CS):")
                metric_score = st.slider("Select Target Progress Score:", 0.0, 1.0, 0.85)
                submit = st.form_submit_button("Commit to Sheets DB")
                
                if submit and metric_id:
                    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    sheet.append_row([metric_id, metric_score, ts])
                    st.toast("Telemetry matrix cleanly committed to database!", icon="✅")
                    st.rerun()
        except Exception as e:
            st.error(f"Sheets connectivity gap: {e}")

# --- TAB 2: AUTOMATED DOCUMENT ASSEMBLY LINE ---
with tab2:
    st.subheader("Template-Driven Document Compilation Assembly")
    doc_title = st.text_input("Report / Technical Brief Filename:", value="D25_Evidence_Based_Policy_Brief")
    
    if st.button("Compile & Provision Document to Drive"):
        try:
            # Create a blank metadata tracking profile inside Google Drive
            meta = {'name': doc_title, 'mimeType': 'application/vnd.google-apps.document'}
            file_obj = drive.files().create(body=meta, fields='id').execute()
            doc_id = file_obj.get('id')
            
            # Formulate text body using target structural layout parameters
            body_text = f"TECHNICAL PERFORMANCE COMPLIANCE BRIEF\nCompiled: {datetime.date.today()}\nSovereign Local Systems Operation Handover Manifest.\n"
            req = [{'insertText': {'location': {'index': 1}, 'text': body_text}}]
            docs.documents().batchUpdate(documentId=doc_id, body={'requests': req}).execute()
            
            st.success("Document asset generated seamlessly!")
            st.markdown(f"🔗 [Review Generated Asset on Google Workspace](https://google.com{doc_id}/edit)")
        except Exception as e:
            st.error(f"Asset provision failure: {e}")

# --- TAB 3: GENERATIVE AI DIALOGUE SANDBOX (DELIVERABLES 18 & 20) ---
with tab3:
    st.subheader("Dialogue-Based AI Learning Simulator (Deliverable 18)")
    st.caption("Testing sandboxed instance deployment configuration metrics running on gemini-2.5-pro.")
    
    # Context prompt parameters defining strict system boundaries
    system_instruction = (
        "You are an expert dialogue-based AI tutor integrated into the Bangladesh national education ecosystem. "
        "Your task is to teach structural curriculum concepts, web/blog development, and digital literacy skills. "
        "Adhere closely to Universal Design for Learning (UDL) frameworks. Use clear, universal language appropriate "
        "for students. Keep statements short and highly actionable."
    )
    
    # Establish stateful interface message history storage
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Welcome to the sandboxed learning hub! What skill area are we testing today?"}
        ]
    
    # Visually layout complete historical conversation elements
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # Process dynamic user inputs real-time
    if user_prompt := st.chat_input("Enter your testing query (e.g., How do I structure my first blog layout?):"):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)
            
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            with st.spinner("Processing generation token stream..."):
                try:
                    # Execute API request matching technical proposal target metrics
                    response = ai.models.generate_content(
                        model='gemini-2.5-pro',
                        contents=user_prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=system_instruction,
                            temperature=0.2, # Strict, low-deterministic output control configuration
                            max_output_tokens=800,
                        )
                    )
                    ai_response = response.text
                    response_placeholder.write(ai_response)
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                except Exception as e:
                    st.error(f"AI Core response processing timeout: {e}")
