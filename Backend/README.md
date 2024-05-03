You can run the backend server manually:

# Manual Installation

## Requirements
Python >= 3.9

## Setup

First, clone this repo and change your working directory to the cloned repo:

```bash
    git clone https://github.com/KalaRohit/Google-AI-Hackathon
    cd Google-AI-Hackathon
```

Then, create a Python virtual envrionment:
```bash
    python -m venv venv
```

Activate this venv for your particular shell application:
```bash
    source venv/bin/activate #linux/mac
    venv\Scripts\activate #command prompt
    venv\Scripts\Activate.ps1 #powershell
```

Change the directory to the backend folder within the repo:
```bash
    cd Backend
```

Install the requirements:
```bash
    pip install -r requirements.txt
```

You can now run the server using the following command:
```bash
    uvicorn simple_script_sever:app --port 8000
```


# Installing using the Dockerfile

## Requirements

Docker version 24.0.7

## Setup

First, clone this repo and change your working directory to the cloned repo:

```bash
    git clone https://github.com/KalaRohit/Google-AI-Hackathon
    cd Google-AI-Hackathon
```

Then build the backend dockerfile:

```bash
    docker build -t simple_script_server . -f backend.dockerfile
```

Next, run the built image:

```bash
    docker run -p 8000:80 simple_script_server
```


# Testing Installation

Open up your browser and go to localhost:8000
```bash
    http://localhost:8000/
```

If it says Hello World, your installation is succesful.
