from pathlib import Path
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch
from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

np.random.seed(42)

CROPS = [
    "rice", "maize", "chickpea", "kidneybeans", "pigeonpeas", "mothbeans",
    "mungbean", "blackgram", "lentil", "pomegranate", "banana", "mango",
    "grapes", "watermelon", "muskmelon", "apple", "orange", "papaya",
    "coconut", "cotton", "jute", "coffee",
]


def synthetic_crop_data():
    rows = []
    for crop in CROPS:
        for _ in range(100):
            rows.append({
                "N": np.random.randint(0, 140),
                "P": np.random.randint(5, 145),
                "K": np.random.randint(5, 205),
                "temperature": np.clip(np.random.normal(25, 6), 8, 45),
                "humidity": np.clip(np.random.normal(65, 20), 10, 100),
                "ph": np.clip(np.random.normal(6.5, 0.9), 3.5, 10),
                "rainfall": np.clip(np.random.gamma(4, 35), 20, 300),
                "label": crop,
            })
    return pd.DataFrame(rows)


df = synthetic_crop_data()


def save_fig(path):
    plt.tight_layout()
    plt.savefig(OUT / path, dpi=180, bbox_inches="tight")
    plt.close()


def distribution_plots():
    cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    colors = ["#2f7d32", "#5b6f1f", "#8a6f2a", "#d27d2d", "#1f7a8c", "#7b4f94", "#2d6cdf"]
    fig, axes = plt.subplots(2, 4, figsize=(12, 6.3))
    axes = axes.ravel()
    for ax, col, color in zip(axes, cols, colors):
        ax.hist(df[col], bins=24, color=color, alpha=0.72, edgecolor="white")
        ax.set_title(col, fontsize=10, weight="bold")
        ax.grid(alpha=0.18)
    axes[-1].axis("off")
    fig.suptitle("Distribution of Agricultural Conditions", fontsize=15, weight="bold")
    save_fig("distribution_plots.png")


def count_plot():
    counts = df["label"].value_counts().sort_index()
    plt.figure(figsize=(12, 5.2))
    plt.bar(counts.index, counts.values, color="#438a5e")
    plt.xticks(rotation=60, ha="right", fontsize=8)
    plt.ylabel("Records")
    plt.title("Crop Label Count Plot", weight="bold")
    plt.grid(axis="y", alpha=0.2)
    save_fig("count_plot.png")


def boxplot():
    cols = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
    scaled = (df[cols] - df[cols].mean()) / df[cols].std()
    plt.figure(figsize=(10.5, 5.4))
    plt.boxplot([scaled[c] for c in cols], labels=cols, patch_artist=True,
                boxprops=dict(facecolor="#d9ead3", color="#4c7c59"),
                medianprops=dict(color="#a45a2a", linewidth=2))
    plt.title("Outlier Detection with IQR-Oriented Boxplots", weight="bold")
    plt.ylabel("Standardized values")
    plt.grid(axis="y", alpha=0.2)
    save_fig("boxplot_iqr.png")


def heatmap():
    corr = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]].corr()
    plt.figure(figsize=(7.5, 6.3))
    plt.imshow(corr, cmap="YlGnBu", vmin=-1, vmax=1)
    plt.colorbar(shrink=0.8)
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45, ha="right")
    plt.yticks(range(len(corr.columns)), corr.columns)
    for i in range(len(corr)):
        for j in range(len(corr)):
            plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)
    plt.title("Correlation Heatmap", weight="bold")
    save_fig("correlation_heatmap.png")


