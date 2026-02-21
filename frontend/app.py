import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Hospital Patient Management System",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
        border: none;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    .main h1 {
        color: #1a202c !important;
        text-align: center;
        padding: 25px;
        background: linear-gradient(120deg, #ffffff 0%, #f7fafc 100%);
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.15);
        margin-bottom: 10px;
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        border: 2px solid #667eea;
    }
    h2, h3 {
        color: #2d3748 !important;
        font-weight: 600 !important;
    }
    .stDataFrame {
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    div[data-testid="stSidebar"] .stSelectbox label {
        color: white;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🏥 Hospital Patient Management System")
st.markdown("---")

# ---------------------------------------
# SAFE API FUNCTION
# ---------------------------------------
def call_api(method, endpoint, data=None):
    response = None
    try:
        url = f"{API_URL}{endpoint}"

        if method == "GET":
            response = requests.get(url, timeout=10)

        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)

        elif method == "PUT":
            response = requests.put(url, json=data, timeout=10)

        elif method == "DELETE":
            response = requests.delete(url, timeout=10)

        return response

    except requests.exceptions.ConnectionError:
        st.error("❌ Backend not running. Start FastAPI.")
    except Exception as e:
        st.error(f"❌ API Error: {e}")

    return None


# ---------------------------------------
# SIDEBAR
# ---------------------------------------
with st.sidebar:
    st.markdown("""
        <div style='text-align: center; padding: 20px; margin-bottom: 20px;'>
            <h1 style='color: white; margin: 0;'>🏥</h1>
            <p style='color: white; margin: 5px 0 0 0;'>Patient Portal</p>
        </div>
    """, unsafe_allow_html=True)
    
    menu = st.selectbox(
        "📌 Navigation Menu",
        ["📋 View Patients", "➕ Add Patient", "✏ Update Patient", "🗑 Delete Patient"],
        label_visibility="visible"
    )
    
    st.markdown("---")
    
    st.markdown("""
        <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 10px; margin-top: 20px;'>
            <p style='color: white; margin: 0; font-size: 0.9em;'>
                <b>Quick Tips:</b><br><br>
                📋 View all patients<br>
                ➕ Add new records<br>
                ✏️ Update info<br>
                🗑️ Remove records
            </p>
        </div>
    """, unsafe_allow_html=True)

# ---------------------------------------
# VIEW
# ---------------------------------------
if menu == "📋 View Patients":

    st.markdown("### 👨‍⚕️ Registered Patients")
    
    # Add statistics cards
    col1, col2, col3 = st.columns(3)
    
    response = call_api("GET", "/patients")

    if response and response.status_code == 200:

        data = response.json()

        if not data:
            st.warning("⚠ No patients found in the database")
        else:
            # Display statistics
            with col1:
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                        <h2 style='color: white; margin: 0;'>{}</h2>
                        <p style='margin: 5px 0 0 0;'>Total Patients</p>
                    </div>
                """.format(len(data)), unsafe_allow_html=True)
            
            with col2:
                avg_age = sum(p.get('age', 0) for p in data) / len(data) if data else 0
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                        <h2 style='color: white; margin: 0;'>{:.1f}</h2>
                        <p style='margin: 5px 0 0 0;'>Average Age</p>
                    </div>
                """.format(avg_age), unsafe_allow_html=True)
            
            with col3:
                total_days = sum(p.get('admission_days', 0) for p in data)
                st.markdown("""
                    <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;'>
                        <h2 style='color: white; margin: 0;'>{}</h2>
                        <p style='margin: 5px 0 0 0;'>Total Admission Days</p>
                    </div>
                """.format(total_days), unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Display data table
            df = pd.DataFrame(data)
            st.dataframe(df, use_container_width=True, height=400)
            
            st.success(f"✅ Showing {len(data)} patient(s)")

    elif response:
        st.error(response.text)


# ---------------------------------------
# ADD
# ---------------------------------------
elif menu == "➕ Add Patient":

    st.markdown("### ➕ Add New Patient")
    st.markdown("""
        <div style='background: linear-gradient(135deg, #e0c3fc 0%, #8ec5fc 100%); 
        padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <p style='margin: 0; color: #2d3748; font-weight: bold;'>
                📝 Fill in the patient details below to add them to the system
            </p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**👤 Personal Information**")
        name = st.text_input("Full Name", placeholder="Enter patient's name")
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male","Female","Other"])
        phone = st.text_input("Contact Number", placeholder="e.g., 1234567890")

    with col2:
        st.markdown("**🏥 Medical Information**")
        address = st.text_input("Address", placeholder="Enter full address")
        disease = st.text_input("Disease/Condition", placeholder="Diagnosis")
        admission_days = st.number_input("Admission Days", min_value=0, max_value=365, value=0)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
    with col_btn2:
        add_button = st.button("✅ Add Patient", use_container_width=True)

    if add_button:

        if not name or not phone or not disease:
            st.error("⚠️ Please fill all required fields: Name, Phone, and Disease")

        else:
            try:
                payload = {
                    "name": name,
                    "age": int(age),
                    "gender": gender,
                    "phone": int(phone),   # ⭐ FIX: convert to int
                    "address": address,
                    "disease": disease,
                    "admission_days": int(admission_days)
                }

                response = call_api("POST","/patients",payload)

                if response and response.status_code in [200,201]:
                    st.balloons()
                    st.success(f"🎉 Patient '{name}' added successfully!")
                    st.info("↻ Refreshing page...")
                    st.rerun()
                elif response:
                    st.error(response.text)

            except ValueError:
                st.error("❌ Phone number must contain only digits")


# ---------------------------------------
# UPDATE
# ---------------------------------------
elif menu == "✏ Update Patient":

    st.markdown("### ✏️ Update Patient Information")
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); 
        padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <p style='margin: 0; color: #2d3748; font-weight: bold;'>
                🔍 Enter Patient ID and update their information
            </p>
        </div>
    """, unsafe_allow_html=True)

    patient_id = st.number_input("🆔 Patient ID", min_value=1, value=1, 
                                 help="Enter the ID of the patient you want to update")

    st.markdown("---")
    
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**👤 Personal Information**")
        name = st.text_input("Full Name", placeholder="Updated name")
        age = st.number_input("Age (years)", min_value=1, max_value=120, value=25)
        gender = st.selectbox("Gender", ["Male","Female","Other"])
        phone = st.text_input("Contact Number", placeholder="Updated phone")

    with col2:
        st.markdown("**🏥 Medical Information**")
        address = st.text_input("Address", placeholder="Updated address")
        disease = st.text_input("Disease/Condition", placeholder="Updated diagnosis")
        admission_days = st.number_input("Admission Days", min_value=0, max_value=365, value=0)
        st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("---")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
    with col_btn2:
        update_button = st.button("🚀 Update Patient", use_container_width=True)

    if update_button:

        if not name or not phone or not disease:
            st.error("⚠️ Please fill all required fields: Name, Phone, and Disease")

        else:
            try:
                payload = {
                    "name": name,
                    "age": int(age),
                    "gender": gender,
                    "phone": int(phone),   # ⭐ FIX
                    "address": address,
                    "disease": disease,
                    "admission_days": int(admission_days)
                }

                response = call_api("PUT",f"/patients/{patient_id}",payload)

                if response and response.status_code == 200:
                    st.success(f"✅ Patient ID {patient_id} updated successfully!")
                    st.info("↻ Refreshing page...")
                    st.rerun()
                elif response:
                    st.error(response.text)

            except ValueError:
                st.error("❌ Phone number must contain only digits")


# ---------------------------------------
# DELETE
# ---------------------------------------
elif menu == "🗑 Delete Patient":

    st.markdown("### 🗑️ Delete Patient Record")
    st.markdown("""
        <div style='background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%); 
        padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <p style='margin: 0; color: #2d3748; font-weight: bold;'>
                ⚠️ Warning: This action cannot be undone!
            </p>
        </div>
    """, unsafe_allow_html=True)

    patient_id = st.number_input("🆔 Patient ID to Delete", min_value=1, value=1,
                                 help="Enter the ID of the patient record to delete")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Show warning before delete
    st.warning("⚠️ You are about to permanently delete this patient record")
    
    col_btn1, col_btn2, col_btn3 = st.columns([1,1,1])
    with col_btn2:
        delete_button = st.button("🗑️ Confirm Delete", use_container_width=True, 
                                  type="primary")

    if delete_button:

        response = call_api("DELETE",f"/patients/{patient_id}")

        if response and response.status_code == 200:
            st.success(f"✅ Patient ID {patient_id} deleted successfully!")
            st.info("↻ Refreshing page...")
            st.rerun()
        elif response:
            st.error(response.text)

# ---------------------------------------
# FOOTER
# ---------------------------------------
st.markdown("---")
st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%); 
    border-radius: 10px; margin-top: 30px;'>
        <p style='color: #4a5568; margin: 0;'>
            🏥 <b>Hospital Patient Management System</b> | Built with FastAPI & Streamlit
        </p>
        <p style='color: #718096; margin: 5px 0 0 0; font-size: 0.9em;'>
            © 2026 | Secure & Efficient Patient Management
        </p>
    </div>
""", unsafe_allow_html=True)
