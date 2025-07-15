from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib
import numpy as np

def train_model(dataset_path='data/cve_dataset.csv'):
    df = pd.read_csv(dataset_path)
    vectorizer = TfidfVectorizer()
    X_text = vectorizer.fit_transform(df['description'])
    X = np.hstack((X_text.toarray(), df[['cvss', 'exploitability']].values))
    y = df['priority']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier().fit(X_train, y_train)
    joblib.dump(model, 'models/prioritizer_model.pkl')
    joblib.dump(vectorizer, 'models/vectorizer.pkl')
    return model

def prioritize_findings(findings, model_path='models/prioritizer_model.pkl', vec_path='models/vectorizer.pkl'):
    model = joblib.load(model_path)
    vectorizer = joblib.load(vec_path)
    descs = [str(f) for f in findings]
    X_text = vectorizer.transform(descs)
    cvss_vals = np.array([[f.get('cvss', 0), len(str(f))] for f in findings])  # Placeholder exploitability
    X = np.hstack((X_text.toarray(), cvss_vals))
    priorities = model.predict(X)
    for i, f in enumerate(findings):
        f['priority'] = priorities[i]
    return findings
