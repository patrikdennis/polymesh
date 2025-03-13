# PolyMesh - Interactive Polygon Meshing Tool

## 🛠️ Setup Instructions

### 1 Clone the Repository

```bash
git clone https://github.com/patrikdennis/polymesh.git
cd polymesh
```

### 2 Create a Virtual Environment

Mac/linux & Windows
```powershell
python -m venv venv
activate venv
```


### 3 Install Dependencies
Mac/linux
```bash
pip install -r requirements.txt
```


### 4 Create a .env File
Mac/linux
```bash
touch .env
```

Windows
```powershell
New-Item -Path . -Name ".env" -ItemType "file"
```


Then open .env and add:
```ini
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
```

## Run
```bash
python3 manage.py runserver
```

Finally copy and paste the development server domain.

