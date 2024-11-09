import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize WebDriver
def init_driver(chrome_driver_path=None):
    options = webdriver.ChromeOptions()
    if chrome_driver_path:
        return webdriver.Chrome(executable_path=chrome_driver_path, options=options)
    return webdriver.Chrome(options=options)

# Scrape data function
def fetch_cutoff_data(heading_text):
    driver = init_driver()
    data = []
    try:
        driver.get("https://www.shiksha.com/science/articles/cuet-du-cut-off-blogId-129629")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        # Find the heading for the specified cutoff round
        cutoff_heading = soup.find('h2', string=heading_text)
        if not cutoff_heading:
            print(f"Error: '{heading_text}' heading not found.")
            return []
        table = cutoff_heading.find_next('table')
        if not table:
            print("Error: No table found after the heading.")
            return []

        rows = table.find_all('tr')
        count = 0
        for row in rows:
            columns = row.find_all(['th', 'td'])
            row_data = [col.get_text(strip=True) for col in columns]
            # Rearrange columns based on desired order:
            if len(row_data) == 4 and count > 0:
                gender = "Gender-Neutral" if "W" not in college_name else "Female-only"
                arranged_data = [
                    college_name, # College name 
                    row_data[0],  # Program
                    row_data[1],  # Category
                    gender,       # Gender
                    row_data[2],  # Cutoff-Rank
                ]
                data.append(arranged_data)
            elif len(row_data) == 1:
                college_name = row_data[0]
                count = 1
    except Exception as e:
        print(f"An error occurred during scraping for {heading_text}: {e}")
    finally:
        driver.quit()
    return data

# Scrape both rounds and combine data
def scrape_and_combine_data():
    data_first = fetch_cutoff_data("CUET DU 2024 First Cut Off")
    data_second = fetch_cutoff_data("CUET DU 2024 Second Cut Off")
    combined_data = data_first + data_second
    df = pd.DataFrame(combined_data, columns=["College-name", "Program", "Category", "Gender", "Cutoff"])
    return df

# Classification code with visualization
def classify_data_with_visualization(df):
    # Convert Cutoff to a numeric type if necessary
    df["Cutoff"] = pd.to_numeric(df["Cutoff"], errors="coerce")

    # Bin the 'Cutoff' values into categories: Low, Medium, High
    cutoff_labels = ["Low", "Medium", "High"]
    df["Cutoff_Category"] = pd.qcut(df["Cutoff"], q=3, labels=cutoff_labels)

    # Drop rows with missing values in Cutoff_Category
    df = df.dropna(subset=["Cutoff_Category"])

    # Encode categorical columns
    label_encoders = {}
    for column in ["College-name", "Program", "Category", "Gender", "Cutoff_Category"]:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    # Define features (X) and target labels (y)
    X = df[["College-name", "Program", "Category", "Gender"]]
    y = df["Cutoff_Category"]

    # Split the data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=33)

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

# Main function to scrape, classify, and visualize
def main():
    df = scrape_and_combine_data()
    if not df.empty:
        print("Data scraped successfully!")
        classify_data_with_visualization(df)

if __name__ == "__main__":
    main()
