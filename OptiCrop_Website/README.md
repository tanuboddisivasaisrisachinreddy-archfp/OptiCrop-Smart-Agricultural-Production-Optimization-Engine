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
