saber_pqc_project/
│
├── README.md
#├── LICENSE
#├── pyproject.toml          # modern packaging 
#├── setup.cfg               # config (linting, etc.)
#├── requirements.txt
│
├── saber_pqc/              # main package
│   ├── main.py             # high-level interface
│   │
│   ├── core/               # core implementation of SABER
│   │   ├── keygen.py
│   │   ├── encrypt.py
│   │   ├── decrypt.py
│   │
│   ├── utils/              # helpers & shared utilities
│   │
│   └── tests/              # unit tests inside package
│       ├── test_keygen.py
│       ├── test_encrypt.py
│       ├── test_decrypt.py
│
├── tests/                  # external tests (pytest)

│
├── docs/                   # documentation
│   ├── design.md
└── .gitignore
