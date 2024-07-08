from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload and static directories exist
if not os.path.exists('uploads'):
    os.makedirs('uploads')

if not os.path.exists('static'):
    os.makedirs('static')

# Database configuration
DB_USERNAME = 'root'
DB_PASSWORD = '12345'
DB_HOST = 'localhost'
DB_PORT = '3306'
DB_NAME = 'flaskwebapp'

# SQLAlchemy engine
engine = create_engine(f"mysql+mysqlconnector://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


@app.route('/')
def index():
    return render_template('index.html')



@app.route('/summary')
def summary():
    # Example insights (replace with actual computed insights)
    insights = {
        'median_bmi': 24.5,
        'survival_rate': 0.85,
        'gender_distribution': {'Male': 300, 'Female': 200},
        'cancer_stage_distribution': {'Stage I': 150, 'Stage II': 200, 'Stage III': 100, 'Stage IV': 50}
    }
    return render_template('summary.html', insights=insights)


@app.route('/view_csv')
def view_csv():
    # Assuming there is only one uploaded CSV file
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not uploaded_files:
        return "No CSV file uploaded."

    # Display the first CSV file in the uploads directory
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_files[0])
    df = pd.read_csv(csv_path)

    # Select the first 100 rows
    df = df.head(100)

    csv_content = df.to_html(classes='table table-striped', index=False)
    return render_template('view_csv.html', csv_content=csv_content)


@app.route('/chart/<chart_type>')
def chart(chart_type):
    chart_info = {
        'treatment_duration': {
            'title': 'Treatment Duration and Survival Rate',
            'plot_path': 'treatment_duration.png',
            'description': '<strong>Insights:</strong> The chart vividly illustrates that patients undergoing treatment for more than a year have a significantly higher number of survivors compared to those with shorter treatment durations. This indicates the critical importance of sustained and comprehensive treatment plans in improving survival rates. The stark contrast between the "<3 months" and ">1 year" groups emphasizes the need for long-term treatment access and adherence. These insights advocate for healthcare policies that support prolonged treatment durations to enhance survival outcomes for lung cancer patients.',
            'additional_text': '<p><strong>Purpose:</strong> Understanding the impact of treatment duration on survival is crucial for optimizing lung cancer treatment plans. This analysis aims to determine how long-term treatment affects survival rates and identify the optimal duration for improving patient outcomes.</p><p><strong>Dataset, Analysis, Method, Statistics:</strong> The dataset comprises lung cancer patient survival status categorized by the duration of treatment—less than 3 months, 3-6 months, 6-12 months, and more than 1 year. A bar chart was created to show the number of survivors and non-survivors for each treatment duration. This visualization helps to compare the effectiveness of different treatment lengths.</p>'
        },
        'treatment_type': {
            'title': 'End of Treatment Outcomes by Treatment Type',
            'plot_path': 'treatment_type.png',
            'description': '<strong>Insights:</strong> The chart shows that all treatment types have more non-survivors than survivors, reflecting the aggressive nature of lung cancer. However, the survival rates are relatively similar across treatments, suggesting no single treatment is vastly superior. This calls for continued research into combining treatments and developing personalized medicine approaches to enhance effectiveness. The insights highlight the need for innovative strategies and comprehensive care plans to improve patient outcomes.',
            'additional_text': '<p><strong>Purpose:</strong> The aim is to evaluate the effectiveness of different lung cancer treatments byexamining the outcomes of patients who have undergone chemotherapy, combinedtherapy, radiation, or surgery. This analysis seeks to identify which treatments are most successful in improving survival rates.</p><p><strong>Dataset, Analysis, Method, Statistics:</strong> The dataset includes patient outcomes after different types of lung cancer treatments. A bar chart was utilized to compare the number of survivors and non-survivors for each treatment type. This method highlights the overall effectiveness and survival rates associated with each treatment option.</p>'
        },
        'family_history': {
            'title': 'Distribution of Lung Cancer Cases by Age Group and Family History',
            'plot_path': 'family_history.png',
            'description': '<strong>Insights:</strong> The chart reveals that individuals aged 50-59 years have the highest incidence of lung cancer, with a significant proportion having a family history of the disease. This suggests a potential genetic link or shared environmental factors, emphasizing the importance of early screening for those with a family history. The noticeable decline in cases after 60-69 years could indicate a survivor bias or diagnostic challenges. These insights stress the importance of targeted prevention measures and proactive health screenings to mitigate risks.',
            'additional_text': '<p><strong>Purpose:</strong>The goal here is to understand how age and family history contribute to the distribution of lung cancer cases. Identifying patterns in these factors can help in targeting prevention and early detection strategies more effectively, especially for those with a genetic predisposition.</p><p><strong>Dataset, Analysis, Method, Statistics:</strong> The dataset includes lung cancer cases categorized by age group and family history of cancer. A bar chart was used to display the number of cases in each age group, further divided by whether or not there was a family history of cancer. This method highlights the peak age groups for lung cancerdiagnoses and the potential impact of hereditary factors.</p>'
        },
        'age_group_survival': {
            'title': 'Survival Status by Age Group',
            'plot_path': 'age_group_survival.png',
            'description': '<strong>Insights:</strong> The chart reveals that late adults (50-69 years) have the highest number of both survivors and non-survivors, indicating high incidence and improved survival due to advancements in treatment. However, seniors (80+ years) shows second to young adult lower on non survivor and survived rates, The highlight here is the need for better support and tailored treatments for older patient specifically late adults for having more accumulated total of survivors and non survivors which also makes them have the lowest survival rate in all age categories. This data underscores the necessity for age-specific healthcare strategies to improve survival outcomes across all age groups.',
            'additional_text': '<p><strong>Purpose:</strong> Examining survival status by age group helps to uncover how different age demographics are affected by lung cancer and how survival rates vary with age. This information is vital for developing age-specific treatment and support strategies.</p><p><strong>Dataset, Analysis, Method, Statistics:</strong> s The analysis used a dataset of lung cancer patients, categorizing them into different age groups: teenagers, young adults, adults, late adults, and seniors. A stacked bar chart was created to show the number of survivors and non-survivors within each age group. This visualization provides a clear comparison of survival outcomes across different age brackets.</p>'
        },
        'age_smoking_heatmap': {
            'title': 'Survival Rate by Age Group and Smoking Status',
            'plot_path': 'age_smoking_heatmap.png',
            'description': '<strong>Insights:</strong> The insights drawn from this heatmap are profound. It illustrates that former smokers in the 80+ age group have the highest survival rate at 26.9%, underscoring the significant benefits of quitting smoking, even later in life. On the other hand, current smokers across all age groups exhibit lower survival rates, reinforcing the critical need for smoking cessation programs. This visualization tells a compelling story of hope and resilience, emphasizing that it’s never too late to quit smoking for better health outcomes.',
            'additional_text': '<p><strong>Purpose:</strong> Understanding the relationship between smoking status and survival rates across different age groups is crucial in the battle against lung cancer. Smoking is a well-known risk factor for lung cancer, but how quitting or continuing to smoke affects survival across ages is less clear. This analysis aims to highlight the importance of smoking cessation at any age and its potential impact on improving survival outcomes.</p><p><strong>Dataset, Analysis, Method, Statistics:</strong> Using a comprehensive dataset of lung cancer patients, we analyzed survival rates segmented by age group and smoking status— current smoker, former smoker, never smoked, and passive smoker. A heatmap was generated to visually represent these survival rates, providing an easy comparison across different categories. The analysis revealed varying survival outcomes, with former smokers in the 80+ age group showing a remarkably higher survival rate.</p>'
        }
    }

    if chart_type in chart_info:
        return render_template('chart_template.html',
                               title=chart_info[chart_type]['title'],
                               plot_path=chart_info[chart_type]['plot_path'],
                               description=chart_info[chart_type]['description'],
                               additional_text=chart_info[chart_type]['additional_text'])
    else:
        return "Chart type not found", 404





