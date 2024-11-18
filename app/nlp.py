import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import joblib
from django.conf import settings
import os
# Download necessary NLTK resources

labels = [
            "Visual Data in NLP", "Speech & Audio in NLP", "Sentiment Analysis", "Stylistic Analysis",
            "Multimodality", "Discourse & Pragmatics", "Semantic Text Processing", "Multilinguality",
            "Paraphrasing", "Text Generation", "Linguistics & Cognitive NLP", "Linguistic Theories",
            "Information Retrieval", "Natural Language Interfaces", "Dialogue Systems & Conversational Agents",
            "Language Models", "Representation Learning", "Ethical NLP", "Psycholinguistics",
            "Responsible & Trustworthy NLP", "Text Classification", "Information Extraction & Text Mining",
            "Typology", "Syntactic Text Processing", "Machine Translation", "Question Answering",
            "Emotion Analysis", "Code-Switching", "Phonology", "Explainability & Interpretability in NLP",
            "Reasoning", "Fact & Claim Verification", "Robustness in NLP", "Text Clustering", "Low-Resource NLP",
            "Programming Languages in NLP", "Phonetics", "Speech Recognition", "Semantic Similarity",
            "Commonsense Reasoning", "Passage Retrieval", "Summarization", "Cognitive Modeling", "Polarity Analysis",
            "Textual Inference", "Cross-Lingual Transfer", "Text Error Correction", "Relation Extraction",
            "Green & Sustainable NLP", "Text Complexity", "Topic Modeling", "Numerical Reasoning", "Argument Mining",
            "Named Entity Recognition", "Code Generation", "Question Generation", "Knowledge Representation",
            "Captioning", "Syntactic Parsing", "Machine Reading Comprehension", "Event Extraction", "Opinion Mining",
            "Tagging", "Structured Data in NLP", "Morphology", "Term Extraction", "Knowledge Graph Reasoning",
            "Indexing", "Open Information Extraction", "Coreference Resolution", "Text Segmentation",
            "Dialogue Response Generation", "Word Sense Disambiguation", "Semantic Parsing", "Intent Recognition",
            "Aspect-based Sentiment Analysis", "Semantic Search", "Data-to-Text Generation", "Text Normalization",
            "Chunking", "Document Retrieval", "Text Style Transfer"
        ]

class NLPModel:
    def __init__(self, vectorizer_path, model_path):  # Corrected from _init_ to __init__
        # Load the vectorizer and model
        vectorizer_path = os.path.join(settings.BASE_DIR, 'nlp_model', vectorizer_path)
        model_path = os.path.join(settings.BASE_DIR, 'nlp_model', model_path)
        self.vectorizer = joblib.load(vectorizer_path)
        self.model = joblib.load(model_path)
        self.stop_words = set(stopwords.words('english'))
        self.stemmer = SnowballStemmer('english')
        # Define your labels array here
        self.labels = labels

    def preprocess_text(self, text):
        ''' Remove unwanted characters and patterns from the text. '''
        unwanted_chars_patterns = [
            r'[!?,;:—".]',  # Remove punctuation
            r'<[^>]+>',  # Remove HTML tags
            r'http[s]?://\S+',  # Remove URLs
            r'[^\w\s]',  # Remove non-alphanumeric characters
        ]

        print("Original text:", text)
        for pattern in unwanted_chars_patterns:
            text = re.sub(pattern, '', text)
            print(f"After pattern {pattern}: {text}")
        return text

    def preprocess_and_predict(self, text):
        ''' Preprocess the text and predict labels. '''
        text = self.preprocess_text(text)
        text = text.lower()
        tokens = word_tokenize(text)
        tokens = [self.stemmer.stem(word) for word in tokens if word not in self.stop_words and word.isalpha() and len(word) >= 3]
        processed_text = ' '.join(tokens)
        vectorized_text = self.vectorizer.transform([processed_text])
        predictions = self.model.predict(vectorized_text)
        predicted_labels = [self.labels[i] for i in range(len(predictions[0])) if predictions[0][i] == 1]
        return predicted_labels

# Initialize the NLPModel instance
# model = NLPModel("vectorizer2.pkl", "multioutput_classifier2.pkl")