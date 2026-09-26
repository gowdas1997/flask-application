from flask import Flask
import redis
import os
import random

app = Flask(__name__)
r = redis.Redis(host=os.environ.get("REDIS_HOST", "redis"), port=6379, decode_responses=True)

ENV_NAME = os.environ.get("ENV_NAME", "local")

THEMES = {
    "dev": {"bg1": "#667eea", "bg2": "#764ba2", "badge": "🛠️ DEVELOPMENT"},
    "prod": {"bg1": "#11998e", "bg2": "#38ef7d", "badge": "🚀 PRODUCTION"},
    "local": {"bg1": "#f7971e", "bg2": "#ffd200", "badge": "💻 LOCAL"},
}

QUOTES = [
    "Ship it and see what happens!",
    "Works on my cluster.",
    "Automated deployments = happy engineer.",
    "One push, zero manual steps.",
    "CI/CD: because manual deploys are for weekends off.",
    "Automated pipelines never call in sick.",
]

@app.route("/")
def home():
    count = r.incr("hits")
    theme = THEMES.get(ENV_NAME, THEMES["local"])
    quote = random.choice(QUOTES)
    return f"""
    <html>
    <head>
        <title>Flask + Redis | {ENV_NAME.upper()}</title>
        <style>
            * {{ margin: 0; padding: 0; box-sizing: border-box; }}
            body {{
                height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(-45deg, {theme['bg1']}, {theme['bg2']}, {theme['bg1']}, {theme['bg2']});
                background-size: 400% 400%;
                animation: gradientShift 8s ease infinite;
                font-family: 'Segoe UI', sans-serif;
                overflow: hidden;
                position: relative;
            }}
            @keyframes gradientShift {{
                0% {{ background-position: 0% 50%; }}
                50% {{ background-position: 100% 50%; }}
                100% {{ background-position: 0% 50%; }}
            }}
            .particle {{
                position: absolute;
                bottom: -50px;
                width: 12px;
                height: 12px;
                background: rgba(255,255,255,0.5);
                border-radius: 50%;
                animation: floatUp linear infinite;
            }}
            @keyframes floatUp {{
                0% {{ transform: translateY(0) translateX(0); opacity: 0; }}
                10% {{ opacity: 1; }}
                100% {{ transform: translateY(-110vh) translateX(30px); opacity: 0; }}
            }}
            .card {{
                background: rgba(255,255,255,0.15);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px 60px;
                text-align: center;
                color: white;
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
                animation: popIn 0.6s ease;
                z-index: 10;
                position: relative;
            }}
            @keyframes popIn {{
                0% {{ transform: scale(0.7); opacity: 0; }}
                100% {{ transform: scale(1); opacity: 1; }}
            }}
            .badge {{
                display: inline-block;
                background: rgba(0,0,0,0.25);
                padding: 6px 16px;
                border-radius: 20px;
                font-size: 14px;
                margin-bottom: 20px;
                letter-spacing: 1px;
                animation: pulse 2s ease-in-out infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ transform: scale(1); }}
                50% {{ transform: scale(1.08); }}
            }}
            h1 {{ font-size: 52px; margin: 10px 0; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
            p.quote {{ font-style: italic; opacity: 0.85; margin-top: 20px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="badge">{theme['badge']}</div>
            <h1>👋 Visit #{count}</h1>
            <p>Flask + Redis running on Kubernetes</p>
            <p class="quote">"{quote}"</p>
        </div>
        <script>
            for (let i = 0; i < 25; i++) {{
                const p = document.createElement('div');
                p.className = 'particle';
                p.style.left = Math.random() * 100 + 'vw';
                p.style.animationDuration = (5 + Math.random() * 8) + 's';
                p.style.animationDelay = (Math.random() * 8) + 's';
                p.style.width = p.style.height = (6 + Math.random() * 10) + 'px';
                document.body.appendChild(p);
            }}
        </script>
    </body>
    </html>
    """

@app.route("/health")
def health():
    return {"status": "ok", "env": ENV_NAME}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
