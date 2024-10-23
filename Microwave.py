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
"HIC_ISB_TrainingTeam_01.",
"HIC_ISB_TrainingTeam_02",
"HIC_ISB_TrainingTeam_03",
"HIC_ISB_TrainingTeam_04",
"HIC_ISB_TrainingTeam_05"
    
}
# Define your questions
microwave= {
"true_false": [
    {
        "question": "RTN905-2F supports four IF ports.",
        "answer": "False"
    },
    {
        "question": "RTN905-2F has one 25G(o) & one 10G(o) port.",
        "answer": "False"
    },
    {
        "question": "RTN905-2F has a switching capacity of 60Gbs.",
        "answer": "True"
    },
    {
        "question": "RTN905-2F can support ISM10 with the latest version.",
        "answer": "False"
    },
    {
        "question": "RTN905-2F has a height equal to '2U'.",
        "answer": "False"
    },
    {
        "question": "RTN950A supports 12 directions/ODU.",
        "answer": "True"
    },
    {
        "question": "For E-Band, we can also use RTN905F.",
        "answer": "False"
    },
    {
        "question": "RTN950A can support 8192QAM Modulation.",
        "answer": "True"
    },
    {
        "question": "RTN950A doesn't support SDB link using E-band in parallel.",
        "answer": "False"
    },
    {
        "question": "RTN950A has a switching capacity of 90Gbs with control card CSHOF.",
        "answer": "True"
    },
    {
        "question": "RTN950A has a switching capacity of 10Gbs with control card CSHO.",
        "answer": "True"
    },
    {
        "question": "RTN950A can be used for long-haul links using 6-7-8G frequency bands.",
        "answer": "False"
    },
    {
        "question": "RTN950A can be used for access and aggregation layers.",
        "answer": "True"
    },
    {
        "question": "RTN6900 supports 24 directions/ODU.",
        "answer": "True"
    },
    {
        "question": "RTN6900 has a switching capacity of 200Gbs.",
        "answer": "True"
    },
    {
        "question": "ISM10 has a sub-IF board slot where we can use two EBBsa cards.",
        "answer": "False"
    },
    {
        "question": "ISM10 has a sub-IF board slot where we can use two ISMsa cards.",
        "answer": "False"
    },
    {
        "question": "RTN6900 can support 16384QAM Modulation.",
        "answer": "True"
    },
    {
        "question": "RTN6900 has two 25G and two 10G ports.",
        "answer": "True"
    },
    {
        "question": "RTN6900 has a height equal to '3U'.",
        "answer": "False"
    },
    {
        "question": "XMC-3 ODU can support long-haul links using 6-7-8GHz frequency bands.",
        "answer": "False"
    },
    {
        "question": "XMC-3 ODU can support 4096QAM Modulation.",
        "answer": "True"
    },
    {
        "question": "XMC-3H ODU can support 8192QAM Modulation.",
        "answer": "True"
    },
    {
        "question": "ISM8 card can easily be used in ISV3 mode.",
        "answer": "True"
    },
    {
        "question": "XMC-3E ODU can support channel spacing with 112MHz.",
        "answer": "True"
    },
    {
        "question": "The operating frequency of XMC-3E is 80GHz.",
        "answer": "False"
    },
    {
        "question": "The maximum TX power of XMC-5D ODU is 33 dBm/QPSK/7GHz.",
        "answer": "True"
    },
    {
        "question": "The maximum TX power of XMC-5D Pro ODU is 28 dBm/QPSK/18GHz/23GHz.",
        "answer": "True"
    },
    {
        "question": "XMC-5D has four IF ports.",
        "answer": "False"
    },
    {
        "question": "XMC-5D Pro ODU can support channel spacing with 224MHz.",
        "answer": "True"
    }
],

    "single_choice": [
     {
        "question": "RTN905-2F supports (   ) IF ports.",
        "options": ["A) one IF port", "B) Three IF ports", "C) Five IF ports", "D) Two IF Ports"],
        "answer": "D) Two IF Ports"
    },
    {
        "question": "RTN905-2F can easily be used at (   ) layers.",
        "options": ["A) Three sites dependent HUB site", "B) Access layer", "C) Aggregation layers", "D) Fiber Nodes"],
        "answer": "B) Access layer"
    },
    {
        "question": "Which of the following statements is correct supporting 'MIMO'?",
        "options": ["A) RTN905 2F & RTN950A can support MIMO", "B) RTN905 2F & RTN980L can support MIMO", "C) RTN950A & RTN950 can support MIMO", "D) RTN905 2F & RTN380AX can support MIMO"],
        "answer": "C) RTN950A & RTN950 can support MIMO"
    },
    {
        "question": "RTN6900 has a switching capacity of (    ).",
        "options": ["A) 50GBs", "B) 100GBs", "C) 200GBs", "D) 500GBs"],
        "answer": "C) 200GBs"
    },
    {
        "question": "Control card CSHOF has a total of 10G(o) ports.",
        "options": ["A) one port", "B) Three ports", "C) Five ports", "D) Two ports"],
        "answer": "D) Two ports"
    },
    {
        "question": "Input voltage of RTN950A is as follows.",
        "options": ["A) –48 V DC power inputs with 20A fuse capacity", "B) –40 V DC power inputs with 10A fuse capacity", "C) –80 V DC power inputs with 40A fuse capacity", "D) –20 V DC power inputs with 20A fuse capacity"],
        "answer": "A) –48 V DC power inputs with 20A fuse capacity"
    },
    {
        "question": "The number of IF ports of XMC-3E ODU is (  ).",
        "options": ["A) one port", "B) Three ports", "C) Five ports", "D) Two ports"],
        "answer": "A) one port"
    },
    {
        "question": "Which of the following statements is correct?",
        "options": ["A) XMC-5D ODU has two IF ports & called 1T1R", "B) XMC-5D ODU has two IF ports & called 2T2R", "C) XMC-5D ODU has four IF ports & called 4T4R", "D) XMC-5D ODU has three IF ports & called 3T3R"],
        "answer": "B) XMC-5D ODU has two IF ports & called 2T2R"
    },
    {
        "question": "Which of the following statements is correct?",
        "options": ["A) RTN6900 -ISM10 has 1 sub board slot used for only EBBsa", "B) RTN6900 -ISM10 has 1 sub board slot used for only ISMsa", "C) RTN6900 -ISM10 has 1 sub board slot used for only ISM8", "D) RTN6900 -ISM10 has 1 sub board slot used for ISMsa & EBBsa"],
        "answer": "D) RTN6900 -ISM10 has 1 sub board slot used for ISMsa & EBBsa"
    },
    {
        "question": "Which of the following statements is correct?",
        "options": ["A) Antennae with 18GHz freq can support 23GHz & 38GHz freq ODU", "B) Antennae with 18GHz freq can support 18GHz & 38GHz freq ODU", "C) Antennae with 18GHz freq can support 13GHz & 38GHz freq ODU", "D) Antennae with 18GHz freq can support only 18GHz freq ODU"],
        "answer": "D) Antennae with 18GHz freq can support only 18GHz freq ODU"
    }

        
    ],
    "multiple_choice": [
        {
        "question": "Which of the following statements is correct?",
        "options": ["A) XMC-2H ODU can only support Long-haul links", "B) XMC-3E ODU can only support Long-haul links", "C) RFU ODU can only support Long-haul links", "D) XMC-5D ODU can only support Long-haul links", "E) XMC-LH RFU ODU can only support Long-haul links"],
        "answer": ["C) RFU ODU can only support Long-haul links", "E) XMC-LH RFU ODU can only support Long-haul links"]
    },
    {
        "question": "Which of the following statements is correct?",
        "options": ["A) RTN950A support CA", "B) RTN950 support CA", "C) RTN980L support CA", "D) RTN6900 support CA"],
        "answer": ["A) RTN950A support CA", "B) RTN950 support CA", "C) RTN980L support CA", "D) RTN6900 support CA"]
    },
    {
        "question": "Which of the following statements is correct?",
        "options": ["A) RTN905 -2F support MIMO", "B) RTN950 support MIMO", "C) RTN950A support MIMO", "D) RTN910A support MIMO"],
        "answer": ["B) RTN950 support MIMO", "C) RTN950A support MIMO", "D) RTN910A support MIMO"]
    },
    {
        "question": "K-Band frequency bands are as follows.",
        "options": ["A) 38GHz & 80GHz", "B) 10GHz & 18GHz", "C) 13GHz & 23GHz", "D) 11GHz & 15GHz", "E) 6GHz & 7GHz"],
        "answer": ["B) 10GHz & 18GHz", "C) 13GHz & 23GHz", "D) 11GHz & 15GHz", "E) 6GHz & 7GHz"]
    },
    {
        "question": "SDB MW link has a combination of two frequency bands, which are (   ).",
        "options": ["A) 23GHz & 80GHz", "B) 18GHz & 80GHz", "C) 15GHz & 80GHz", "D) 11GHz & 15GHz", "E) 6GHz & 7GHz"],
        "answer": ["A) 23GHz & 80GHz", "B) 18GHz & 80GHz", "C) 15GHz & 80GHz"]
    },
    {
        "question": "Which of the following statements is correct?",
        "options": ["A) RTN6900 -ISM10 have 1 sub board slot used for only EBBsa", "B) RTN6900 -ISM10 have 1 sub board slot used for only ISMsa", "C) RTN6900 -ISM10 have 1 sub board slot used for only ISM8", "D) RTN6900 -ISM10 have 1 sub board slot used for ISV3 & ISU2"],
        "answer": ["A) RTN6900 -ISM10 have 1 sub board slot used for only EBBsa", "B) RTN6900 -ISM10 have 1 sub board slot used for only ISMsa"]
    },
    {
        "question": "Which of the following statements is correct?",
        "options": ["A) XMC-3E ODU have one IF port & called 1T1R", "B) XMC-5D ODU have two IF ports & called 2T2R", "C) XMC-2H ODU have one IF port & called 1T1R", "D) XMC-5D ODU have three IF ports & called 3T3R"],
        "answer": ["A) XMC-3E ODU have one IF port & called 1T1R", "B) XMC-5D ODU have two IF ports & called 2T2R", "C) XMC-2H ODU have one IF port & called 1T1R"]
    },
    {
        "question": "ISM8 IF card has the properties as follows.",
        "options": ["A) One port & three 10GE port for cascade", "B) Three ports & two 10GE port for cascade", "C) Two IF Ports & one 10GE port for cascade", "D) Two IF Ports"],
        "answer": ["C) Two IF Ports & one 10GE port for cascade", "D) Two IF Ports"]
    },
    {
        "question": "1+0 XPIC link has the properties as follows.",
        "options": ["A) 1+0 XPIC link has one frequency channel", "B) 1+0 XPIC link has one frequency channel with four polarization (V+H)", "C) 1+0 XPIC link has one frequency channel with eight polarization (V+H)", "D) 1+0 XPIC link has one frequency channel with two polarization (V+H)"],
        "answer": ["A) 1+0 XPIC link has one frequency channel", "D) 1+0 XPIC link has one frequency channel with two polarization (V+H)"]
    },
    {
        "question": "Which of the following statements is correct about RTN6900?",
        "options": ["A) RTN6900 support 24 ODUs", "B) RTN6900 support +1, XPIC, PLA/EPLA, AM, TDM, PWE3/MPLS, CA, SDB", "C) Switching capacity of RTN6900 is 200GBs", "D) RTN6900 support modulation is 16384QAM", "E) RTN6900 channel spacing is 224MHz"],
        "answer": ["A) RTN6900 support 24 ODUs", "B) RTN6900 support +1, XPIC, PLA/EPLA, AM, TDM, PWE3/MPLS, CA, SDB", "C) Switching capacity of RTN6900 is 200GBs", "D) RTN6900 support modulation is 16384QAM", "E) RTN6900 channel spacing is 224MHz"]
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
    single_choice_questions[:10] + 
    mcq_questions[:10]
)

    # Limit to the first 20 questions
    st.session_state.flattened_questions = all_questions[:35]

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
                            score = 3
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
        total_questions = 35
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