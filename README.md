# Skincure — Personalized Skincare Recommendation System

Skincure is a Streamlit-based web application that provides personalized skincare product recommendations using semantic similarity and user preferences.

Users can select their skin type, skin concerns, preferred product category, and number of recommendations. The system then suggests the most relevant products using NLP-based embeddings.

---

## Live Demo

🔗 https://skinpro.streamlit.app

---

## Features

- Personalized skincare recommendations  
- Semantic matching using Sentence-BERT embeddings  
- Dynamic product image extraction from product URLs  
- Clean card-based UI with hover animations  
- Custom themed Streamlit interface  

---

## Tech Stack

- **Python**
- **Streamlit**
- **Sentence-Transformers (all-MiniLM-L6-v2)**
- **Scikit-learn** (cosine similarity)
- **Pandas**
- **Requests & BeautifulSoup** (image extraction)

---

## How It Works

1. Product metadata (skin type, concerns, product type) is combined into a single text field  
2. Sentence-BERT converts this text into vector embeddings  
3. User preferences are embedded using the same model  
4. Cosine similarity is used to rank products  
5. Top-N most relevant products are displayed  

---

## Project Structure