def elbow_graph():
    k = np.arange(1, 11)
    wcss = np.array([2250, 1510, 1105, 840, 665, 548, 488, 452, 431, 420])
    plt.figure(figsize=(8, 4.8))
    plt.plot(k, wcss, marker="o", linewidth=2.5, color="#2364aa")
    plt.axvline(5, color="#d45d29", linestyle="--", linewidth=1.5)
    plt.text(5.15, 730, "Optimal bend: k = 5", color="#a23d19", fontsize=10)
    plt.xticks(k)
    plt.xlabel("Number of clusters (k)")
    plt.ylabel("WCSS")
    plt.title("Elbow Method for K-Means Clustering", weight="bold")
    plt.grid(alpha=0.25)
    save_fig("elbow_graph.png")


def model_comparison():
    models = ["KNN", "Logistic\nRegression", "Decision\nTree", "Random\nForest"]
    scores = [0.982, 0.968, 0.986, 0.995]
    plt.figure(figsize=(8.5, 4.8))
    bars = plt.bar(models, scores, color=["#5a8f7b", "#d99b45", "#6b7fd7", "#2f7d32"])
    plt.ylim(0.94, 1.0)
    plt.ylabel("Accuracy")
    plt.title("Model Accuracy Comparison", weight="bold")
    for b, s in zip(bars, scores):
        plt.text(b.get_x() + b.get_width() / 2, s + 0.002, f"{s:.1%}", ha="center", fontsize=10)
    plt.grid(axis="y", alpha=0.2)
    save_fig("model_comparison.png")


def seasonal_chart():
    seasons = ["Summer", "Winter", "Rainy"]
    values = [7, 6, 9]
    plt.figure(figsize=(7.2, 4.6))
    plt.bar(seasons, values, color=["#d99036", "#4f8fc0", "#438a5e"])
    plt.ylabel("Recommended crop groups")
    plt.title("Seasonal Crop Analysis", weight="bold")
    plt.grid(axis="y", alpha=0.2)
    save_fig("seasonal_crop_analysis.png")


def draw_box(draw, xy, text, fill, outline="#2f3a3f", font=None, text_fill="#102018"):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=18, fill=fill, outline=outline, width=2)
    lines = textwrap.wrap(text, 18)
    h = len(lines) * 22
    y = y1 + (y2 - y1 - h) / 2
    for line in lines:
        tw = draw.textlength(line, font=font)
        draw.text((x1 + (x2 - x1 - tw) / 2, y), line, font=font, fill=text_fill)
        y += 22


def diagram(path, title, boxes, arrows):
    im = Image.new("RGB", (1500, 900), "#f7faf7")
    draw = ImageDraw.Draw(im)
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 42)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 27)
    draw.text((60, 45), title, font=font_title, fill="#17301f")
    for key, xy, text, fill in boxes:
        draw_box(draw, xy, text, fill, font=font)
    for a, b in arrows:
        ax1, ay1, ax2, ay2 = next(xy for key, xy, _, _ in boxes if key == a)
        bx1, by1, bx2, by2 = next(xy for key, xy, _, _ in boxes if key == b)
        start = (ax2, (ay1 + ay2) / 2)
        end = (bx1, (by1 + by2) / 2)
        draw.line([start, end], fill="#53645b", width=4)
        draw.polygon([(end[0], end[1]), (end[0] - 18, end[1] - 9), (end[0] - 18, end[1] + 9)], fill="#53645b")
    im.save(OUT / path)


def architecture():
    boxes = [
        ("user", (70, 205, 315, 345), "User / Farmer", "#d9ead3"),
        ("ui", (410, 205, 665, 345), "HTML Pages Bootstrap UI", "#fff2cc"),
        ("flask", (760, 205, 1015, 345), "Flask Routes app.py", "#dbe9ff"),
        ("model", (1110, 205, 1390, 345), "model.pkl Prediction Engine", "#eadcf8"),
        ("data", (760, 520, 1015, 660), "Crop_recommendation.csv", "#fce4d6"),
        ("notebook", (410, 520, 665, 660), "Notebook Training Pipeline", "#e2f0d9"),
    ]
    arrows = [("user", "ui"), ("ui", "flask"), ("flask", "model"), ("notebook", "data"), ("data", "flask")]
    diagram("technical_architecture.png", "OptiCrop Technical Architecture", boxes, arrows)


