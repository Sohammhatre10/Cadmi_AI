#First scrape the data and store as csv!!!
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

def classify_data_with_visualization(df):
    # Converting Cutoff to a numeric type 
    df["Cutoff"] = pd.to_numeric(df["Cutoff"], errors="coerce")

    # Bin the 'Cutoff' values into categories: Low, Medium, High
    cutoff_labels = ["Low", "Medium", "High"]
    df["Cutoff_Category"] = pd.qcut(df["Cutoff"], q=3, labels=cutoff_labels)

    # Dropping rows with missing values in Cutoff_Category
    df = df.dropna(subset=["Cutoff_Category"])

    # Encode categorical columns
    label_encoders = {}
    for column in ["College-name", "Program", "Category", "Gender", "Cutoff_Category"]:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    X = df[["College-name", "Program", "Category", "Gender"]] #features (X) 

    y = df["Cutoff_Category"] #target label (y)

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=64)

    # Initialize and train the model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))

    # Confusion Matrix
    conf_matrix = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(conf_matrix, annot=True, fmt="d", cmap="Blues", xticklabels=cutoff_labels, yticklabels=cutoff_labels)
    plt.xlabel("Predicted Labels")
    plt.ylabel("True Labels")
    plt.title("Confusion Matrix")
    plt.show()

    # Classification Report as DataFrame for bar plot
    report = classification_report(y_test, y_pred, output_dict=True)
    report_df = pd.DataFrame(report).transpose()
    
    # Plot Precision, Recall, F1-Score
    report_df[['precision', 'recall', 'f1-score']].iloc[:-3].plot(kind='bar', figsize=(10, 6))
    plt.title("Precision, Recall, F1-Score for Each Class")
    plt.xlabel("Classes")
    plt.ylabel("Scores")
    plt.show()

# Main function to load data from CSV, classify, and visualize
def main():
    df1 = pd.read_csv("du_cutoff_2024_first.csv")  
    df2 = pd.read_csv("du_cutoff_2024_second.csv")
    df3 = pd.read_csv("csab.csv")
    df4 = pd.read_csv("iitmain.csv")
    if not df1.empty:
        print("Data loaded successfully!")
        classify_data_with_visualization(df1)  #du cutoff 1
        classify_data_with_visualization(df2)  #du cutoff 2
        classify_data_with_visualization(df3)  #csab cutoff
        classify_data_with_visualization(df4)  #iitmain cutoff

if __name__ == "__main__":
    main()
