import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load dataset
file_path = 'C:/Users/shiva/Downloads/synthetic_crime_data.csv'

df = pd.read_csv(file_path)

# Define first and second set of inputs
first_set = ["Crime Type", "Weapon Used", "Crime Location", "Time of Crime", "Weather", "Victim Age", "Victim Gender", "Victim Occupation", "Financial Status", "Psychological Traits", "Social Interactions", "Online Activity", "Witness Count", "Witness Reliability Score", "DNA Evidence", "CCTV Footage", "Call Records", "Internet Activity"]
second_set = ["Crime Hotspots", "Similar Patterns", "Distance to Suspect", "Risk-Taking Behavior", "Emotional Triggers", "Lying Patterns", "Social Interaction Patterns"]

categorical_cols = [col for col in first_set + second_set if df[col].dtype == 'object']
numerical_cols = [col for col in first_set + second_set if col not in categorical_cols]

# Encode categorical columns
label_encoders = {}
for col in categorical_cols:
    label_encoders[col] = LabelEncoder()
    df[col] = label_encoders[col].fit_transform(df[col])

# Define target column names based on actual dataset
Y_columns = {"Criminal Type": "Criminal Type", "Crime Category": "Crime Category", "Behavioral Tendencies": "Behavioral Tendencies", "Psychological Profile": "Psychological Profile"}
Y = df[list(Y_columns.keys())]  # Use actual column names from dataset

# Split dataset
X_train, X_test, Y_train, Y_test = train_test_split(df[first_set], Y, test_size=0.2, random_state=42)

# Train models
models = {}
for col in Y.columns:
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, Y_train[col])
    models[col] = model

# GUI function
def predict_crime():
    user_inputs = []
    for col in first_set:
        if col in categorical_cols:
            user_inputs.append(label_encoders[col].transform([dropdown_vars[col].get()])[0])
        else:
            user_inputs.append(float(entry_vars[col].get()))
    
    # Convert input to DataFrame with feature names
    user_inputs_df = pd.DataFrame([user_inputs], columns=first_set)
    
    # Predict
    predictions = {col: models[col].predict(user_inputs_df)[0] for col in models.keys()}
    
    # Ensure Correct Key Usage
    decoded_predictions = {}
    for col in predictions:
        if col in label_encoders:
            decoded_predictions[col] = label_encoders[col].classes_[predictions[col]]
        else:
            decoded_predictions[col] = predictions[col]
    
    # Show output in a separate dialog box
    output_message = (f"Criminal Type: {decoded_predictions['Criminal Type']}\n"
                      f"Crime Category: {decoded_predictions['Crime Category']}\n"
                      f"Behavioral Tendencies: {decoded_predictions['Behavioral Tendencies']}\n"
                      f"Psychological Profile: {decoded_predictions['Psychological Profile']}")
    messagebox.showinfo("Crime Prediction Result", output_message)
    ask_additional_analysis()

# Function to ask for additional analysis
def ask_additional_analysis():
    response = messagebox.askyesno("Additional Analysis", "Do you need to analyze the criminal further with more inputs?")
    if response:
        collect_additional_inputs()

# Function to collect additional inputs
def collect_additional_inputs():
    additional_window = tk.Toplevel(app)
    additional_window.title("Additional Inputs")
    additional_vars = {}
    
    for col in second_set:
        frame = tk.Frame(additional_window, bg='#f0f0f0')
        frame.pack(fill='x', padx=10, pady=2)
        tk.Label(frame, text=col, bg='#f0f0f0', font=("Arial", 10)).pack(side='left')
        additional_vars[col] = tk.StringVar()
        unique_values = list(label_encoders[col].classes_)
        dropdown = ttk.Combobox(frame, textvariable=additional_vars[col], values=unique_values)
        dropdown.pack(side='right')
        dropdown.current(0)
    
    def submit_additional():
        additional_window.destroy()
        messagebox.showinfo("Analysis Complete", "Criminal profiling updated with additional inputs.")
    
    submit_button = tk.Button(additional_window, text="Submit", command=submit_additional, bg='#4CAF50', fg='white')
    submit_button.pack()

# Initialize Tkinter app
app = tk.Tk()
app.title("Crime Prediction System")
app.geometry("600x500")
app.configure(bg='#d9e6f2')

# Create frames for input fields
frame_top = tk.Frame(app, bg='#d9e6f2')
frame_top.pack(fill='x', padx=20, pady=10)
frame_bottom = tk.Frame(app, bg='#d9e6f2')
frame_bottom.pack(fill='x', padx=20, pady=10)

dropdown_vars = {}
entry_vars = {}

for i, col in enumerate(first_set):
    parent_frame = frame_top if i < len(first_set) // 2 else frame_bottom
    frame = tk.Frame(parent_frame, bg='#d9e6f2')
    frame.pack(fill='x', padx=5, pady=2)
    tk.Label(frame, text=col, bg='#d9e6f2', font=("Arial", 10, "bold")).pack(side='left')
    if col in categorical_cols:
        dropdown_vars[col] = tk.StringVar()
        unique_values = list(label_encoders[col].classes_)
        dropdown = ttk.Combobox(frame, textvariable=dropdown_vars[col], values=unique_values)
        dropdown.pack(side='right')
        dropdown.current(0)
    else:
        entry_vars[col] = tk.StringVar()
        entry = tk.Entry(frame, textvariable=entry_vars[col])
        entry.pack(side='right')

# Predict button
predict_button = tk.Button(app, text="Predict", command=predict_crime, bg='#008CBA', fg='white', font=("Arial", 12, "bold"))
predict_button.pack(pady=10)

app.mainloop()


