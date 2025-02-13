# PolyMesh - Interactive Polygon Meshing Tool

## 🛠️ Setup Instructions

### 1 Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd polymesh

### 2 Create a Virtual Environment

Mac & Linux
```bash
git clone https://github.com/YOUR_USERNAME/polymesh.git
cd polymesh


Windows
```powershell
python -m venv venv
venv\Scripts\activate


### 3 Install Dependencies
```bash
pip install -r requirements.txt


### 4 Create a .env File
```bash
touch .env


```powershell
New-Item -Path . -Name ".env" -ItemType "file"


Then open .env and add:
```ini
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

