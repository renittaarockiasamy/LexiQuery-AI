# **🧠 LexiQuery AI**



**LexiQuery AI is an AI-powered multi-format Document Question-Answering (Q\&A) System.**

**It enables users to upload documents (PDF, DOCX, TXT, CSV) and ask natural language questions.**

**Using Retrieval-Augmented Generation (RAG) with LangChain, Hugging Face Transformers, FAISS, and Streamlit,**

**the system retrieves the most relevant text and generates accurate, contextual answers.**



#### **🔑 Key Components**



**Data Ingestion: Uploads PDF, DOCX, TXT, or CSV files and parses them into text.**



**Text Splitting: Splits documents into manageable chunks using character-based splitting for optimal processing.**



**Embedding Generation: Creates semantic vector embeddings using Sentence-Transformers.**



**Vector Store: Stores embeddings in FAISS for fast similarity-based retrieval.**



**Question Answering: On receiving a user query, retrieves top relevant chunks and generates contextual answers using Hugging Face Transformers.**



##### **🚀 Features**



**📂 Multi-format support → Works with PDF, DOCX, TXT, and CSV files.**



**🔎 Semantic Search → Retrieves the most relevant document chunks.**



**🤖 Contextual AI Answers → Generates accurate answers using transformer-based models.**



**⚡ Efficient Retrieval → FAISS ensures scalable, fast similarity search.**



**🌐 Interactive Web App → Built with Streamlit for a user-friendly experience.**



**📝 Source Highlighting → Displays supporting excerpts for transparency.**



##### **🛠 Prerequisites**

###### 

**Python 3.10+**



**Pip / Virtual Environment (venv) for dependency management**



###### **📦 Installation**

**1. Clone the Repository**

**git clone https://github.com/your-username/LexiQuery-AI.git**

**cd LexiQuery-AI**



###### **2. Create a Virtual Environment (recommended)**

**python -m venv venv**

**source venv/bin/activate   # Mac/Linux**

**venv\\Scripts\\activate      # Windows**



###### **3. Install Dependencies**

**pip install -r requirements.txt**

###### 

###### **▶️ Usage**



**Run the Streamlit application:**



**streamlit run app.py**



###### 

###### **Steps:**



**Upload your document (PDF, DOCX, TXT, or CSV).**



**Type a question in natural language.**



**Receive an answer with supporting text from the document.**



###### **📌 Example Questions**



**For an uploaded policy document:**



**“What is the company’s policy on remote work?”**



**“Explain the leave application process.”**



**For an uploaded research paper:**



**“Summarize the main findings of this study.”**



**“What methods were used for data collection?”**



###### **📂 Project Structure**

**LexiQuery-AI/**

**│**

**├── app.py             # Main Streamlit application**

**├── requirements.txt   # List of dependencies**

**├── README.md          # Documentation**

**└── .gitignore         # Ignored files/folders for version control**



###### **🤝 Contributing**



**Contributions are welcome!**

**If you find issues or have ideas for improvement, feel free to open an issue or submit a pull request.**

###### 

###### **📜 License**



**This project is released under the MIT License.**



###### **✨ Author**



**Renitta** 

**Postgraduate Student – M.Sc. Data Science**

**Passionate about AI, NLP, and Applied Machine Learning**