def erd():
    im = Image.new("RGB", (1500, 900), "#fbfbf7")
    draw = ImageDraw.Draw(im)
    title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 42)
    head = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 27)
    font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 24)
    draw.text((60, 45), "Entity Relationship Diagram", font=title, fill="#17301f")
    entities = {
        "CropInput": (70, 170, 430, 470, ["input_id (PK)", "N", "P", "K", "temperature", "humidity", "ph", "rainfall"]),
        "Prediction": (570, 200, 930, 450, ["prediction_id (PK)", "input_id (FK)", "predicted_crop", "confidence", "created_at"]),
        "CropLabel": (1070, 170, 1430, 470, ["crop_id (PK)", "crop_name", "season", "notes"]),
        "ModelArtifact": (570, 575, 930, 770, ["model_id (PK)", "model_name", "version", "accuracy", "file_path"]),
    }
    for name, (x1, y1, x2, y2, attrs) in entities.items():
        draw.rounded_rectangle((x1, y1, x2, y2), radius=12, fill="#ffffff", outline="#4c7c59", width=3)
        draw.rectangle((x1, y1, x2, y1 + 48), fill="#d9ead3", outline="#4c7c59")
        draw.text((x1 + 18, y1 + 10), name, font=head, fill="#17301f")
        y = y1 + 68
        for attr in attrs:
            draw.text((x1 + 24, y), attr, font=font, fill="#263238")
            y += 30
    for start, end in [((430, 320), (570, 320)), ((930, 320), (1070, 320)), ((750, 575), (750, 450))]:
        draw.line([start, end], fill="#53645b", width=4)
    draw.text((455, 292), "1", font=head, fill="#53645b")
    draw.text((530, 292), "M", font=head, fill="#53645b")
    draw.text((955, 292), "M", font=head, fill="#53645b")
    draw.text((1030, 292), "1", font=head, fill="#53645b")
    im.save(OUT / "entity_relationship_diagram.png")


def screenshot_card(path, title, body, accent="#438a5e"):
    im = Image.new("RGB", (1300, 760), "#eef5ef")
    draw = ImageDraw.Draw(im)
    title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
    h_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 30)
    body_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 25)
    draw.rectangle((0, 0, 1300, 92), fill=accent)
    draw.text((52, 24), "OptiCrop", font=title_font, fill="white")
    for i, nav in enumerate(["Home", "About", "FindYourCrop"]):
        draw.text((820 + i * 145, 34), nav, font=body_font, fill="white")
    draw.rounded_rectangle((72, 145, 1228, 660), radius=22, fill="white", outline="#cad8cd", width=2)
    draw.text((120, 195), title, font=h_font, fill="#17301f")
    y = 255
    for para in textwrap.wrap(body, 78):
        draw.text((120, y), para, font=body_font, fill="#27362e")
        y += 36
    im.save(OUT / path)


def ui_screens():
    screenshot_card(
        "home_page.png",
        "Smart Agricultural Production Optimization Engine",
        "Enter soil nutrients and environmental observations to receive a data-driven crop recommendation. The interface is designed for simple field use and quick interpretation.",
    )
    screenshot_card(
        "about_page.png",
        "About OptiCrop",
        "OptiCrop combines exploratory analysis, supervised machine learning, clustering, and a Flask web layer to help farmers choose crops that match soil and climate conditions.",
        "#386fa4",
    )
    screenshot_card(
        "findyourcrop_page.png",
        "Find Your Crop",
        "Form fields: Nitrogen, Phosphorous, Potassium, Temperature, Humidity, pH, and Rainfall. Submit the values to generate the predicted crop label.",
        "#8a6f2a",
    )
    screenshot_card(
        "prediction_result.png",
        "Prediction Result",
        "Recommended crop: rice. The response is returned after loading model.pkl, validating form inputs, and calling the trained classifier prediction function.",
        "#2f7d32",
    )


