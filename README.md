# Student Details FastAPI Project

## Folder Structure

```plaintext
student_details/
├── app/
│   ├── core/
│   │   ├── config.py             # Future env configs
│   │   └── middleware.py         # Custom logging middleware
│   ├── models/
│   │   └── student.py            # Pydantic models for Student
│   ├── routes/
│   │   └── student_routes.py     # All /students endpoints
│   ├── services/
│   │   └── student_service.py    # CRUD logic and in-memory store
│   ├── store/
│   │   └── memory_store.py       # In-memory data store and lock
│   ├── utils/
│   │   └── ollama_client.py      # Ollama API integration
│   └── main.py                   # FastAPI app entry point
├── venv/                         # Python virtual environment
└── README.md                     # Project documentation
```

## How to Run

1. **Install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

2. **Start the server:**

    ```sh
    uvicorn app.main:app --reload
    ```

3. **API Docs:**  
   Visit [http://localhost:8000/docs](http://localhost:8000/docs)

## Ollama Installation & Running Instructions

### 1. **Install Ollama**

Follow the official instructions for your platform:  
[https://ollama.com/download](https://ollama.com/download)

**For Linux (x86_64):**

```sh
curl -fsSL https://ollama.com/install.sh | sh
```

**For macOS:**

```sh
brew install ollama
```

**For Windows:**  
Download and run the installer from the [Ollama website](https://ollama.com/download).

---

### 2. **Start the Ollama Server**

After installation, start the Ollama server:

```sh
ollama serve
```

This will run the Ollama API at `http://localhost:11434` by default.

---

### 3. **Pull a Model (e.g., mistral)**

Before using the API, pull the model you want (as set in your `.env`):

```sh
ollama pull mistral
```

Replace `mistral` with your desired model name if different.

---

### 4. **Verify Ollama is Running**

You can check the version to verify the server is up:

```sh
curl http://localhost:11434/api/version
```

---

### 5. **Environment Variables**

Make sure your `.env` file matches the Ollama server and model configuration:

```plaintext
OLLAMA_API_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=mistral
OLLAMA_VERSION_URL=http://localhost:11434/api/version
```

---

**Now your FastAPI app can connect to the Ollama API for AI-powered

## Features

- CRUD for students
- Input validation with Pydantic
- Unique email enforcement
- Logging middleware
- Ollama AI summary endpoint
- Proper error handling

## Example API Usage (cURL)

### Create Student

```sh
curl -X POST "http://localhost:8000/students/" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith", "age": 22, "email": "alice.smith@example.com"}'
```

### Get All Students

```sh
curl "http://localhost:8000/students/"
```

### Get Student by ID

```sh
curl "http://localhost:8000/students/1"
```

### Update Student

```sh
curl -X PUT "http://localhost:8000/students/1" \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "age": 23, "email": "alice.johnson@example.com"}'
```

### Delete Student

```sh
curl -X DELETE "http://localhost:8000/students/1"
```

### Test Route

```sh
curl "http://localhost:8000/students/test"
```

### Get Student AI Summary

```sh
curl "http://localhost:8000/students/1/summary"
```
