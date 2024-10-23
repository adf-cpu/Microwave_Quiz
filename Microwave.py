import streamlit as st
import pandas as pd
from datetime import datetime
import random
import cloudinary
import cloudinary.uploader
import os
st.markdown(
    """
    <style>
    .st-emotion-cache-1huvf7z {
        display: none; /* Hides the button */
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Hide the avatar image
st.markdown(
    """
    <style>
    ._profileImage_1yi6l_74 {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Use Streamlit's image function to show the image on the left side
col1, col2 = st.columns([1, 3])  # Create 2 columns with ratios (left narrower than right)

with col1:  # Left column
    st.image("Huawei.jpg", width=80)

cloudinary.config(
    cloud_name="drpkmvcdb",  # Replace with your Cloudinary cloud name
    api_key="421723639371647",        # Replace with your Cloudinary API key
    api_secret="AWpJzomMBrw-5DHNqujft5scUbM"   # Replace with your Cloudinary API secret
)

def upload_to_cloudinary(file_path, public_id):
    try:
        response = cloudinary.uploader.upload(
            file_path,
            resource_type="raw",
            public_id=public_id,
            overwrite=True,  # Allow overwriting
            invalidate=True,  # Invalidate cached versions on CDN
            unique_filename=False,  # Do not generate a unique filename
            use_filename=True  # Use the file's original filename
        )
        return response['secure_url']
    except cloudinary.exceptions.Error as e:
        st.error(f"Cloudinary upload failed: {str(e)}")
        return None

# Function to save results to Excel
def save_results(username, total_attempted, correct_answers, wrong_answers, total_score, time_taken, details):   
    try:
        df = pd.read_excel("quiz_results_microwave.xlsx")
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Username", "Date", "Total Attempted", "Correct Answers", "Wrong Answers", "Total Score", "Time Taken", "Details"])

    new_data = pd.DataFrame([[username, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), total_attempted, correct_answers, wrong_answers, total_score, time_taken, details]],
                            columns=["Username", "Date", "Total Attempted", "Correct Answers", "Wrong Answers", "Total Score", "Time Taken", "Details"])
    df = pd.concat([df, new_data], ignore_index=True)
    df.to_excel("quiz_results_microwave.xlsx", index=False)
       # Upload the file to Cloudinary
    uploaded_url = upload_to_cloudinary("quiz_results_microwave.xlsx", "quiz_results_microwave")
    if uploaded_url:
        st.success(f"Quiz results uploaded successfully!")
        # st.markdown(f"Access your file here: [quiz_results.xlsx]({uploaded_url})")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0
if 'answers' not in st.session_state:
    st.session_state.answers = []
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'quiz_submitted' not in st.session_state:
    st.session_state.quiz_submitted = False
if 'flattened_questions' not in st.session_state:
    st.session_state.flattened_questions = []
# List of allowed usernames
allowed_usernames = {
"Farrukh.Hussain",
"HIC_ISB_TrainingTeam_01.",
"HIC_ISB_TrainingTeam_02",
"HIC_ISB_TrainingTeam_03",
"HIC_ISB_TrainingTeam_04",
"HIC_ISB_TrainingTeam_05"
    
}
# Define your questions
microwave= {
"true_false": [
    {"question": "RTN905-2F support four IF ports.", "answer": "False"},
    {"question": "RTN905-2F have one 25G(o) & one 10G(o) ports.", "answer": "False"},
    {"question": "One RTN950A can support easily two 2+0 XPIC link separately.", "answer": "True"},
    {"question": "RTN905-2F can support ISM10 with latest version.", "answer": "False"},
    {"question": "RTN905-2F have its heights equal to '2U'.", "answer": "False"},
    {"question": "RTN950A support 12 directions/ODU.", "answer": "True"},
    {"question": "For E-Band we can also use RTN905F.", "answer": "False"},
    {"question": "RTN950A have two power supply.", "answer": "True"},
    {"question": "RTN950A doesn't support for SDB link using E-band in parallel.", "answer": "False"},
    {"question": "It is not allowed to access / login the other vendor microwave link during microwave link installation & alignment.", "answer": "True"},
    {"question": "During microwave alignment if you found interference must discuss with Huawei SE to provide proper alternate frequency channel.", "answer": "True"},
    {"question": "RTN950A can use for long-haul links using 6-7-8G freq band.", "answer": "False"},
    {"question": "RTN6900 support 24 directions/ODU.", "answer": "True"},
    {"question": "Eband is using 80GHz frequency.", "answer": "True"},
    {"question": "ISM10 have a sub if board slot where we can use two ISMsa cards.", "answer": "False"},
    {"question": "It is allowed to access / login the other vendor microwave link during microwave link installation & alignment.", "answer": "False"},
    {"question": "During the equipment verification if found any missing or damage offshore/onshore item, must inform the Huawei SE timely to avoid any delay.", "answer": "True"},
    {"question": "RTN6900 have its heights equal to '3U'.", "answer": "False"},
    {"question": "During microwave installation if found any incident, must inform the Huawei SE within 5 mins.", "answer": "True"},
    {"question": "RTN380AX is a complete outdoor microwave solution.", "answer": "True"},
    {"question": "XMC-3H ODU can support 8192QAM Modulation.", "answer": "True"},
    {"question": "ISM8 card can easily use in ISV3 mode.", "answer": "True"},
    {"question": "Operating freq of XMC-3E is 80GHz.", "answer": "False"},
    {"question": "It is necessary to do indoor & outdoor equipment labeling after Installation & link alignment.", "answer": "True"},
    {"question": "RTN950A is a complete outdoor microwave solution.", "answer": "False"},
    {"question": "XMC-5D have four IF ports.", "answer": "False"},
    {"question": "Required RSL of microwave link is mentioned on each site.", "answer": "False"},
    {"question": "The RTN980 supports two control boards.", "answer": "True"},
    {"question": "The E-Band Microwave is not Full outdoor MW.", "answer": "False"},
    {"question": "The RSL of Microwave decreases. Frequency interference is a potential Case.", "answer": "False"},
    {"question": "The Optix RTN 950 is applicable to long distance large capacity Microwave Transmission.", "answer": "False"},
    {"question": "RTN 980LI and RTN980L are Common Models for Short Distance MW access.", "answer": "False"},
    {"question": "The E-Band Microwave 0.6M antenna can be installed on top of Guyed Tower.", "answer": "False"},
    {"question": "It's not necessary to confirm service after activity completion.", "answer": "False"},
    {"question": "Any plan Change must be reviewed by Technical Team and approved by customer.", "answer": "True"},
    {"question": "MW Equipment verification should be done as per Design Document before starting installation.", "answer": "True"},
    {"question": "MW dismantling can be done without any traffic verification.", "answer": "False"},
    {"question": "Interference test from both ends need to perform before antenna alignment.", "answer": "True"},
    {"question": "Verification of site status should be done with NOC and Huawei site engineer before leaving site.", "answer": "True"},
    {"question": "Do not Clean the site and remove Useless material from site before leaving site.", "answer": "False"},
    {"question": "IF Cable must be grounded properly.", "answer": "True"},
    {"question": "ODU Grounding is not mandatory.", "answer": "False"},
    {"question": "RTN6900 Grounding is necessary in nearest grounding bus bar.", "answer": "True"},
    {"question": "RTN980 takes 5U Space in Rack.", "answer": "True"},
    {"question": "Slot 1&3 are paired slots in RTN950A.", "answer": "False"},
    {"question": "RTN6900 can support max 24x Directions.", "answer": "True"},
    {"question": "Power consumption of RTN6900 is less than RTN980.", "answer": "True"},
    {"question": "IDU/RTN900, ODU & IF grounding are Necessary on available grounding bus bar.", "answer": "True"},
    {"question": "It is necessary to take all the indoor & outdoor installation pictures after Installation & link alignment.", "answer": "True"},
    {"question": "During microwave link installation & alignment, must note the serial number of IDU, ODU, Coupler & MW Dish.", "answer": "True"}
],

    "single_choice": [
     {
        "question": "RTN905-2F supports (   ) IF ports.",
        "options": ["A) One IF port", "B) Three IF ports", "C) Five IF ports", "D) Two IF Ports"],
        "answer": "D) Two IF Ports"
    },
    {
        "question": "RTN905-2F can easily use at (   ) layers.",
        "options": ["A) Three sites dependent HUB site", "B) Access layer", "C) Aggregation layers", "D) Fiber Nodes"],
        "answer": "B) Access layer"
    },
    {
        "question": "In case of New link installation, must confirm before MW link installation (   ).",
        "options": ["A) Check the delivered equipment on site with Huawei provided link budget in detail", "B) Check security guard's uniform", "C) Check the fuel tank of Generator", "D) Check the Wapda transformer on site"],
        "answer": "A) Check the delivered equipment on site with Huawei provided link budget in detail"
    },
    {
        "question": "SDB MW link have combination of two freq bands, which are (   ).",
        "options": ["A) 23GHz & 38GHz", "B) 18GHz & 6GHz", "C) 13GHz & 80GHz", "D) 11GHz & 15GHz", "E) 6GHz & 7GHz"],
        "answer": "C) 13GHz & 80GHz"
    },
    {
        "question": "Control card CSHOF have total 10G(o) ports.",
        "options": ["A) one port", "B) Three ports", "C) Five ports", "D) Two Ports"],
        "answer": "D) Two Ports"
    },
    {
        "question": "Input voltage of RTN950A are as follow.",
        "options": ["A) –48 V DC power inputs with 20A fuse capacity", "B) –40 V DC power inputs with 10A fuse capacity", "C) –80 V DC power inputs with 40A fuse capacity", "D) –20 V DC power inputs with 20A fuse capacity"],
        "answer": "A) –48 V DC power inputs with 20A fuse capacity"
    },
    {
        "question": "No of IF ports of XMC-3E ODU is (  ).",
        "options": ["A) one port", "B) Three ports", "C) Five ports", "D) Two Ports"],
        "answer": "A) one port"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) XMC-5D ODU have two IF ports & called 1T1R", "B) XMC-5D ODU have two IF ports & called 2T2R", "C) XMC-5D ODU have Four IF ports & called 4T4R", "D) XMC-5D ODU have three IF ports & called 3T3R"],
        "answer": "B) XMC-5D ODU have two IF ports & called 2T2R"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) RTN6900 -ISM10 have 1 sub board slot used for only EBBsa", "B) RTN6900 -ISM10 have 1 sub board slot used for only ISMsa", "C) RTN6900 -ISM10 have 1 sub board slot used for only ISM8", "D) RTN6900 -ISM10 have 1 sub board slot used for ISMsa & EBBsa"],
        "answer": "D) RTN6900 -ISM10 have 1 sub board slot used for ISMsa & EBBsa"
    },
    {
        "question": "Single Polarized antennae can only used for.",
        "options": ["A) 13G_1+0 XPIC link", "B) 23G_2+0 XPIC link", "C) 1+0 link", "D) SDB Microwave link"],
        "answer": "C) 1+0 link"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) We can use 38GHz ODU with 6GHz Antennae", "B) We can use 38GHz ODU with 38GHz Antennae", "C) We can use 23GHz ODU with 8GHz Antennae", "D) We can use 13GHz ODU with 80GHz Antennae"],
        "answer": "B) We can use 38GHz ODU with 38GHz Antennae"
    },
    {
        "question": "Which MW is Full outdoor.",
        "options": ["A) RTN380", "B) RTN950A", "C) RTN950A", "D) RTN10A"],
        "answer": "A) RTN380"
    },
    {
        "question": "Which Control Board related with RTN 950A.",
        "options": ["A) CSHN", "B) CSH", "C) CSHNU", "D) CSHO"],
        "answer": "D) CSHO"
    },
    {
        "question": "Which Service Boards are related with RTN980.",
        "options": ["A) EM6X", "B) CSH", "C) CSHNA", "D) CSHNU"],
        "answer": "A) EM6X"
    },
    {
        "question": "If Critical incident found the incident must report with in () minutes.",
        "options": ["A) 60", "B) 30", "C) 15", "D) 5"],
        "answer": "D) 5"
    },
    {
        "question": "Can we download & use any Third Party Software from internet websites.",
        "options": ["A) Yes", "B) No"],
        "answer": "B) No"
    },
    {
        "question": "Which of the following statement is correct.",
        "options": ["A) Antennae with 18GHz freq can support 23GHz & 38GHz freq ODU", "B) Antennae with 18GHz freq can support 18GHz & 38GHz freq ODU", "C) Antennae with 18GHz freq can support 13GHz & 38GHz freq ODU", "D) Antennae with 18GHz freq can support only 18GHz freq ODU"],
        "answer": "C) Antennae with 18GHz freq can support 13GHz & 38GHz freq ODU"
    },
    {
        "question": "Which RTN IF boards have Dual port of IF.",
        "options": ["A) ISV3", "B) ISU2", "C) ISM6", "D) IF1A"],
        "answer": "C) ISM6"
    },
    {
        "question": "Which IF card have 10G Port.",
        "options": ["A) ISM6", "B) ISV3", "C) ISX2", "D) ISM8"],
        "answer": "D) ISM8"
    },
    {
        "question": "Which RTN900 ODU have Dual IF port.",
        "options": ["A) 13G XMC-3", "B) 23G-XMC-2", "C) 15G-XMC-3", "D) 15G-XMC5D"],
        "answer": "D) 15G-XMC5D"
    },
    {
        "question": "When installing the IF board, E1 board and EHT board, what need to use.",
        "options": ["Screw Driver", "Antistatic Wrist strap", "Label Printer"],
        "answer": "B) Antistatic Wrist strap"
    },
    {
        "question": "Default polarization of MW antenna is.",
        "options": ["A) Vertical", "B) Horizontal", "C) None of the above"],
        "answer": "A) Vertical"
    },
    {
        "question": "How many supporting rods are required for 1.8M MW Antenna.",
        "options": ["A) 1", "B) 3", "C) 2", "D) 4"],
        "answer": "C) 2"
    },
    {
        "question": "Pair slots in RTN980 are.",
        "options": ["A) 7,9", "B) 6,8", "C) 3,5", "D) 2,4"],
        "answer": "C) 3,5"
    },
    {
        "question": "ISM10 Board can be installed in.",
        "options": ["A) RTN950A", "B) RTN6900", "C) RTN980"],
        "answer": "B) RTN6900"
    },
    {
        "question": "ISMsa is sub board of.",
        "options": ["A) ISM10", "B) ISM8", "C) ISM6", "D) ISV3"],
        "answer": "A) ISM10"
    },
    {
        "question": "RTN6900 Supports which type of ODU.",
        "options": ["A) XMC-2", "B) XMC-3", "C) XMC-5D", "D) XMC-5D Pro"],
        "answer": "D) XMC-5D Pro"
    },
    {
        "question": "Running mode supported by ISM8 card.",
        "options": ["A) IS3", "B) IS8", "C) IS6", "D) All of the above"],
        "answer": "D) All of the above"
    },
    {
        "question": "How many antennas required for 1+1 XPIC Configurations.",
        "options": ["A) 2", "B) 4", "C) None of the above"],
        "answer": "A) 2"
    },
    {
        "question": "While working on Ufone network must consider the (   ).",
        "options": ["A) Huawei Engineers have allowed to access or connect with other vendor equipment", "B) Prohibit to operate/login in any other vendor equipment", "C) After completing the activity leave the site without NOC confirmation for services alarms", "D) ignore the interference coming from other Ufone's MW link"],
        "answer": "B) Prohibit to operate/login in any other vendor equipment"
    },
    {
        "question": "ODU grounding is (   ).",
        "options": ["A) Necessary", "B) Not Necessary"],
        "answer": "A) Necessary"
    },
    {
        "question": "IDU grounding is (   ).",
        "options": ["A) Necessary", "B) Not Necessary"],
        "answer": "A) Necessary"
    },
    {
        "question": "IF grounding, Nito & self bonding are (   ).",
        "options": ["A) Necessary", "B) Not Necessary"],
        "answer": "A) Necessary"
    }
        
    ],
    "multiple_choice": [
        {
        "question": "In case of New link installation, must confirm before MW link installation (   ).",
        "options": [
            "A) Check the delivered equipment on site with Huawei provided link budget",
            "B) Check the Antennae, accessories, (side strut in case of 1.2m, 1.8m or higher antennae)",
            "C) Check the delivered ODUs with required accessories",
            "D) Check the delivered IDU/RTN900 based on MR process & with required accessories",
            "E) Check power cable of IDU/RTN900, grounding cable, thimbles, IF connectors, Power Connector"
        ],
        "answer": ["A) Check the delivered equipment on site with Huawei provided link budget", "B) Check the Antennae, accessories, (side strut in case of 1.2m, 1.8m or higher antennae)", "C) Check the delivered ODUs with required accessories", "D) Check the delivered IDU/RTN900 based on MR process & with required accessories", "E) Check power cable of IDU/RTN900, grounding cable, thimbles, IF connectors, Power Connector"]
    },
    {
        "question": "Which of the following statement is correct?",
        "options": [
            "A) 1+0_XPIC link have use four ODUs(XMC-3), two coupler & two MW Dishes",
            "B) 2+0_XPIC link have use eight ODUs(XMC-3), four coupler & two MW Dishes",
            "C) 1+0_XPIC link have use one freq channel with two polarization (V+H)",
            "D) 2+0_XPIC link have use two freq channel with two polarization (V1+H1 & V2+H2)"
        ],
        "answer": ["A) 1+0_XPIC link have use four ODUs(XMC-3), two coupler & two MW Dishes", "B) 2+0_XPIC link have use eight ODUs(XMC-3), four coupler & two MW Dishes", "C) 1+0_XPIC link have use one freq channel with two polarization (V+H)", "D) 2+0_XPIC link have use two freq channel with two polarization (V1+H1 & V2+H2)"]
    },
    {
        "question": "Should consider the points (  ) before installation of MW Dish.",
        "options": [
            "A) Antenna azimuth(°)",
            "B) Antenna height(m)",
            "C) Available space on Tower for new MW Antenna Installation",
            "D) Antennae size with available space on tower"
        ],
        "answer": ["A) Antenna azimuth(°)", "B) Antenna height(m)", "C) Available space on Tower for new MW Antenna Installation", "D) Antennae size with available space on tower"]
    },
    {
        "question": "K-Band freq bands are as follow.",
        "options": [
            "A) 38GHz & 80GHz",
            "B) 10GHz & 18GHz",
            "C) 13GHz & 23GHz",
            "D) 11GHz & 15GHz",
            "E) 6GHz & 7GHz"
        ],
        "answer": ["B) 10GHz & 18GHz", "C) 13GHz & 23GHz", "D) 11GHz & 15GHz", "E) 6GHz & 7GHz"]
    },
    {
        "question": "SDB MW link have combination of two freq bands, which are (   ).",
        "options": [
            "A) 23GHz & 80GHz",
            "B) 18GHz & 80GHz",
            "C) 15GHz & 80GHz",
            "D) 11GHz & 15GHz",
            "E) 6GHz & 7GHz"
        ],
        "answer": ["A) 23GHz & 80GHz", "B) 18GHz & 80GHz", "C) 15GHz & 80GHz"]
    },
    {
        "question": "Which of the following statement is correct?",
        "options": [
            "A) RTN6900 -ISM10 have 1 sub board slot used for only EBBsa",
            "B) RTN6900 -ISM10 have 1 sub board slot used for only ISMsa",
            "C) RTN6900 -ISM10 have 1 sub board slot used for only ISM8",
            "D) RTN6900 -ISM10 have 1 sub board slot used for ISV3 & ISU2"
        ],
        "answer": ["A) RTN6900 -ISM10 have 1 sub board slot used for only EBBsa", "B) RTN6900 -ISM10 have 1 sub board slot used for only ISMsa"]
    },
    {
        "question": "Which of the following statement is correct?",
        "options": [
            "A) XMC-3E ODU have one IF port & called 1T1R",
            "B) XMC-5D ODU have two IF ports & called 2T2R",
            "C) XMC-2H ODU have one IF port & called 1T1R",
            "D) XMC-5D ODU have three IF ports & called 3T3R"
        ],
        "answer": ["A) XMC-3E ODU have one IF port & called 1T1R", "B) XMC-5D ODU have two IF ports & called 2T2R", "C) XMC-2H ODU have one IF port & called 1T1R"]
    },
    {
        "question": "During LOS-TSSR survey, must consider the (   ).",
        "options": [
            "A) LOS clearance Antennae Height & available space on Tower",
            "B) Available space for IDU in Indoor Rack or Outdoor Cabinet",
            "C) IF Cable Route & IF cable length",
            "D) Available breakers in Rectifier for new IDU"
        ],
        "answer": ["A) LOS clearance Antennae Height & available space on Tower", "B) Available space for IDU in Indoor Rack or Outdoor Cabinet", "C) IF Cable Route & IF cable length", "D) Available breakers in Rectifier for new IDU"]
    },
    {
        "question": "1+0 XPIC link have the properties as follow.",
        "options": [
            "A) 1+0 XPIC link have one freq channel",
            "B) 1+0 XPIC link have one freq channel with Four polarization (V+H)",
            "C) 1+0 XPIC link have one freq channel with eight polarization (V+H)",
            "D) 1+0 XPIC link have one freq channel with two polarization (V+H)"
        ],
        "answer": ["A) 1+0 XPIC link have one freq channel", "D) 1+0 XPIC link have one freq channel with two polarization (V+H)"]
    },
    {
        "question": "In case of sharing site with other Mobile Operator, must confirm before MW link installation (   ).",
        "options": [
            "A) Confirm the 'Ufone site ID' by using Latitude/Longitude provided in link budget.",
            "B) Confirm the 'Ufone outdoor cabinets' & IF Cable Tray",
            "C) Confirm the 'Ufone outdoor Rectifier' & IF Cable Tray",
            "D) Confirm the 'Ufone outdoor Battery Bank' & IF Cable Tray",
            "E) Confirm the 'Ufone Generator' in case of Wapda failure, need Generator back up"
        ],
        "answer": ["A) Confirm the 'Ufone site ID' by using Latitude/Longitude provided in link budget.", "B) Confirm the 'Ufone outdoor cabinets' & IF Cable Tray", "C) Confirm the 'Ufone outdoor Rectifier' & IF Cable Tray", "D) Confirm the 'Ufone outdoor Battery Bank' & IF Cable Tray", "E) Confirm the 'Ufone Generator' in case of Wapda failure, need Generator back up"]
    },
    {
        "question": "Which of the following statement is correct with respect to 'MW Antennae Installation'?",
        "options": [
            "A) Check the Proposed Antennae size in link budget with available space on tower",
            "B) Check the Antenna height(m) on proposed tower leg with required antennae azimuth (°)",
            "C) Available space in outdoor cabinet for IDU Installation",
            "D) Antenna azimuth(°)"
        ],
        "answer": ["A) Check the Proposed Antennae size in link budget with available space on tower", "B) Check the Antenna height(m) on proposed tower leg with required antennae azimuth (°)", "D) Antenna azimuth(°)"]
    },
    {
        "question": "What are the Advantages of WDT Cutover?",
        "options": [
            "A) No Manual Snapshot is required",
            "B) A Short interruption time and fast service configuration",
            "C) Onsite subcontractor’s Skill Requirement is Free"
        ],
        "answer": ["A) No Manual Snapshot is required", "B) A Short interruption time and fast service configuration", "C) Onsite subcontractor’s Skill Requirement is Free"]
    },
    {
        "question": "Which Board related with RTN 980?",
        "options": [
            "A) CSH",
            "B) ISM8",
            "C) EG4",
            "D) EM6X"
        ],
        "answer": ["B) ISM8", "C) EG4", "D) EM6X"]
    },
    {
        "question": "What are the Necessary Parameters for MW link configuration?",
        "options": [
            "A) Frequency",
            "B) Modulation",
            "C) TX Power",
            "D) ELINE/ELAN service Configuration"
        ],
        "answer": ["A) Frequency", "B) Modulation", "C) TX Power"]
    },
    {
        "question": "Patch Cord connectivity use between.",
        "options": [
            "A) RTN950A to RTN980",
            "B) 13G XMC-3 to RTN950A",
            "C) EM6X to EG4"
        ],
        "answer": ["A) RTN950A to RTN980", "C) EM6X to EG4"]
    },
    {
        "question": "Which of the following statement is correct with respect to 'IDU Installation'?",
        "options": [
            "A) Check the available space in existing outdoor cabinet for new IDU/RTN900 Installation",
            "B) Check the available free circuit breakers in existing rectifier for IDU/RTN900 power supply",
            "C) Check the available free holes in grounding bus bar for IDU/RTN900 grounding",
            "D) Check the available free holes in roxtic for IF cable routing properly",
            "E) Check the IF cable grounding bus bar in case of indoor room"
        ],
        "answer": ["A) Check the available space in existing outdoor cabinet for new IDU/RTN900 Installation", "B) Check the available free circuit breakers in existing rectifier for IDU/RTN900 power supply", "C) Check the available free holes in grounding bus bar for IDU/RTN900 grounding"]
    },
    {
        "question": "Which of the following statement is correct?",
        "options": [
            "A) XMC-2H ODU can only support Long-haul links",
            "B) XMC-3E ODU can only support Long-haul links",
            "C) RFU ODU can only support Long-haul links",
            "D) XMC-5D ODU can only support Long-haul links",
            "E) XMC-LH RFU ODU can only support Long-haul links"
        ],
        "answer": ["C) RFU ODU can only support Long-haul links", "E) XMC-LH RFU ODU can only support Long-haul links"]
    }

    ]
}
# Flatten questions for navigation
if not st.session_state.flattened_questions:
    flattened_questions = []

    for category, qs in microwave.items():
        for q in qs:
            q['type'] = category  # Set the type for each question
            flattened_questions.append(q)

    # Shuffle questions within each type
    random.shuffle(flattened_questions)

    true_false_questions = [q for q in flattened_questions if q['type'] == 'true_false']
    single_choice_questions = [q for q in flattened_questions if q['type'] == 'single_choice']
    mcq_questions = [q for q in flattened_questions if q['type'] == 'multiple_choice']

    # Combine the questions in the desired order
    all_questions = (
    true_false_questions[:15] + 
    single_choice_questions[:15] + 
    mcq_questions[:10]
)

    # Limit to the first 20 questions
    st.session_state.flattened_questions = all_questions[:40]