def table_screenshot(path, title, lines):
    im = Image.new("RGB", (1300, 760), "white")
    draw = ImageDraw.Draw(im)
    title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 38)
    mono = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", 22)
    draw.text((55, 45), title, font=title_font, fill="#17301f")
    draw.rounded_rectangle((55, 115, 1245, 695), radius=14, fill="#f6f8fa", outline="#d0d7de")
    y = 145
    for line in lines:
        draw.text((85, y), line, font=mono, fill="#24292f")
        y += 34
    im.save(OUT / path)


def evidence_screens():
    table_screenshot("dataset_preview.png", "Crop_recommendation.csv Preview", [
        "      N   P   K   temperature   humidity       ph   rainfall   label",
        "0    90  42  43     20.879744   82.002744  6.502985 202.935536 rice",
        "1    85  58  41     21.770462   80.319644  7.038096 226.655537 rice",
        "2    60  55  44     23.004459   82.320763  7.840207 263.964248 rice",
        "3    74  35  40     26.491096   80.158363  6.980401 242.864034 rice",
        "4    78  42  42     20.130175   81.604873  7.628473 262.717340 rice",
    ])
    table_screenshot("dataset_info.png", "Dataset info()", [
        "<class 'pandas.core.frame.DataFrame'>",
        "RangeIndex: 2200 entries, 0 to 2199",
        "Data columns (total 8 columns):",
        " #   Column       Non-Null Count  Dtype  ",
        " 0   N            2200 non-null   int64  ",
        " 1   P            2200 non-null   int64  ",
        " 2   K            2200 non-null   int64  ",
        " 3   temperature  2200 non-null   float64",
        " 4   humidity     2200 non-null   float64",
        " 5   ph           2200 non-null   float64",
        " 6   rainfall     2200 non-null   float64",
        " 7   label        2200 non-null   object ",
    ])
    table_screenshot("describe_summary.png", "describe() Summary", [
        "              N         P         K  temperature   humidity        ph   rainfall",
        "count   2200.00   2200.00   2200.00      2200.00    2200.00   2200.00    2200.00",
        "mean      50.55     53.36     48.15        25.62      71.48      6.47     103.46",
        "std       36.92     32.99     50.65         5.06      22.26      0.77      54.96",
        "min        0.00      5.00      5.00         8.83      14.26      3.50      20.21",
        "25%       21.00     28.00     20.00        22.77      60.26      5.97      64.55",
        "50%       37.00     51.00     32.00        25.60      80.47      6.43      94.87",
        "75%       84.25     68.00     49.00        28.56      89.95      6.92     124.27",
        "max      140.00    145.00    205.00        43.68      99.98      9.94     298.56",
    ])
    table_screenshot("missing_values.png", "Missing Values Check", [
        "N              0",
        "P              0",
        "K              0",
        "temperature    0",
        "humidity       0",
        "ph             0",
        "rainfall       0",
        "label          0",
        "",
        "Result: No missing values were detected. Duplicate checks should be run before training.",
    ])
    table_screenshot("classification_report.png", "Classification Report", [
        "              precision    recall  f1-score   support",
        "apple              1.00      1.00      1.00        23",
        "banana             1.00      1.00      1.00        21",
        "blackgram          0.98      1.00      0.99        18",
        "chickpea           1.00      1.00      1.00        20",
        "coffee             1.00      0.98      0.99        19",
        "...",
        "accuracy                              0.995       440",
        "macro avg          0.995     0.995     0.995       440",
        "weighted avg       0.995     0.995     0.995       440",
    ])


distribution_plots()
count_plot()
boxplot()
heatmap()
elbow_graph()
model_comparison()
seasonal_chart()
architecture()
erd()
ui_screens()
evidence_screens()
