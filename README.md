# 🍽️ Restaurant Reviews Prediction System Using NLP & Scikit-learn

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Scikit--Learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white"/>
  <img src="https://img.shields.io/badge/NLTK-154F5B?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>
</p>

<p align="center">
  A Machine Learning and NLP-based web application that analyzes restaurant reviews and predicts customer sentiment — classifying feedback as <strong>Positive</strong> or <strong>Negative</strong> using text preprocessing, feature extraction, and trained ML models.
</p>

---

## 📌 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Dataset](#-dataset)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [NLP + ML Pipeline](#-nlp--ml-pipeline)
- [Model Performance](#-model-performance)
- [Installation & Usage](#-installation--usage)
- [Screenshots](#-screenshots)
- [Author](#-author)
- [License](#-license)

---

## 🧠 Overview

Restaurant Reviews Prediction System is an end-to-end NLP + Machine Learning project that takes a customer's restaurant review as input and predicts its **sentiment — Positive ✅ or Negative ❌**.

The system preprocesses raw text (tokenization, stopword removal, stemming), converts it into numerical features using **TF-IDF / Bag of Words**, and classifies sentiment using trained ML models. Results are accessible via both a **Flask web app** and a **desktop GUI**.

---

## 🌐 Live Demo

> 🚀 **[Click here to try the app](#)** *(Add your deployment link here)*

---

## ✨ Features

- 📝 Accepts raw restaurant reviews as plain text input
- 🧹 Full NLP text preprocessing — tokenization, stopword removal, stemming
- ⚡ Instant sentiment prediction — **Positive ✅ / Negative ❌**
- 🌐 Flask-based web application interface
- 🖥️ Desktop GUI support via `gui_app.py`
- 📊 Visual results — accuracy metrics, confusion matrix, word distributions
- 💾 Model loaded from saved file — no retraining on every run

---

## 📊 Dataset

| Property | Details |
|---|---|
| **Domain** | Restaurant reviews |
| **Task** | Binary Sentiment Classification |
| **Labels** | Positive / Negative |
| **Input** | Raw customer review text |
| **Format** | CSV |

### Sample Data

| Review | Sentiment |
|---|---|
| `"Food was amazing and service was excellent."` | ✅ Positive |
| `"Very slow service and poor quality food."` | ❌ Negative |
| `"Best pasta I've ever had, will come back!"` | ✅ Positive |
| `"Rude staff and cold food. Never again."` | ❌ Negative |

---

## 📁 Project Structure

```
RestaurantReviewsPredictionSystem/
│
├── dataset/                # Raw and cleaned review datasets
├── saved_model/            # Trained ML model and vectorizer (.pkl files)
├── gui_app.py              # Desktop GUI application
├── web_app.py              # Flask web application
├── restapp.ipynb           # Jupyter Notebook — EDA, training, evaluation
├── requirements.txt        # Python dependencies
├── .gitignore
└── README.md               # Project documentation
```

---

## 🛠 Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.8+ | Core programming language |
| Pandas / NumPy | Data manipulation |
| NLTK | Text preprocessing — tokenization, stopwords, stemming |
| Scikit-learn | ML model training and evaluation |
| Matplotlib / Seaborn | Visualizations and EDA |
| Flask | Web application backend |
| PyMySQL | Database connectivity (optional) |
| Pickle | Model serialization |

---

## 🔬 NLP + ML Pipeline

```
Raw Review Text
      ↓
Text Preprocessing
  • Lowercasing
  • Remove punctuation, special characters, numbers
  • Tokenization — split into words
  • Stopword removal (NLTK stopwords)
  • Stemming — PorterStemmer
      ↓
Feature Extraction
  • Bag of Words (CountVectorizer) or TF-IDF Vectorizer
  • Vectorizer saved separately for consistent inference
      ↓
EDA
  • Sentiment class distribution
  • Most frequent words — Positive vs Negative
  • Word cloud visualization
      ↓
Model Training
  • Algorithms tested: Logistic Regression, Naive Bayes, Random Forest, SVM
  • Train/Test split: 80/20, random_state=42
      ↓
Evaluation
  • Accuracy Score
  • Precision, Recall, F1 Score
  • Confusion Matrix
      ↓
Deployment
  • Flask web app — browser-based predictions
  • Desktop GUI — standalone app
  • Loads saved model + vectorizer via pickle
  • Outputs Positive ✅ / Negative ❌ with confidence
```

---

## 📈 Model Performance

| Metric | Score |
|---|---|
| **Accuracy** | *(Add your score)* |
| **Precision** | *(Add your score)* |
| **Recall** | *(Add your score)* |
| **F1 Score** | *(Add your score)* |
| **Best Algorithm** | *(Add best model)* |

### Models Compared

| Model | Accuracy |
|---|---|
| Logistic Regression | *(Add score)* |
| Naive Bayes | *(Add score)* |
| Random Forest | *(Add score)* |
| SVM | *(Add score)* |

---

## 💻 Installation & Usage

### 1. Clone the repository
```bash
git clone https://github.com/adityabobade7900/RestaurantReviewsPredictionSystem.git
cd RestaurantReviewsPredictionSystem
```

### 2. Create and activate a virtual environment
```bash
python -m venv pyenv
.\pyenv\Scripts\activate      # Windows
source pyenv/bin/activate     # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the app

**Flask Web App:**
```bash
python web_app.py
```

**Desktop GUI:**
```bash
python gui_app.py
```

**Jupyter Notebook (training + EDA):**
```bash
jupyter notebook restapp.ipynb
```

### 5. Open in browser (Flask)
```
http://localhost:5000
```

---

## 🧪 Sample Test Cases

| Input Review | Predicted Sentiment |
|---|---|
| `"Food was amazing and service was excellent."` | ✅ Positive |
| `"Very slow service and poor quality food."` | ❌ Negative |
| `"Loved the ambience and the pasta was great!"` | ✅ Positive |
| `"Never ordering from here again. Terrible experience."` | ❌ Negative |

---

## 📸 Screenshots

> *(Add screenshots of your running app here)*
> Drag and drop your app screenshots into this section after uploading to GitHub.

- GUI Screenshot
- Web App Screenshot
- Prediction Output
- Confusion Matrix

---

## 🔮 Future Improvements

- ⭐ Multi-class sentiment (Positive / Neutral / Negative)
- 🔢 Star rating prediction from review text
- 🤖 Upgrade to Transformer-based models (BERT, DistilBERT)
- ☁️ Cloud deployment (Render / Streamlit Cloud / AWS)
- 📡 Real-time review analysis API
- 🍕 Restaurant-specific recommendation system

---

## 👨‍💻 Author

**Aditya Bobade**
Data Analyst | Python | MySQL | Power BI | Machine Learning | NLP

[![GitHub](https://img.shields.io/badge/GitHub-adityabobade7900-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/adityabobade7900)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Aditya%20Bobade-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/adityabobade7900)
[![Portfolio](https://img.shields.io/badge/Portfolio-Visit%20Here-FF5722?style=for-the-badge&logo=google-chrome&logoColor=white)](https://adityabobade7900.github.io/adityabobade/)

---

## 📞 Need Help?

| Platform | Link |
|---|---|
| 💼 LinkedIn | [linkedin.com/in/adityabobade7900](https://www.linkedin.com/in/adityabobade7900) |
| 📧 Email | [bobade1436@gmail.com](mailto:bobade1436@gmail.com) |
| 🐙 GitHub | [github.com/adityabobade7900](https://github.com/adityabobade7900) |

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use, modify and distribute.

---

> ⭐ **If you found this project helpful, please give it a star on GitHub!** ⭐
