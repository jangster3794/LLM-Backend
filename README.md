# LangChain OpenAI API Integration

This repository contains a Flask application integrating OpenAI's GPT-3.5 model through the LangChain library. LangChain provides an easy-to-use interface for constructing complex conversational flows and queries using language models. This README file will guide you through the setup and usage of the API endpoints provided in this application.

## Prerequisites

Before you begin, ensure you have the following installed/configured:

- Python 3.6 or higher
- [Flask](https://flask.palletsprojects.com/en/2.1.x/) web framework
- [OpenAI API Key](https://beta.openai.com/signup/) (You can get it from OpenAI's official website)
- PyPDF2
- LangChain
- FAISS

## Installation

1. Clone the repository to your local machine:

    ```
    git clone https://github.com/jangster3794/LLM-Backend.git
    ```

2. Navigate to the project directory:

    ```
    cd LLM-Backend
    ```

3. Install the required Python packages:

    ```
    pip install -r requirements.txt
    ```

4. Set up your environment variables by creating a `.env` file in the project root directory and adding your OpenAI API key:

    ```
    OPENAI_API_KEY=your_openai_api_key
    ```

## Usage

### Running the Flask Application

To start the Flask application, run the following command in your terminal:

```
python main.py
```

The application will start running at `http://localhost:5000/`.

### API Endpoints

#### 1. **Single Query Endpoint**

   Send a single query to the OpenAI language model.

   - **Endpoint:** `openai_llm/single-query`
   - **Method:** `POST`
   - **Payload:**
     ```json
     {
       "question": "Your question here"
     }
     ```
   - **Response:**
     ```json
     {
       "success": true,
       "data": "Response from OpenAI model"
     }
     ```

#### 2. **Conversation Chain Endpoint**

   Manage a conversation with the OpenAI model using chained queries.

   - **Get Previous Conversation:**
     - **Endpoint:** `openai_llm/convo-chain`
     - **Method:** `GET`
     - **Response:**
       ```json
       {
         "success": true,
         "data": "Previous conversation from memory"
       }
       ```

   - **Send Input to Conversation Chain:**
     - **Endpoint:** `openai_llm/convo-chain`
     - **Method:** `POST`
     - **Payload:**
       ```json
       {
         "question": "Your question here"
       }
       ```
     - **Response:**
       ```json
       {
         "success": true,
         "data": "Response from OpenAI model"
       }
       ```

#### 3. **Create Vector Store from PDF Endpoint**

   Manage a conversation with the PDF Faiss vectorstore model using chained queries.


   - **Create Vector Store from PDF Endpoint:**
     - **Endpoint:** `pdf_ai_llm/create-store`
     - **Method:** `POST`
     - **Payload:**
       ```form-data
       {
         "file": "Your pdf file here"
       }
       ```
     - **Response:**
       ```json
       {
         "success": true,
         "data": "Response from API"
       }
       ```

#### 4. **Query PDF Vectorstore Endpoint**

   Send a query to the PDF AI vectorstore model.

   - **Endpoint:** `pdf_ai_llm/query`
   - **Method:** `POST`
   - **Payload:**
     ```json
     {
       "question": "Your question here"
     }
     ```
   - **Response:**
     ```json
     {
       "success": true,
       "data": "Response from PDF-FAISS vectorstore model"
     }
     ```
