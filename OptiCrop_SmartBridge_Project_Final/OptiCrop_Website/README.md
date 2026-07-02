# OptiCrop Website

OptiCrop is a Flask web application that recommends a suitable crop from soil and environmental inputs.

## Run in Terminal

```bash
cd "/Users/sachintanuboddi/Documents/New project/OptiCrop_Website"
/opt/anaconda3/bin/python3 app.py
```

Open this URL in your browser:

```text
http://127.0.0.1:5000
```

If `model.pkl` is placed in this folder, the app uses it automatically. Without `model.pkl`, the app uses a simple fallback recommendation function so the website still runs.

## Deploy on Render

Use these settings:

```text
Root Directory: OptiCrop_Website
Build Command: pip install -r requirements.txt
Start Command: gunicorn wsgi:app
```

The app also includes a `Procfile` and `render.yaml` for Python web deployment.