@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            process_file(filepath)  # If you want to process the file
            return redirect(url_for('summary'))
    return render_template('upload.html')


@app.route('/dataframe')
def dataframe():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if files:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], files[-1])  # Get the latest uploaded file
        df = pd.read_csv(filepath)

        # Generate statistical summary
        summary_df = df.describe().transpose()

        # Rename the index to avoid issues with BLOB/TEXT types
        summary_df.reset_index(inplace=True)
        summary_df.rename(columns={'index': 'feature'}, inplace=True)

        # Save statistical summary to MySQL
        summary_df.to_sql('dataframe_summary', con=engine, if_exists='replace', index=False)

        # Generate HTML for summary
        summary_html = summary_df.to_html(classes='table table-striped')
        return render_template('dataframe.html', summary=summary_html)
    else:
        return redirect(url_for('upload_file'))


@app.route('/overall_insights')
def overall_insights():
    return render_template('overall_insights.html')

def process_file(filepath):
    df = pd.read_csv(filepath)

    # Generate statistical summary
    summary_df = df.describe().transpose()

    # Rename the index to avoid issues with BLOB/TEXT types
    summary_df.reset_index(inplace=True)
    summary_df.rename(columns={'index': 'feature'}, inplace=True)

    # Save statistical summary to MySQL
    summary_df.to_sql('dataframe_summary', con=engine, if_exists='replace', index=False)

    # Generate treatment duration and survival rate visualization
    df['beginning_of_treatment_date'] = pd.to_datetime(df['beginning_of_treatment_date'])
    df['end_treatment_date'] = pd.to_datetime(df['end_treatment_date'])
    df['treatment_duration_days'] = (df['end_treatment_date'] - df['beginning_of_treatment_date']).dt.days
    df['treatment_duration_months'] = df['treatment_duration_days'] / 30.44

    bins = [0, 3, 6, 12, float('inf')]
    labels = ['1-3 months', '3-6 months', '6-12 months', '>1 year']
    df['treatment_duration_bin'] = pd.cut(df['treatment_duration_months'], bins=bins, labels=labels, right=False)
    aggregated_data = df.groupby(['treatment_duration_bin', 'survived']).size().unstack(fill_value=0)

    plt.figure(figsize=(10, 6))
    aggregated_data.plot(kind='bar', stacked=True, figsize=(10, 6), color=['red', 'green'])
    plt.xlabel('Treatment Duration')
    plt.ylabel('Number of Patients')
    plt.title('Treatment Duration and Survival Rate')
    plt.legend(['Non-Survivor', 'Survivor'], title='Survival Status')
    plt.grid(True)
    treatment_duration_path = os.path.join('static', 'treatment_duration.png')
    plt.savefig(treatment_duration_path)
    plt.close()

    # End of Treatment Outcomes by Treatment Type
    survival_counts = df.groupby(['treatment_type', 'survived']).size().unstack(fill_value=0).reset_index()
    survival_counts_melted = survival_counts.melt(id_vars='treatment_type', value_vars=[0, 1], var_name='survived',
                                                  value_name='count')
    plt.figure(figsize=(10, 6))
    sns.barplot(x='treatment_type', y='count', hue='survived', data=survival_counts_melted,
                palette={0: 'red', 1: 'green'})
    plt.xlabel('Treatment Type')
    plt.ylabel('Count')
    plt.title('End of Treatment Outcomes by Treatment Type')
    legend = plt.legend(title='Survived', labels=['Not Survived', 'Survived'])
    for text, color in zip(legend.get_texts(), ['red', 'green']):
        text.set_color(color)
    plt.grid(axis='y')
    treatment_type_path = os.path.join('static', 'treatment_type.png')
    plt.savefig(treatment_type_path)
    plt.close()

    # Impact of Family History on Age of Lung Cancer Onset
    age_bins = [0, 30, 40, 50, 60, 70, 80, float('inf')]
    age_labels = ['<30', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
    family_history_counts = df.groupby(['age_group', 'family_history']).size().unstack(fill_value=0)
    plt.figure(figsize=(10, 6))
    family_history_counts.plot(kind='bar', stacked=True, color=['blue', 'orange'])
    plt.xlabel('Age Group')
    plt.ylabel('Number of Patients')
    plt.title('Impact of Family History on Age of Lung Cancer Onset')
    plt.legend(title='Family History', labels=['No', 'Yes'])
    plt.grid(axis='y')
    family_history_path = os.path.join('static', 'family_history.png')
    plt.savefig(family_history_path)
    plt.close()

    # Survival Status by Age Group
    age_bins = [0, 18, 30, 50, 70, float('inf')]
    age_labels = ['Teenagers', 'Young Adults', 'Adults', 'Late Adults', 'Seniors']
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=age_labels, right=False)
    df['survival_status'] = df['survived'].map({1: 'Survived', 0: 'Not Survived'})
    survival_counts = df.groupby(['age_group', 'survival_status']).size().unstack(fill_value=0)
    plt.figure(figsize=(12, 8))
    survival_counts.plot(kind='bar', stacked=True, color=['green', 'red'])
    plt.xlabel('Age Group')
    plt.ylabel('Number of Patients')
    plt.title('Survival Status by Age Group')
    plt.legend(title='Survival Status', labels=['Survived', 'Not Survived'])
    plt.grid(axis='y')
    age_group_survival_path = os.path.join('static', 'age_group_survival.png')
    plt.savefig(age_group_survival_path)
    plt.close()

    # Survival Rate by Age Group and Smoking Status
    bins = [0, 30, 40, 50, 60, 70, 80, float('inf')]
    labels = ['<30', '30-39', '40-49', '50-59', '60-69', '70-79', '80+']
    df['age_bin'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
    survival_rates = df.groupby(['age_bin', 'smoking_status'])['survived'].mean().unstack() * 100
    plt.figure(figsize=(12, 8))
    sns.heatmap(survival_rates, annot=True, fmt=".1f", cmap="viridis", cbar_kws={'label': 'Survival Rate (%)'})
    plt.xlabel('Smoking Status')
    plt.ylabel('Age Group')
    plt.title('Survival Rate by Age Group and Smoking Status')
    age_smoking_heatmap_path = os.path.join('static', 'age_smoking_heatmap.png')
    plt.savefig(age_smoking_heatmap_path)
    plt.close()


if __name__ == '__main__':
    app.run(debug=True)
