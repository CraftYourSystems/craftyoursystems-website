# craftyoursystems-website
Official website for CraftYourSystems — a student development team building modern websites and software systems.
craftyoursystems/
│
├── backend/                      ← Python backend (Flask/FastAPI)
│   ├── app.py                    ← entry point
│   ├── requirements.txt
│   ├── setup.sql
│   ├── gunicorn.conf.py
│   ├── .env.example
│   ├── .gitignore
│
│   ├── db/
│   │   └── database.py
│
│   ├── middleware/
│   │   └── auth_middleware.py
│
│   ├── routes/
│   │   ├── auth.py
│   │   └── form.py
│
│   └── services/                 ← (add this, important)
│       ├── auth_service.py
│       └── form_service.py
│
│
├── frontend/                     ← all UI stuff
│   ├── index.html
│   ├── app.py (optional if serving frontend)
│
│   ├── assets/                   ← static files
│   │   ├── images/
│   │   │   ├── full-logo.png
│   │   │   ├── logo-single.png
│   │   │   └── logo-single-black.png
│   │   │
│   │   ├── css/
│   │   │   └── style.css
│   │   │
│   │   └── js/
│   │       ├── main.js
│   │       └── script.js
│
│   └── docs/                     ← frontend docs if needed
│
│
├── shared/                       ← optional but powerful
│   ├── config/
│   └── utils/
│
├── README.md
└── .gitignore