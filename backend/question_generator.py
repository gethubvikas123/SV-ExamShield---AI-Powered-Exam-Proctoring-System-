# Hybrid Question Generator with Groq AI + Pre-loaded Fallback


import os
import random
import json
import time
from typing import List, Dict
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class QuestionGenerator:
    def __init__(self):
        """Initialize with Groq API and pre-loaded question bank"""
        
        # Groq API setup
        self.groq_enabled = os.getenv('GROQ_ENABLED', 'true').lower() == 'true'
        self.groq_timeout = int(os.getenv('GROQ_TIMEOUT', 5))  # seconds
        
        if self.groq_enabled:
            try:
                api_key = os.getenv('GROQ_API_KEY')
                if api_key:
                    self.groq_client = Groq(api_key=api_key)
                    print("✅ Groq API initialized successfully")
                else:
                    print("⚠️ GROQ_API_KEY not found, using pre-loaded questions only")
                    self.groq_client = None
                    self.groq_enabled = False
            except Exception as e:
                print(f"⚠️ Failed to initialize Groq: {e}")
                self.groq_client = None
                self.groq_enabled = False
        else:
            self.groq_client = None
            print("ℹ️ Groq disabled, using pre-loaded questions only")

        
        # 120 Pre-loaded questions (10 per subject per difficulty)
        self.question_bank = {
            "Mathematics": {
                "easy": [
                    {
                        "question": "What is 15 + 28?",
                        "option_a": "42",
                        "option_b": "43",
                        "option_c": "44",
                        "option_d": "45",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is 12 × 8?",
                        "option_a": "84",
                        "option_b": "92",
                        "option_c": "96",
                        "option_d": "100",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is the square root of 64?",
                        "option_a": "6",
                        "option_b": "7",
                        "option_c": "8",
                        "option_d": "9",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is 100 ÷ 5?",
                        "option_a": "15",
                        "option_b": "20",
                        "option_c": "25",
                        "option_d": "30",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is 7 × 7?",
                        "option_a": "45",
                        "option_b": "48",
                        "option_c": "49",
                        "option_d": "50",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is 50% of 200?",
                        "option_a": "50",
                        "option_b": "75",
                        "option_c": "100",
                        "option_d": "125",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is 2³ (2 cubed)?",
                        "option_a": "6",
                        "option_b": "8",
                        "option_c": "9",
                        "option_d": "12",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is the perimeter of a square with side 5?",
                        "option_a": "15",
                        "option_b": "20",
                        "option_c": "25",
                        "option_d": "30",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is 9 + 16?",
                        "option_a": "24",
                        "option_b": "25",
                        "option_c": "26",
                        "option_d": "27",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is 144 ÷ 12?",
                        "option_a": "10",
                        "option_b": "11",
                        "option_c": "12",
                        "option_d": "13",
                        "correct_answer": "C"
                    }
                ],
                "medium": [
                    {
                        "question": "What is the slope of the line y = 2x + 3?",
                        "option_a": "1",
                        "option_b": "2",
                        "option_c": "3",
                        "option_d": "5",
                        "correct_answer": "B"
                    },
                    {
                        "question": "Solve: 3x + 5 = 20. What is x?",
                        "option_a": "3",
                        "option_b": "4",
                        "option_c": "5",
                        "option_d": "6",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is 15% of 300?",
                        "option_a": "35",
                        "option_b": "40",
                        "option_c": "45",
                        "option_d": "50",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is the area of a circle with radius 7? (Use π = 3.14)",
                        "option_a": "153.86",
                        "option_b": "149.5",
                        "option_c": "162.4",
                        "option_d": "140.2",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is the factorial of 5 (5!)?",
                        "option_a": "100",
                        "option_b": "120",
                        "option_c": "140",
                        "option_d": "150",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is log₁₀(100)?",
                        "option_a": "1",
                        "option_b": "2",
                        "option_c": "3",
                        "option_d": "10",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is the sum of angles in a triangle?",
                        "option_a": "90°",
                        "option_b": "180°",
                        "option_c": "270°",
                        "option_d": "360°",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is the value of π (pi) to 2 decimal places?",
                        "option_a": "3.12",
                        "option_b": "3.14",
                        "option_c": "3.16",
                        "option_d": "3.18",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is the Pythagorean theorem formula?",
                        "option_a": "a² + b² = c²",
                        "option_b": "a + b = c",
                        "option_c": "a² - b² = c²",
                        "option_d": "a × b = c",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is the volume of a cube with side 3?",
                        "option_a": "9",
                        "option_b": "18",
                        "option_c": "27",
                        "option_d": "36",
                        "correct_answer": "C"
                    }
                ],
                "hard": [
                    {
                        "question": "What is the derivative of x²?",
                        "option_a": "x",
                        "option_b": "2x",
                        "option_c": "x²",
                        "option_d": "2",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is the integral of 2x dx?",
                        "option_a": "x²",
                        "option_b": "x² + C",
                        "option_c": "2x²",
                        "option_d": "2x² + C",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is e (Euler's number) approximately?",
                        "option_a": "2.518",
                        "option_b": "2.618",
                        "option_c": "2.718",
                        "option_d": "2.818",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is the determinant of matrix [[1,2],[3,4]]?",
                        "option_a": "-2",
                        "option_b": "-1",
                        "option_c": "0",
                        "option_d": "1",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is lim(x→0) sin(x)/x?",
                        "option_a": "0",
                        "option_b": "1",
                        "option_c": "∞",
                        "option_d": "undefined",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is the golden ratio (φ)?",
                        "option_a": "1.518",
                        "option_b": "1.618",
                        "option_c": "1.718",
                        "option_d": "1.818",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is the eigenvalue equation?",
                        "option_a": "Av = λv",
                        "option_b": "Av = v",
                        "option_c": "Av = 0",
                        "option_d": "Av = λ",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is the Laplace transform of e^(at)?",
                        "option_a": "1/(s-a)",
                        "option_b": "1/(s+a)",
                        "option_c": "s/(s-a)",
                        "option_d": "a/(s-a)",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What does Taylor series expansion represent?",
                        "option_a": "Infinite sum of derivatives at a point",
                        "option_b": "Finite sum of values",
                        "option_c": "Product of series",
                        "option_d": "Matrix operation",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is Bayes' theorem formula?",
                        "option_a": "P(A|B) = P(B|A)P(A)/P(B)",
                        "option_b": "P(A|B) = P(A) + P(B)",
                        "option_c": "P(A|B) = P(A) × P(B)",
                        "option_d": "P(A|B) = P(B)",
                        "correct_answer": "A"
                    }
                ]
            },
            "Data Science": {
                "easy": [
                    {
                        "question": "What does CSV stand for?",
                        "option_a": "Computer Separated Values",
                        "option_b": "Comma Separated Values",
                        "option_c": "Column Separated Variables",
                        "option_d": "Common System Values",
                        "correct_answer": "B"
                    },
                    {
                        "question": "Which Python library is most commonly used for data analysis?",
                        "option_a": "NumPy",
                        "option_b": "Pandas",
                        "option_c": "Matplotlib",
                        "option_d": "TensorFlow",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is the main purpose of data visualization?",
                        "option_a": "To make data pretty",
                        "option_b": "To understand patterns and insights",
                        "option_c": "To increase file size",
                        "option_d": "To hide information",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What does SQL stand for?",
                        "option_a": "Structured Query Language",
                        "option_b": "Simple Question Language",
                        "option_c": "System Query Logic",
                        "option_d": "Standard Quality Language",
                        "correct_answer": "A"
                    },
                    {
                        "question": "Which chart is best for showing trends over time?",
                        "option_a": "Pie chart",
                        "option_b": "Bar chart",
                        "option_c": "Line chart",
                        "option_d": "Scatter plot",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is a dataset?",
                        "option_a": "A collection of data",
                        "option_b": "A type of database",
                        "option_c": "A programming language",
                        "option_d": "A visualization tool",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What does API stand for?",
                        "option_a": "Application Programming Interface",
                        "option_b": "Advanced Program Integration",
                        "option_c": "Automated Processing Interface",
                        "option_d": "Application Process Indicator",
                        "correct_answer": "A"
                    },
                    {
                        "question": "Which data type stores True or False values?",
                        "option_a": "Integer",
                        "option_b": "String",
                        "option_c": "Boolean",
                        "option_d": "Float",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is the purpose of data cleaning?",
                        "option_a": "To delete all data",
                        "option_b": "To remove errors and inconsistencies",
                        "option_c": "To encrypt data",
                        "option_d": "To compress data",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What does EDA stand for in data science?",
                        "option_a": "Electronic Data Analysis",
                        "option_b": "Exploratory Data Analysis",
                        "option_c": "Extended Data Access",
                        "option_d": "Experimental Data Algorithm",
                        "correct_answer": "B"
                    }
                ],
                "medium": [
                    {
                        "question": "What is overfitting in machine learning?",
                        "option_a": "Model performs well on training but poor on test data",
                        "option_b": "Model is too simple",
                        "option_c": "Dataset is too small",
                        "option_d": "Algorithm is too slow",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is the purpose of feature engineering?",
                        "option_a": "To delete features",
                        "option_b": "To create new meaningful features from existing data",
                        "option_c": "To visualize features",
                        "option_d": "To encrypt features",
                        "correct_answer": "B"
                    },
                    {
                        "question": "Which metric is used for classification problems?",
                        "option_a": "RMSE",
                        "option_b": "R-squared",
                        "option_c": "Accuracy",
                        "option_d": "Mean Absolute Error",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is cross-validation?",
                        "option_a": "A visualization technique",
                        "option_b": "A data cleaning method",
                        "option_c": "A technique to assess model performance",
                        "option_d": "A database query",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What does NLP stand for?",
                        "option_a": "Natural Language Processing",
                        "option_b": "Network Layer Protocol",
                        "option_c": "New Learning Process",
                        "option_d": "Numeric Linear Programming",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is normalization in data preprocessing?",
                        "option_a": "Encrypting data",
                        "option_b": "Removing duplicates",
                        "option_c":"Scaling features to a common range",
                        "option_d": "Deleting outliers",
                        "correct_answer": "C"
                    },
                    {
                        "question": "Which algorithm is used for clustering?",
                        "option_a": "Linear Regression",
                        "option_b": "K-Means",
                        "option_c": "Decision Tree",
                        "option_d": "Naive Bayes",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is a confusion matrix?",
                        "option_a": "A visualization tool", 
                        "option_b": "A type of neural network",
                        "option_c": "A data storage format",
                        "option_d":"A table showing model prediction errors",
                        "correct_answer": "D"
                    },
                    {
                        "question": "What is the difference between supervised and unsupervised learning?",
                        "option_a": "Supervised uses labeled data, unsupervised doesn't",
                        "option_b": "Unsupervised is faster",
                        "option_c": "Supervised is always better",
                        "option_d": "No difference",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is gradient descent?",
                        "option_a":  "A visualization method",
                        "option_b": "A data structure",
                        "option_c":"An optimization algorithm to minimize loss",
                        "option_d": "A database operation",
                        "correct_answer": "C"
                    }
                ],
                "hard": [
                    {
                        "question": "What is the bias-variance tradeoff?",
                        "option_a": "A type of neural network",
                        "option_b": "Balance between model complexity and generalization",
                        "option_c": "A data preprocessing technique",
                        "option_d": "A visualization method",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is regularization in machine learning?",
                        "option_a": "Technique to prevent overfitting",
                        "option_b": "Method to speed up training",
                        "option_c": "Way to visualize data",
                        "option_d": "Process to clean data",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is the vanishing gradient problem?",
                        "option_a": "Training time increases",
                        "option_b": "Data disappears during processing",
                        "option_c": "Model accuracy decreases",
                        "option_d": "Gradients become too small during backpropagation",
                        "correct_answer": "D"
                    },
                    {
                        "question": "What is ensemble learning?",
                        "option_a": "Combining multiple models for better performance",
                        "option_b": "Using one powerful model",
                        "option_c": "A data cleaning technique",
                        "option_d": "A visualization method",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is transfer learning?",
                        "option_a": "Moving data between databases",
                        "option_b": "Using pre-trained models for new tasks",
                        "option_c": "Converting file formats",
                        "option_d": "Sharing datasets",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is batch normalization used for?",
                        "option_a":"Visualizing batches",
                        "option_b": "Processing data in batches",
                        "option_c": "Cleaning datasets",
                        "option_d":  "Normalizing layer inputs in neural networks",
                        "correct_answer": "D"
                    },
                    {
                        "question": "What is the difference between precision and recall?",
                        "option_a": "Precision is always better",
                        "option_b": "No difference",
                        "option_c": "Precision measures accuracy of positive predictions, recall measures coverage",
                        "option_d": "Recall is only for regression",
                        "correct_answer": "C"
                    },
                    {
                        "question": "What is dimensionality reduction?",
                        "option_a": "Reducing number of features while preserving information",
                        "option_b": "Deleting rows from dataset",
                        "option_c": "Compressing files",
                        "option_d": "Simplifying models",
                        "correct_answer": "A"
                    },
                    {
                        "question": "What is the ROC curve used for?",
                        "option_a": "Visualizing data distribution",
                        "option_b": "Evaluating binary classifier performance",
                        "option_c": "Cleaning outliers",
                        "option_d": "Feature selection",
                        "correct_answer": "B"
                    },
                    {
                        "question": "What is attention mechanism in neural networks?",
                        "option_a": "Mechanism to focus on relevant parts of input",
                        "option_b": "A training technique",
                        "option_c": "A data structure",
                        "option_d": "An activation function",
                        "correct_answer": "A"
                    }
                ]
            },
            "Machine Learning": {
                "easy": [
                    {"question": "What is machine learning?", "option_a":  "Building hardware", "option_b":"Teaching machines to learn from data", "option_c": "Programming languages", "option_d": "Database management", "correct_answer": "B"},
                    {"question": "What is a model in ML?", "option_a": "A learned pattern from data", "option_b": "A database", "option_c": "A programming tool", "option_d": "A visualization", "correct_answer": "A"},
                    {"question": "What is training data?", "option_a": "Program code", "option_b": "Test results", "option_c": "User input", "option_d": "Data used to teach the model", "correct_answer": "D"},
                    {"question": "What is a feature in ML?", "option_a": "An error", "option_b": "An output", "option_c": "An input variable", "option_d": "A function", "correct_answer": "C"},
                    {"question": "What is a label in supervised learning?", "option_a": "The target/output variable", "option_b": "Input feature", "option_c": "Model name", "option_d": "Algorithm type", "correct_answer": "A"},
                    {"question": "What is prediction?", "option_a": "Training process", "option_b": "Model's output for new data", "option_c": "Data cleaning", "option_d": "Feature selection", "correct_answer": "B"},
                    {"question": "What is classification?", "option_a": "Categorizing data into classes", "option_b": "Predicting numbers", "option_c": "Grouping similar data", "option_d": "Cleaning data", "correct_answer": "A"},
                    {"question": "What is regression?", "option_a": "Clustering data", "option_b": "Categorizing data", "option_c": "Predicting continuous values", "option_d": "Cleaning data", "correct_answer": "C"},
                    {"question": "What is accuracy in ML?", "option_a": "Percentage of correct predictions", "option_b": "Speed of training", "option_c": "Size of dataset", "option_d": "Number of features", "correct_answer": "A"},
                    {"question": "What is a neural network?", "option_a": "A programming language", "option_b": "A database", "option_c": "A visualization tool", "option_d": "A network of interconnected nodes mimicking brain", "correct_answer": "D"}
                ],
                "medium": [
                    {"question": "What is backpropagation?", "option_a": "Feature extraction", "option_b": "Data preprocessing", "option_c": "Algorithm to train neural networks", "option_d": "Model evaluation", "correct_answer": "C"},
                    {"question": "What is a decision tree?", "option_a": "A neural network", "option_b": "A tree-like model for decision making", "option_c": "A clustering algorithm", "option_d": "A data structure only", "correct_answer": "B"},
                    {"question": "What is random forest?", "option_a": "Ensemble of decision trees", "option_b": "Single decision tree", "option_c": "Neural network", "option_d": "Clustering method", "correct_answer": "A"},
                    {"question": "What is K-fold cross validation?", "option_a": "Running K iterations", "option_b": "Training K different models", "option_c": "Using K features", "option_d": "Splitting data into K parts for validation", "correct_answer": "D"},
                    {"question": "What is SVM?", "option_a": "Support Vector Machine", "option_b": "Simple Variable Method", "option_c": "System Vector Model", "option_d": "Statistical Variance Measure", "correct_answer": "A"},
                    {"question": "What is learning rate?", "option_a": "Number of epochs", "option_b": "Speed of computer", "option_c": "Step size in gradient descent optimization", "option_d": "Accuracy metric", "correct_answer": "C"},
                    {"question": "What is an epoch in training?", "option_a": "One complete pass through entire dataset", "option_b": "One prediction", "option_c": "One feature", "option_d": "One second", "correct_answer": "A"},
                    {"question": "What is dropout?", "option_a": "Deleting data", "option_b":  "Regularization technique in neural networks", "option_c": "Removing features", "option_d": "Stopping training", "correct_answer": "C"},
                    {"question": "What is activation function?", "option_a": "Starting function", "option_b": "Function to introduce non-linearity in neural networks", "option_c": "Loss function", "option_d": "Data preprocessing function", "correct_answer": "B"},
                    {"question": "What is batch size?", "option_a": "Number of epochs", "option_b": "Total dataset size", "option_c": "Number of features", "option_d": "Number of samples processed together in one iteration", "correct_answer": "D"}
                ],
                "hard": [
                    {"question": "What is GAN?", "option_a": "Grouped Analysis Node", "option_b": "General Algorithm Network", "option_c": "Generative Adversarial Network", "option_d": "Gradient Application Network", "correct_answer": "C"},
                    {"question": "What is LSTM?", "option_a": "Long Short-Term Memory network", "option_b": "Linear System Training Model", "option_c": "Learning Standard Time Method", "option_d": "Layer System Training Machine", "correct_answer": "A"},
                    {"question": "What is Xavier initialization used for?", "option_a": "Normalizing data", "option_b": "Properly initializing neural network weights", "option_c": "Selecting features", "option_d": "Evaluating models", "correct_answer": "B"},
                    {"question": "What is the difference between L1 and L2 regularization?", "option_a": "L1 uses absolute values, L2 uses squared values", "option_b": "No difference", "option_c": "L1 is always better", "option_d": "L2 is faster", "correct_answer": "A"},
                    {"question": "What is reinforcement learning?", "option_a":  "Transfer learning", "option_b": "Supervised learning variant", "option_c": "Unsupervised learning variant", "option_d":"Learning through rewards and penalties", "correct_answer": "D"},
                    {"question": "What is Q-learning?", "option_a": "A reinforcement learning algorithm", "option_b": "A neural network type", "option_c": "A clustering method", "option_d": "A data structure", "correct_answer": "A"},
                    {"question": "What is the kernel trick in SVM?", "option_a": "Normalizing data", "option_b": "Reducing dimensions", "option_c": "Mapping data to higher dimensions implicitly", "option_d": "Cleaning data", "correct_answer": "C"},
                    {"question": "What is attention mechanism?", "option_a": "Activation function", "option_b": "Mechanism to focus on relevant input parts", "option_c": "Loss function", "option_d": "Optimization algorithm", "correct_answer": "B"},
                    {"question": "What is transformer architecture?", "option_a": "Data structure", "option_b": "Type of CNN", "option_c": "Type of RNN", "option_d": "Architecture using self-attention mechanism", "correct_answer": "D"},
                    {"question": "What is meta-learning?", "option_a": "Learning how to learn effectively", "option_b": "Transfer learning", "option_c": "Ensemble learning", "option_d": "Supervised learning", "correct_answer": "A"}
                ]
            },
            "Science": {
                "easy": [
                    {"question": "What is the chemical formula for water?", "option_a": "H₂O", "option_b": "CO₂", "option_c": "O₂", "option_d": "H₂", "correct_answer": "A"},
                    {"question": "What planet is known as the Red Planet?", "option_a": "Venus", "option_b": "Mars", "option_c": "Jupiter", "option_d": "Saturn", "correct_answer": "B"},
                    {"question": "What is the speed of light?", "option_a": "3 × 10⁸ m/s", "option_b": "3 × 10⁶ m/s", "option_c": "3 × 10⁷ m/s", "option_d": "3 × 10⁹ m/s", "correct_answer": "A"},
                    {"question": "What is photosynthesis?", "option_a": "Process plants use to make food from sunlight", "option_b": "Animal breathing process", "option_c": "Water cycle process", "option_d": "Cell division process", "correct_answer": "A"},
                    {"question": "How many bones are in the adult human body?", "option_a": "196", "option_b": "206", "option_c": "216", "option_d": "226", "correct_answer": "B"},
                    {"question": "What is the largest organ in the human body?", "option_a": "Heart", "option_b": "Brain", "option_c": "Liver", "option_d": "Skin", "correct_answer": "D"},
                    {"question": "What gas do plants absorb from the atmosphere?", "option_a": "Oxygen", "option_b": "Nitrogen", "option_c": "Carbon dioxide", "option_d": "Hydrogen", "correct_answer": "C"},
                    {"question": "What is the center of an atom called?", "option_a": "Electron", "option_b": "Proton", "option_c": "Nucleus", "option_d": "Neutron", "correct_answer": "C"},
                    {"question": "What is gravity?", "option_a": "Force that attracts objects toward each other", "option_b": "Type of energy", "option_c": "Form of matter", "option_d": "Chemical reaction", "correct_answer": "A"},
                    {"question": "What is DNA?", "option_a": "A vitamin", "option_b": "A protein", "option_c": "A cell organelle", "option_d": "Genetic material carrying hereditary information", "correct_answer": "D"}
                ],
                "medium": [
                    {"question": "What is Newton's second law of motion?", "option_a": "F = ma (Force equals mass times acceleration)", "option_b": "E = mc²", "option_c": "V = IR", "option_d": "PV = nRT", "correct_answer": "A"},
                    {"question": "What is mitosis?", "option_a": "Process of cell division", "option_b": "Cell death", "option_c": "Cell growth", "option_d": "Cell fusion", "correct_answer": "A"},
                    {"question": "What is the pH of pure water?", "option_a": "5", "option_b": "6", "option_c": "7 (neutral)", "option_d": "8", "correct_answer": "C"},
                    {"question": "What is the powerhouse of the cell?", "option_a": "Nucleus", "option_b": "Mitochondria", "option_c": "Ribosome", "option_d": "Golgi body", "correct_answer": "B"},
                    {"question": "What is Ohm's law?", "option_a": "V = IR (Voltage = Current × Resistance)", "option_b": "F = ma", "option_c": "E = mc²", "option_d": "PV = nRT", "correct_answer": "A"},
                    {"question": "What is the atomic number of carbon?", "option_a": "4", "option_b": "5", "option_c": "6", "option_d": "7", "correct_answer": "C"},
                    {"question": "What is an exothermic reaction?", "option_a": "Reaction that produces light only", "option_b": "Reaction that absorbs heat", "option_c": "Reaction with no heat change", "option_d": "Reaction that releases heat energy", "correct_answer": "D"},
                    {"question": "What is the main function of red blood cells?", "option_a": "Fight infections", "option_b": "Carry oxygen to body tissues", "option_c": "Clot blood", "option_d": "Digest food", "correct_answer": "B"},
                    {"question": "What is kinetic energy?", "option_a": "Energy of motion", "option_b": "Stored energy", "option_c": "Heat energy", "option_d": "Light energy", "correct_answer": "A"},
                    {"question": "What does the periodic table organize?", "option_a": "Forces", "option_b": "Planets", "option_c": "Cells", "option_d": "Chemical elements by atomic number", "correct_answer": "D"}
                ],
                "hard": [
                    {"question": "What is the Heisenberg uncertainty principle?", "option_a": "Entropy always increases", "option_b": "Energy is always conserved", "option_c": "Matter behaves as wave", "option_d": "Cannot simultaneously know exact position and momentum", "correct_answer": "D"},
                    {"question": "What is quantum entanglement?", "option_a": "Nuclear fusion process", "option_b": "Phenomenon where particles remain correlated", "option_c": "Type of chemical bonding", "option_d": "Atomic decay process", "correct_answer": "B"},
                    {"question": "What is the Krebs cycle?", "option_a": "Series of reactions in cellular respiration", "option_b": "DNA replication process", "option_c": "Protein synthesis pathway", "option_d": "Cell division process", "correct_answer": "A"},
                    {"question": "What is entropy in thermodynamics?", "option_a": "A force", "option_b": "Type of energy", "option_c": "Measure of disorder in a system", "option_d": "Chemical property", "correct_answer": "C"},
                    {"question": "What is a black hole?", "option_a": "Region of spacetime with extreme gravity", "option_b": "Type of star", "option_c": "A planet", "option_d": "A galaxy type", "correct_answer": "A"},
                    {"question": "What is CRISPR technology?", "option_a": "Chemical compound", "option_b": "Type of microscope", "option_c": "Gene editing tool", "option_d": "Cell organelle", "correct_answer": "C"},
                    {"question": "What is the Standard Model in physics?", "option_a": "Evolution theory", "option_b": "Cell theory", "option_c": "Atomic theory", "option_d": "Theory describing fundamental particles and forces", "correct_answer": "D"},
                    {"question": "What is dark matter?", "option_a": "Invisible matter making up most of universe mass", "option_b": "Type of energy", "option_c": "Black holes", "option_d": "Antimatter", "correct_answer": "A"},
                    {"question": "What is the Doppler effect?", "option_a": "Light refraction", "option_b": "Change in frequency due to relative motion", "option_c": "Sound absorption", "option_d": "Wave interference", "correct_answer": "B"},
                    {"question": "What is superconductivity?", "option_a": "Zero electrical resistance at low temperatures", "option_b": "Very high conductivity", "option_c": "Magnetic property", "option_d": "Chemical reaction", "correct_answer": "A"}
                ]
            }
        }
        
        print(f"✅ Pre-loaded question bank ready: {self._count_questions()} questions")
    
    def _count_questions(self):
        """Count total pre-loaded questions"""
        total = 0
        for subject in self.question_bank.values():
            for difficulty in subject.values():
                total += len(difficulty)
        return total
    
    def _normalize_question_text(self, question_text):
        return ' '.join(question_text.lower().strip().split())

    def _dedupe_questions(self, questions):
        unique = []
        seen = set()

        for q in questions:
            normalized = self._normalize_question_text(q.get('question', ''))
            if normalized and normalized not in seen:
                seen.add(normalized)
                unique.append(q)

        return unique

    def generate_questions(self, subject: str, difficulty: str, count: int = 5) -> Dict:
        """
        Generate questions using hybrid approach:
        1. Try Groq API first (if enabled and count > 10)
        2. Fallback to pre-loaded questions
        3. Mix Groq + pre-loaded for optimal results
        
        Returns: {"questions": [...], "source": "groq|pre-loaded|hybrid"}
        """
        
        count = min(count, 20)  # Max 20 questions
        
        print(f"\n🔄 Generating {count} {difficulty} questions for {subject}...")
        
        # Strategy selection
        if count <= 10:
            # Use pre-loaded for small counts (instant, reliable)
            print(f"📚 Using pre-loaded questions (count ≤ 10)")
            questions = self._get_preloaded_questions(subject, difficulty, count)
            return {"questions": questions, "source": "pre-loaded"}
        
        elif self.groq_enabled and count > 10:
            # Try Groq for larger counts (unique questions)
            print(f"🤖 Attempting Groq generation...")
            
            try:
                groq_questions = self._generate_with_groq(subject, difficulty, count)
                
                if groq_questions and len(groq_questions) >= count:
                    print(f"✅ Groq generated {len(groq_questions)} unique questions")
                    return {"questions": groq_questions[:count], "source": "groq"}
                else:
                    print(f"⚠️ Groq returned insufficient questions, using hybrid approach")
                    questions = self._hybrid_generation(subject, difficulty, count)
                    return {"questions": questions, "source": "hybrid"}
                    
            except Exception as e:
                print(f"⚠️ Groq failed: {e}, falling back to pre-loaded")
                questions = self._hybrid_generation(subject, difficulty, count)
                return {"questions": questions, "source": "hybrid"}
        
        else:
            # Groq disabled or failed, use hybrid
            print(f"📚 Using hybrid approach (Groq disabled)")
            questions = self._hybrid_generation(subject, difficulty, count)
            return {"questions": questions, "source": "hybrid"}
    
    def _generate_with_groq(self, subject: str, difficulty: str, count: int) -> List[Dict]:
        """Generate questions using Groq API with timeout"""
        
        if not self.groq_client:
            return []
        
        start_time = time.time()
        
        # Prepare prompt
        prompt = f"""Generate {count} multiple choice questions about {subject} at {difficulty} difficulty level.

STRICT FORMAT - Respond ONLY with valid JSON array, no markdown, no explanation:

[
  {{
    "question": "Question text here?",
    "option_a": "First option",
    "option_b": "Second option",
    "option_c": "Third option",
    "option_d": "Fourth option",
    "correct_answer": "A"
  }}
]

Requirements:
1. Each question must be unique and different from common textbook questions
2. Options should be plausible and well-distributed
3. Correct answer must be one of: A, B, C, or D
4. Difficulty: {difficulty} level
5. Subject: {subject}
6. Total questions: {count}
7. Return ONLY the JSON array, nothing else

Generate now:"""

        try:
            # Call Groq API with timeout
            response = self.groq_client.chat.completions.create(
                model="llama-3.1-70b-versatile",  # Fast and smart
                messages=[
                    {"role": "system", "content": "You are an expert exam question generator. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=4000,
                top_p=0.9
            )
            
            elapsed = time.time() - start_time
            print(f"⏱️ Groq response time: {elapsed:.2f}s")
            
            # Check timeout
            if elapsed > self.groq_timeout:
                print(f"⚠️ Groq exceeded timeout ({self.groq_timeout}s)")
                return []
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```"):
                content = content.split("```")[1]
                if content.startswith("json"):
                    content = content[4:]
                content = content.strip()
            
            # Parse JSON
            questions = json.loads(content)
            
            # Validate format
            validated = []
            for q in questions:
                if self._validate_question(q):
                    validated.append({
                        "question": q.get("question", ""),
                        "option_a": q.get("option_a", ""),
                        "option_b": q.get("option_b", ""),
                        "option_c": q.get("option_c", ""),
                        "option_d": q.get("option_d", ""),
                        "correct_answer": q.get("correct_answer", "A").upper(),
                        "subject": subject,
                        "difficulty": difficulty
                    })
            
            if validated:
                print(f"✅ Validated {len(validated)} Groq questions")
            
            return validated
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse Groq response as JSON: {e}")
            return []
        except Exception as e:
            print(f"❌ Groq API error: {e}")
            return []
    def _validate_question(self, q: Dict) -> bool:
        """Validate question format"""
        required_fields = ["question", "option_a", "option_b", "option_c", "option_d", "correct_answer"]
        
        # Check all fields exist and are non-empty
        for field in required_fields:
            if field not in q or not q[field] or len(str(q[field]).strip()) == 0:
                return False
        
        # Validate correct answer is A, B, C, or D
        if q["correct_answer"].upper() not in ["A", "B", "C", "D"]:
            return False
        
        return True
    
    def _get_preloaded_questions(self, subject: str, difficulty: str, count: int) -> List[Dict]:
        """Get questions from pre-loaded bank"""
        
        if subject not in self.question_bank or difficulty not in self.question_bank[subject]:
            print(f"⚠️ {subject}/{difficulty} not in pre-loaded bank")
            return []
        
        bank_questions = self.question_bank[subject][difficulty].copy()
        random.shuffle(bank_questions)
        
        selected = bank_questions[:min(count, len(bank_questions))]
        
        # Add metadata
        for q in selected:
            q['subject'] = subject
            q['difficulty'] = difficulty
        
        print(f"✅ Selected {len(selected)} pre-loaded questions")
        return selected
    
    def _hybrid_generation(self, subject: str, difficulty: str, count: int) -> List[Dict]:
        """Mix pre-loaded questions with templates"""
        
        # Get all available pre-loaded
        preloaded = self._get_preloaded_questions(subject, difficulty, 10)
        
        if len(preloaded) >= count:
            return preloaded[:count]
        
        # Need more, generate templates
        needed = count - len(preloaded)
        templates = self._generate_template_questions(subject, difficulty, needed)
        
        result = preloaded + templates
        random.shuffle(result)
        
        print(f"✅ Hybrid: {len(preloaded)} pre-loaded + {len(templates)} templates")
        return result[:count]
    
    def _generate_template_questions(self, subject: str, difficulty: str, count: int) -> List[Dict]:
        """Generate simple template-based questions"""
        
        templates = {
            "easy": [
                {
                    "question": f"What is a fundamental concept in {subject}?",
                    "option_a": "Core principle A",
                    "option_b": "Core principle B",
                    "option_c": "Core principle C",
                    "option_d": "None of the above",
                    "correct_answer": "A"
                }
            ],
            "medium": [
                {
                    "question": f"Which technique is commonly used in {subject}?",
                    "option_a": "Advanced technique A",
                    "option_b": "Advanced technique B",
                    "option_c": "Advanced technique C",
                    "option_d": "All of the above",
                    "correct_answer": "A"
                }
            ],
            "hard": [
                {
                    "question": f"What is an advanced concept in {subject}?",
                    "option_a": "Complex theory A",
                    "option_b": "Complex theory B",
                    "option_c": "Complex theory C",
                    "option_d": "Complex theory D",
                    "correct_answer": "A"
                }
            ]
        }
        
        questions = []
        template_list = templates.get(difficulty, templates["easy"])
        
        for i in range(count):
            q = template_list[i % len(template_list)].copy()
            q['subject'] = subject
            q['difficulty'] = difficulty
            if i > 0:
                q['question'] += f" (Part {i + 1})"
            questions.append(q)
        
        return questions

# Global instance
question_gen = QuestionGenerator()