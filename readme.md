🏛️ Government Scheme & Scholarship Chatbot (GenAI Powered)

A smart AI-powered chatbot that helps users discover government schemes and scholarships based on their age, education, gender, and state, and allows them to ask detailed follow-up questions such as eligibility, documents, benefits, deadlines, and application steps — all within a single conversational session.

🚀 Project Overview

Navigating government schemes and scholarships is often confusing due to scattered information, eligibility complexity, and lack of clarity.
This project solves that problem by providing an interactive conversational assistant that:

Understands user profiles

Recommends relevant Central & State Government schemes

Maintains chat history per session

Answers both fact-based and explanatory questions using Generative AI

🎯 Key Features
🔹 Smart Scheme Recommendation

Takes user inputs:

Age

Education level

Gender

State

Recommends eligible government schemes & scholarships

🔹 Conversational Follow-ups (Context Aware)

Once a scheme is selected, users can ask:

📄 Documents required

🎁 Benefits

🎓 Eligibility criteria

⏳ Deadline / last date

📝 How to apply

❓ Open-ended questions (e.g., “Is payment guaranteed on time?”)

The chatbot remembers the selected scheme and answers accordingly.

🔹 Hybrid Intelligence (Rule + AI)

Rule-based logic for accurate, fixed information

Generative AI (Hugging Face) for explanations and subjective questions

Honest responses when information is uncertain

🔹 Persistent Chat Sessions

Each chat session has its own history

Previous chats are accessible from the sidebar

“New Chat” starts fresh without losing old conversations

🔹 Clean & Modern UI

Built with Streamlit

Custom CSS for cards and layout

Sidebar profile management

Chat-style interface

🧠 Tech Stack
Layer	Technology
Frontend	Streamlit
AI Model	Hugging Face (google/flan-t5-base)
Logic	Python
Environment	Python 3.10+
Config	python-dotenv
Deployment Ready	Hugging Face Spaces
📂 Project Structure
gov_scheme_chatbot/
│
├── app.py                  # Main Streamlit app
├── .env                    # Hugging Face token (not committed)
│
├── utils/
│   ├── eligibility.py      # Eligibility & recommendation logic
│   └── ai_helper.py        # Hugging Face AI integration (lazy-loaded)
│
├── styles/
│   └── style.css           # Custom UI styling
│
├── venv/                   # Virtual environment
└── README.md               # Project documentation

🔐 Environment Setup
1️⃣ Create & activate virtual environment
python -m venv venv
venv\Scripts\activate

2️⃣ Install dependencies
pip install streamlit transformers torch python-dotenv

3️⃣ Create .env file
HUGGINGFACEHUB_API_TOKEN=your_huggingface_token_here

▶️ Run the Application

⚠️ Important (Windows users)
Disable Streamlit file watcher to prevent crashes:

streamlit run app.py 
or 
streamlit run app.py --server.fileWatcherType=none

🤖 AI Integration Explained

Uses Hugging Face Transformers

Model is lazy-loaded (loads only when needed)

Ensures fast startup and stability

Uses CPU for compatibility and deployment safety