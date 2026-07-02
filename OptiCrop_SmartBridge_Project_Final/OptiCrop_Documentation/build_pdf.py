from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak,
    ListFlowable, ListItem, KeepTogether,
)


BASE = Path(__file__).parent
ASSETS = BASE / "assets"
OUT = BASE / "OptiCrop_Project_Documentation_SkillWallet.pdf"


styles = getSampleStyleSheet()
styles.add(ParagraphStyle("CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=30, leading=36, textColor=colors.HexColor("#2f7d32"), alignment=TA_CENTER, spaceAfter=16))
styles.add(ParagraphStyle("CoverSub", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=17, leading=22, alignment=TA_CENTER, textColor=colors.HexColor("#1f2a24"), spaceAfter=18))
styles.add(ParagraphStyle("H1x", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#2f7d32"), spaceBefore=12, spaceAfter=7))
styles.add(ParagraphStyle("H2x", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, textColor=colors.HexColor("#386fa4"), spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle("Bodyx", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=6))
styles.add(ParagraphStyle("Caption", parent=styles["BodyText"], fontName="Helvetica-Oblique", fontSize=8, leading=10, alignment=TA_CENTER, textColor=colors.HexColor("#5f6f65"), spaceBefore=3, spaceAfter=8))
styles.add(ParagraphStyle("CodexBlock", parent=styles["Code"], fontName="Courier", fontSize=7.2, leading=9, backColor=colors.HexColor("#f6f8fa"), borderPadding=6, spaceBefore=4, spaceAfter=7))


def p(text, style="Bodyx"):
    return Paragraph(text, styles[style])


def bullets(items):
    return ListFlowable(
        [ListItem(p(item), leftIndent=12) for item in items],
        bulletType="bullet",
        leftIndent=15,
        bulletFontSize=7,
        bulletColor=colors.HexColor("#2f7d32"),
    )


def numbered(items):
    return ListFlowable([ListItem(p(item), leftIndent=14) for item in items], bulletType="1", leftIndent=18)


def tbl(headers, rows, widths=None, header="#eaf4ea"):
    data = [[Paragraph(f"<b>{h}</b>", styles["Bodyx"]) for h in headers]]
    data += [[Paragraph(str(c), styles["Bodyx"]) for c in row] for row in rows]
    table = Table(data, colWidths=widths, hAlign="CENTER", repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header)),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.HexColor("#1f2a24")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cad8cd")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return [table, Spacer(1, 8)]


def fig(name, caption, width=6.1 * inch):
    path = ASSETS / name
    if not path.exists():
        return []
    im = Image(str(path))
    ratio = im.imageHeight / float(im.imageWidth)
    im.drawWidth = width
    im.drawHeight = width * ratio
    max_h = 6.5 * inch
    if im.drawHeight > max_h:
        im.drawHeight = max_h
        im.drawWidth = max_h / ratio
    return [KeepTogether([im, p(caption, "Caption")])]


def code(text):
    safe = text.strip().replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br/>")
    return p(safe, "CodexBlock")


def page_header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(colors.HexColor("#5f6f65"))
    canvas.drawString(0.62 * inch, A4[1] - 0.42 * inch, "OptiCrop: Smart Agricultural Production Optimization Engine")
    canvas.line(0.62 * inch, A4[1] - 0.48 * inch, A4[0] - 0.62 * inch, A4[1] - 0.48 * inch)
    canvas.drawRightString(A4[0] - 0.62 * inch, 0.42 * inch, f"Page {doc.page}")
    canvas.restoreState()


story = []
story += [Spacer(1, 1.1 * inch), p("OptiCrop", "CoverTitle"), p("Smart Agricultural Production Optimization Engine", "CoverSub")]
story += [p("Complete Artificial Intelligence and Machine Learning Project Documentation", "Caption"), Spacer(1, 0.3 * inch)]
story += tbl(["Field", "Details"], [
    ["Project Title", "OptiCrop: Smart Agricultural Production Optimization Engine"],
    ["Team Members", "To be filled by project team"],
    ["Team Lead", "To be filled by project team lead"],
    ["Submission", "SkillWallet / SmartBridge Project Documentation"],
    ["Technologies Used", "Python 3.x, Anaconda, Jupyter/Spyder, Flask, HTML5, CSS3, Bootstrap 5, JavaScript, NumPy, Pandas, Scikit-learn, Matplotlib, Seaborn, SciPy, Pickle, Git/GitHub"],
    ["Prepared On", "June 27, 2026"],
], [1.55 * inch, 4.75 * inch], "#eaf2fb")
story += [Spacer(1, 0.18 * inch), p("<b>Project Purpose:</b> OptiCrop predicts the most suitable crop from soil nutrient values and environmental conditions, helping farmers and agriculture stakeholders make data-driven production decisions."), PageBreak()]

sections = [
    "Hardware Requirements", "Software Requirements", "Problem Statement", "Business Requirements", "Literature Survey", "Social and Business Impact", "Dataset Description", "Data Collection", "Data Preprocessing", "Exploratory Data Analysis", "Seasonal Crop Analysis", "Train-Test Split", "Machine Learning Models", "Elbow Method", "Model Evaluation", "Model Saving", "Flask Application", "HTML Pages", "Python Backend", "Application Execution", "Screenshots", "Entity Relationship Diagram", "Technical Architecture", "Conclusion",
]
story += [p("Table of Contents", "H1x"), numbered(sections), PageBreak()]

story += [p("1. Hardware Requirements", "H1x"), p("The OptiCrop project runs on a standard entry-level development system. The dataset contains 2,200 records, so the computation is manageable for classroom and SkillWallet submission environments.")]
story += tbl(["Component", "Minimum Requirement", "Purpose"], [["Processor", "Intel Core i3 or above", "Runs notebook analysis, model training, and Flask server."], ["RAM", "Minimum 4 GB", "Supports Python, Pandas dataframes, and IDE tools."], ["Storage", "Minimum 10 GB free space", "Stores source code, dataset, notebooks, screenshots, and model artifacts."], ["Internet Connection", "Required", "Used for package installation, references, GitHub, and deployment preparation."]], [1.35*inch, 1.95*inch, 3.0*inch])

story += [p("2. Software Requirements", "H1x"), p("The software stack covers analysis, machine learning, visualization, model persistence, and web deployment.")]
story += tbl(["Category", "Software / Library", "Use in OptiCrop"], [["Operating System", "Windows / Linux / macOS", "Cross-platform local execution."], ["Python Runtime", "Python 3.x", "Programming language for notebook, training, and backend."], ["Development Tools", "Anaconda Navigator, Jupyter Notebook / Spyder, VS Code or PyCharm", "Interactive development and project editing."], ["Framework", "Flask Framework", "Routes and prediction web application."], ["Libraries", "NumPy, Pandas, Scikit-learn, Matplotlib, Seaborn, SciPy", "Data cleaning, training, evaluation, and charts."]], [1.45*inch, 2.3*inch, 2.55*inch], "#eaf2fb")

story += [p("3. Problem Statement", "H1x"), p("Farmers often select crops using habit, incomplete local information, or market pressure rather than measured soil and climate conditions. This can reduce yield, waste fertilizer, and increase financial risk. OptiCrop solves this by learning patterns from historical crop suitability data and recommending the crop that best matches new values for nitrogen, phosphorous, potassium, temperature, humidity, pH, and rainfall.")]

story += [p("4. Business Requirements", "H1x"), bullets(["Provide accurate crop recommendations from seven numeric agronomic inputs.", "Expose predictions through a simple, responsive web form.", "Compare multiple ML algorithms before choosing the final model.", "Save the final model as model.pkl for reuse in Flask.", "Include charts, screenshots, ERD, architecture, and evaluation evidence for SkillWallet review."])]
story += tbl(["Stakeholder", "Requirement", "Expected Value"], [["Farmers", "Simple recommendation interface", "Better crop choice and lower guesswork."], ["Researchers", "Interpretable analysis", "Evidence for crop-environment relationships."], ["Agribusiness", "Repeatable prediction flow", "Decision support for advisory tools."], ["Government", "Data-driven insights", "Support for sustainable planning."]], [1.45*inch, 2.25*inch, 2.6*inch])

story += [p("5. Literature Survey", "H1x"), p("Crop recommendation systems are a practical precision-agriculture application. Traditional systems depend on fixed expert rules and crop calendars, while machine learning can learn nonlinear relationships among nutrients, climate, and crop suitability. Classification models such as KNN, Logistic Regression, Decision Tree, and Random Forest are appropriate because the output is a crop label. Random Forest is especially useful for tabular agricultural data because it reduces single-tree overfitting and captures feature interactions. K-Means clustering adds unsupervised insight by grouping similar growing conditions.")]
story += tbl(["Approach", "Description", "Relevance"], [["Rule-based", "Uses expert thresholds.", "Useful baseline but less adaptive."], ["Supervised classification", "Maps features to crop labels.", "Primary prediction method."], ["Ensemble learning", "Combines decision trees.", "Strong final model candidate."], ["Clustering", "Groups similar records.", "Supports exploratory pattern discovery."]], [1.45*inch, 2.45*inch, 2.4*inch], "#eaf2fb")

story += [p("6. Social and Business Impact", "H1x"), p("OptiCrop can support improved productivity, lower fertilizer misuse, better water planning, and reduced crop-selection risk. It is also educationally valuable because it demonstrates a complete AI/ML workflow from dataset loading to web deployment."), bullets(["Productivity: recommends crops compatible with measured field conditions.", "Sustainability: encourages nutrient-aware and rainfall-aware planning.", "Business value: lowers risk from unsuitable crop selection.", "Educational value: provides a complete submission-ready project workflow."])]

story += [p("7. Dataset Description", "H1x"), p("The project uses Crop_recommendation.csv, a public crop recommendation dataset commonly available through Kaggle. It contains 2,200 records, eight columns, seven numeric features, and one target label. Dataset source: https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset")]
story += tbl(["Feature", "Description"], [["N", "Nitrogen ratio/content in soil."], ["P", "Phosphorous ratio/content in soil."], ["K", "Potassium ratio/content in soil."], ["temperature", "Ambient temperature."], ["humidity", "Relative humidity percentage."], ["ph", "Soil acidity/alkalinity value."], ["rainfall", "Rainfall condition."], ["label", "Crop name to predict."]], [1.55*inch, 4.75*inch])
story += fig("dataset_preview.png", "Figure 1: Dataset preview showing first records from Crop_recommendation.csv.")

story += [p("8. Data Collection", "H1x"), p("Data collection is performed by placing Crop_recommendation.csv in the project dataset folder and loading it with Pandas. The collected values combine soil fertility and environmental observations, making them suitable for crop suitability prediction."), code('''import pandas as pd\ndata = pd.read_csv("dataset/Crop_recommendation.csv")\ndata.head()''')]

story += [p("9. Data Preprocessing", "H1x"), p("Preprocessing checks dataset loading, preview, shape, info(), describe(), missing values, duplicates, data types, and outliers. The dataset shape is expected to be 2200 x 8. Missing values are checked using isnull().sum().")]
story += fig("dataset_info.png", "Figure 2: info() screenshot showing non-null counts and data types.")
story += fig("describe_summary.png", "Figure 3: describe() summary for numeric features.")
story += fig("missing_values.png", "Figure 4: Missing values check.")
story += [p("Outlier Detection, IQR, and Log Transformation", "H2x"), p("The IQR method detects values outside Q1 - 1.5 x IQR and Q3 + 1.5 x IQR. Agricultural outliers may be valid, so they are reviewed before transformation. Log transformation is applied only where strong positive skew affects interpretation, commonly for rainfall-like distributions."), code('''Q1 = data[numeric_columns].quantile(0.25)\nQ3 = data[numeric_columns].quantile(0.75)\nIQR = Q3 - Q1\nlower_bound = Q1 - 1.5 * IQR\nupper_bound = Q3 + 1.5 * IQR''')]
story += fig("boxplot_iqr.png", "Figure 5: Boxplot evidence for IQR-based outlier detection.")

story += [p("10. Exploratory Data Analysis", "H1x"), p("EDA includes univariate analysis, bivariate analysis, and multivariate analysis. Distribution plots show feature spread and skewness. Count plots verify class balance. Boxplots reveal outlier behavior. Correlation heatmaps show relationships among numeric variables.")]
story += fig("distribution_plots.png", "Figure 6: Distribution plots for agricultural conditions.")
story += fig("count_plot.png", "Figure 7: Count plot for crop labels.")
story += fig("correlation_heatmap.png", "Figure 8: Multivariate correlation heatmap.", 5.4*inch)

story += [p("11. Seasonal Crop Analysis", "H1x"), p("Seasonal analysis maps crop labels into Summer, Winter, and Rainy categories. This makes recommendations easier to interpret with local climate timing and water availability.")]
story += tbl(["Season", "Example Crops", "Interpretation"], [["Summer", "maize, cotton, mango, muskmelon, watermelon", "Higher temperature and irrigation planning matter."], ["Winter", "chickpea, lentil, kidneybeans, orange, apple", "Cooler conditions and lower humidity may be suitable."], ["Rainy", "rice, jute, coconut, papaya, pigeonpeas", "Rainfall and humidity strongly influence suitability."]], [1.1*inch, 2.55*inch, 2.65*inch])
story += fig("seasonal_crop_analysis.png", "Figure 9: Seasonal crop analysis.")

story += [p("12. Train-Test Split", "H1x"), p("Features X contain N, P, K, temperature, humidity, pH, and rainfall. Target y contains label. The dataset is split into 80% training and 20% testing, preferably with stratification to preserve class distribution."), code('''X = data.drop("label", axis=1)\ny = data["label"]\nX_train, X_test, y_train, y_test = train_test_split(\n    X, y, test_size=0.20, random_state=42, stratify=y\n)''')]

story += [p("13. Machine Learning Models", "H1x"), p("OptiCrop compares KNN, Logistic Regression, Decision Tree, Random Forest, and K-Means Clustering. The supervised models predict crop labels. K-Means is used for unsupervised grouping and exploratory insight.")]
story += tbl(["Model", "Purpose", "Strength"], [["KNN", "Predict by nearest records.", "Simple similarity-based recommendation."], ["Logistic Regression", "Linear multiclass baseline.", "Fast and interpretable."], ["Decision Tree", "Rule-based splits.", "Easy to explain."], ["Random Forest", "Ensemble of trees.", "Strong tabular accuracy and stability."], ["K-Means", "Cluster similar conditions.", "Reveals natural groups."]], [1.35*inch, 2.45*inch, 2.5*inch], "#eaf2fb")
story += fig("model_comparison.png", "Figure 10: Model accuracy comparison.")

story += [p("14. Elbow Method", "H1x"), p("WCSS means Within-Cluster Sum of Squares. It measures compactness by summing squared distances between records and cluster centroids. As k increases, WCSS decreases. The optimal clusters are chosen near the elbow, where adding more clusters gives diminishing improvement.")]
story += fig("elbow_graph.png", "Figure 11: Elbow graph for K-Means clustering.")

story += [p("15. Model Evaluation", "H1x"), p("Evaluation uses accuracy, precision, recall, F1 score, confusion matrix, and classification report. Accuracy gives overall correctness, while precision/recall/F1 show class-level reliability. A confusion matrix identifies which crops are confused.")]
story += tbl(["Metric", "Meaning"], [["Accuracy", "Correct predictions divided by total predictions."], ["Precision", "Reliability of predicted crop labels."], ["Recall", "Ability to capture actual crop classes."], ["F1 Score", "Balanced precision and recall."], ["Confusion Matrix", "Actual-vs-predicted class matrix."], ["Classification Report", "Detailed per-class precision, recall, F1, and support."]], [1.7*inch, 4.6*inch])
story += fig("classification_report.png", "Figure 12: Classification report evidence.")

story += [p("16. Model Saving", "H1x"), p("The selected model is serialized with Pickle and saved as model.pkl. The Flask backend loads this file at runtime instead of retraining the model for every request."), code('''import pickle\nwith open("model.pkl", "wb") as file:\n    pickle.dump(best_model, file)''')]

story += [p("17. Flask Application", "H1x"), p("The Flask application provides the web interface and route handling. It receives POST values from the prediction form, converts them to float, loads model.pkl, calls predict(), and renders the result.")]
story += tbl(["Route", "Page", "Responsibility"], [["/", "Home", "Project overview, navigation, hero, footer."], ["/about", "About", "Objectives, workflow, technologies, benefits."], ["/findyourcrop", "FindYourCrop", "Input form for seven values."], ["/predict", "Prediction Result", "POST handling and crop prediction."]], [1.2*inch, 1.65*inch, 3.45*inch], "#eaf2fb")

story += [p("18. HTML Pages", "H1x"), p("HTML pages include Home, About, FindYourCrop, and Result. Bootstrap 5 supports responsive layout, cards, buttons, navigation bar, and agriculture-themed styling.")]
story += fig("home_page.png", "Figure 13: Home Page screenshot.")
story += fig("about_page.png", "Figure 14: About Page screenshot.")
story += fig("findyourcrop_page.png", "Figure 15: FindYourCrop Page screenshot.")
story += fig("prediction_result.png", "Figure 16: Prediction Result screenshot.")

story += [p("19. Python Backend", "H1x"), code('''app = Flask(__name__)\nmodel = pickle.load(open("model.pkl", "rb"))\n\n@app.route("/predict", methods=["POST"])\ndef predict():\n    values = [float(request.form[field]) for field in\n              ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]\n    prediction = model.predict(np.array(values).reshape(1, -1))[0]\n    return render_template("result.html", prediction=prediction)\n\nif __name__ == "__main__":\n    app.run(debug=True)''')]

story += [p("20. Application Execution", "H1x"), numbered(["Open the project folder.", "Install packages using requirements.txt.", "Train the model and generate model.pkl.", "Run python app.py.", "Open http://127.0.0.1:5000.", "Submit the FindYourCrop form and verify the prediction result."]), code('''pip install -r requirements.txt\npython model/train_model.py\npython app.py''')]

story += [p("21. Screenshots", "H1x"), p("The report includes required screenshots under relevant headings. The supplied OptiCrop PDF pages are included below as source evidence pages.")]
story += tbl(["Screenshot Requirement", "Included As"], [["Dataset", "Figure 1 and source page 1"], ["Graphs", "Figures 6-8 and source pages"], ["Boxplot", "Figure 5"], ["Elbow Graph", "Figure 11"], ["Classification Report", "Figure 12"], ["Prediction Result", "Figure 16"], ["Home/About/FindYourCrop", "Figures 13-15"]], [2.6*inch, 3.7*inch])
for i in range(1, 11):
    story += fig(f"source_page-{i:02}.png", f"Source Screenshot Page {i}: Evidence extracted from the supplied OptiCrop PDF.", 4.85*inch)

story += [p("22. Entity Relationship Diagram", "H1x"), p("OptiCrop can run from CSV files, but the ERD below models a production database design for storing submitted inputs, predictions, crop labels, and model artifacts.")]
story += fig("entity_relationship_diagram.png", "Figure 17: Logical ERD for OptiCrop.", 6.3*inch)

story += [p("23. Technical Architecture", "H1x"), p("The architecture separates presentation, application, ML, and data layers. The notebook trains and evaluates models, Pickle stores the selected model, Flask loads model.pkl, and HTML templates collect inputs and display predictions.")]
story += fig("technical_architecture.png", "Figure 18: OptiCrop technical architecture.", 6.3*inch)

story += [p("24. Conclusion", "H1x"), p("OptiCrop demonstrates a complete end-to-end AI and machine learning workflow for smart agricultural production optimization. It defines a practical problem, uses a structured crop recommendation dataset, performs preprocessing and EDA, trains and compares multiple models, evaluates classification performance, saves the final model, and deploys prediction through a Flask web application."), p("The documentation is structured for SkillWallet submission with cover page, requirements, business context, literature survey, dataset description, preprocessing, EDA, seasonal analysis, train-test split, ML models, K-Means elbow method, evaluation, model saving, Flask application details, screenshots, ERD, technical architecture, and conclusion.")]

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=0.62*inch, leftMargin=0.62*inch, topMargin=0.72*inch, bottomMargin=0.62*inch)
doc.build(story, onFirstPage=page_header_footer, onLaterPages=page_header_footer)
print(OUT)
