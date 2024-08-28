# Singapore Flat Resale Price Prediction

"Price is what you pay and value is what you get."  
— Warren Buffett

## Overview

The resale flat market in Singapore is highly competitive, making it challenging to accurately estimate the resale value of a flat. Factors affecting resale prices include location, flat type, floor area, and lease duration. This project aims to develop a predictive model to estimate resale prices based on these factors, providing users with a reliable estimate of a flat's resale value.

## Objectives

- **Data Wrangling:** Clean and structure the acquired data.
- **Data Analysis:** Perform exploratory data analysis (EDA) to understand trends and patterns.
- **Feature Engineering:** Identify and develop key features to improve model accuracy.
- **ML Models:** Train and evaluate multiple machine learning models.
- **Model Deployment:** Deploy the predictive model via a Streamlit web application on the cloud.
- **User Accessibility:** Ensure the application is user-friendly and accessible online.

## Data Analysis

1. **Data Acquisition:** Collect data from the Singapore Housing and Development Board (HDB) on resale transactions from 1990 to the present.
2. **Data Preparation:** Clean and structure the data to make it suitable for machine learning applications.
3. **Feature Extraction:** Extract important features like town, flat type, storey range, floor area, flat model, and lease commence date.
4. **Feature Engineering:** Develop additional features to enhance the model's predictive power.

## Algorithm Selection

- **Model Selection:** Choose appropriate machine learning algorithms for regression (e.g., Linear Regression, Decision Trees, Random Forests).
- **Model Training:** Train the selected model using historical data.
- **Model Evaluation:** Evaluate the model using regression metrics such as MAE, MSE, RMSE, and R² Score.
- **Model Validation:** Validate model performance on unseen data to ensure accuracy and generalizability.

## Design and Implementation

- **Web Application Development:** Develop a Streamlit web application where users can input flat details.
- **Predictive Integration:** Integrate the trained model to predict resale prices based on user inputs.
- **Deployment:** Deploy the application on a cloud platform to ensure online accessibility.
- **User Experience:** Ensure the application is intuitive and easy to use.

## Testing and Feedback

- **Functional Testing:** Verify that all features of the application work correctly.
- **Accuracy Assessment:** Test the model's prediction accuracy using various test cases.
- **Performance Monitoring:** Monitor the application's performance under different conditions.
- **User Feedback Integration:** Collect user feedback for continuous improvement.

## Getting Started

To run this project locally:

1. Clone the repository.
2. Install the necessary dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

“Mistakes are the portals of discovery.”