# Initialize answers
if len(st.session_state.answers) != len(st.session_state.flattened_questions):
    st.session_state.answers = [None] * len(st.session_state.flattened_questions)


# Login form
if not st.session_state.logged_in:
    st.header("Welcome to Huawei Quiz Portal")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")  # You might want to handle password validation separately

    if st.button("Login"):
        if username in allowed_usernames and password:  # Add password validation as needed
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.start_time = datetime.now()  # Track start time on login
            st.success("Logged in successfully!")
            st.session_state.logged_in = True
            st.experimental_set_query_params()  # Ensures the state is saved and reloaded without rerunning the entire script
              
        else:
            st.error("Please enter a valid username and password.")
else:
    st.sidebar.markdown(f"## Welcome **{st.session_state.username}** For The Quiz Of Microwave ")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.current_question = 0  # Reset current question
        st.session_state.answers = [None] * len(st.session_state.flattened_questions)  # Reset answers
        st.session_state.username = ""
        st.session_state.quiz_submitted = False  # Reset quiz submission status
        st.session_state.flattened_questions = []  # Reset questions
        st.success("You have been logged out.")
        # st.experimental_rerun()  # Refresh the page to reflect the new state

    # Quiz Page
    st.header(f"Welcome {st.session_state.username} For The Quiz Of Microwave")
    
    # Navigation buttons
    col1, col2 = st.columns(2)

    # Only show navigation buttons if the quiz hasn't been submitted
    if not st.session_state.quiz_submitted:
        if st.session_state.current_question > 0:
            with col1:
                if st.button("Previous", key="prev"):
                    st.session_state.current_question -= 1

    if st.session_state.current_question < len(st.session_state.flattened_questions) - 1:  # Show "Next" button if not on the last question
        with col2:
            if st.button("Next", key="next"):
                st.session_state.current_question += 1

    if st.session_state.current_question == len(st.session_state.flattened_questions) - 1 and not st.session_state.quiz_submitted:
        if st.button("Submit", key="submit"):
            if not st.session_state.quiz_submitted:  # Only process if not already submitted
                total_score = 0
                questions_attempted = 0
                correct_answers = 0
                wrong_answers = 0
                result_details = []

                for idx, question_detail in enumerate(st.session_state.flattened_questions):
                    user_answer = st.session_state.answers[idx]
                    if user_answer is not None:
                        questions_attempted += 1
                        
                        if question_detail["type"] == "true_false":
                            
                            score = 2
                            if user_answer == question_detail["answer"]:
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))
                        elif question_detail["type"] == "single_choice":
                            score = 2
                            if sorted(user_answer) == sorted(question_detail["answer"]):
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))
                        elif question_detail["type"] == "multiple_choice":
                            score = 4
                            if user_answer == question_detail["answer"]:
                                correct_answers += 1
                                total_score += score
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Correct"))
                            else:
                                wrong_answers += 1
                                result_details.append((question_detail["question"], user_answer, question_detail["answer"], "Wrong"))

                end_time = datetime.now()
                time_taken = end_time - st.session_state.start_time
                
                save_results(st.session_state.username, questions_attempted, correct_answers, wrong_answers, total_score, str(time_taken), str(result_details))
                st.success("Quiz submitted successfully!")
                st.session_state.quiz_submitted = True

                total_marks = 100  # Total marks for the quiz
                percentage = (total_score / total_marks) * 100
                result_message = "<h1 style='color: green;'>Congratulations! You passed the Test!</h1>" if percentage >= 70 else "<h1 style='color: red;'>Sorry You Have Failed The Test!.</h1>"

                # Display results in a card
                st.markdown("<div class='card'><h3>Quiz Results</h3>", unsafe_allow_html=True)
                st.markdown(result_message, unsafe_allow_html=True)
                st.write(f"**Total Questions Attempted:** {questions_attempted}")
                st.write(f"**Correct Answers:** {correct_answers}")
                st.write(f"**Wrong Answers:** {wrong_answers}")
                st.write(f"**Total Score:** {total_score}")
                st.write(f"**Percentage:** {percentage:.2f}%")
                st.markdown("</div>", unsafe_allow_html=True)

    # CSS for enhanced design
    st.markdown("""<style>
        .card {
            background-color: #ffcccc; /* Light background */
            border: 1px solid #ddd; /* Subtle border */
            border-radius: 8px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        .question-card {
            background-color: #ffcccc; /* Light red color for questions */
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>""", unsafe_allow_html=True)

    # Display current question if quiz is not submitted
    if not st.session_state.quiz_submitted and st.session_state.current_question < len(st.session_state.flattened_questions):
        current_question = st.session_state.flattened_questions[st.session_state.current_question]
        total_questions = 40
        question_number = st.session_state.current_question + 1 
        progress_percentage = question_number / total_questions
        st.write(f"**Question {question_number} of {total_questions}**")  # Question count
        st.progress(progress_percentage)
        
        st.markdown(f"<div class='question-card'><h4>Question {question_number}: {current_question['question']}</h4></div>", unsafe_allow_html=True)

        # Display options based on question type
        if current_question["type"] == "multiple_choice":
            st.header('Multiple Choice Questions')
            st.session_state.answers[st.session_state.current_question] =  st.multiselect("Choose Multiple Choice option:", current_question["options"], key=f"mc_{st.session_state.current_question}")
        elif current_question["type"] == "true_false":
            st.header('True False')
         
            st.session_state.answers[st.session_state.current_question] =st.radio("Choose an  option:", ["True", "False"], key=f"tf_{st.session_state.current_question}")
        elif current_question["type"] == "single_choice":
            st.header('Single Choice Questions')
           
            st.session_state.answers[st.session_state.current_question] =st.radio("Choose Single Choice options:", current_question["options"], key=f"cc_{st.session_state.current_question}")

# Add a footer
st.markdown("<footer style='text-align: center; margin-top: 20px;'>© 2024 Huawei Training Portal. All Rights Reserved.</footer>", unsafe_allow_html=True)
