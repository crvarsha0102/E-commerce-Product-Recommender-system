Building an E-commerce Recommendation System with Machine Learning and Streamlit

This project outlines how to build a personalized e-commerce recommendation system using Python, Streamlit, and various machine learning techniques. The goal is to enhance the user experience on an e-commerce platform by providing tailored product suggestions, thereby increasing user engagement and sales.

Features:
Personalized Recommendations: Delivers product suggestions based on individual user preferences and behavior.
Multiple Recommendation Models: Implements and combines different recommendation approaches:
1) Content-based Filtering: Recommends items with similar attributes.
2) Collaborative Filtering: Uses user-item interaction data to find patterns and make predictions.
3) Hybrid & Multi-model Approaches: Combines the above methods for more accurate and diverse results.
Streamlit Application: Provides a user-friendly web interface for browsing products, viewing recommendations, and interacting with the system.
Scalable Architecture: Built with Python libraries like pandas, scikit-learn, and TensorFlow for efficient data processing and model training.

Technologies Used:
Streamlit: The web framework for the e-commerce application.
Python: The core programming language.
Machine Learning Libraries: pandas, numpy, scikit-learn, TensorFlow.

Getting Started:
Clone the repository:

git clone [repository-url]
cd [repository-name]
Install dependencies:

pip install -r requirements.txt
Run the Streamlit application:
streamlit run app.py

How It Works
The system is built on a simple workflow:
Data: E-commerce data (product details, user ratings, interactions) is collected and preprocessed.
Integration: The trained models are integrated into a streamlit application, which serves recommendations to users on the website.

Signup and Login Page:
<img width="1905" height="644" alt="image" src="https://github.com/user-attachments/assets/0c60ddfc-c52d-45d7-9b43-a026a70c55f3" />
Home Page showing trending Products:
<img width="1906" height="890" alt="image" src="https://github.com/user-attachments/assets/d134aaa4-bba7-437f-9ce8-17f99fc80261" />
Searching for product:
<img width="1904" height="893" alt="image" src="https://github.com/user-attachments/assets/9c1c87b3-b70b-4700-aa7b-364b7d5514e5" />
Adding Product to Cart:
<img width="1101" height="537" alt="image" src="https://github.com/user-attachments/assets/8f041b5e-2033-4839-9ddf-6237d68ccf69" />
Editing cart:
<img width="1111" height="807" alt="image" src="https://github.com/user-attachments/assets/a1084b9f-752d-4d85-b518-fbcfb7aaba26" />
Recommending products based on Search:
<img width="1064" height="793" alt="image" src="https://github.com/user-attachments/assets/c6aea724-f94c-4d27-9a56-3e93a4bbb33b" />


