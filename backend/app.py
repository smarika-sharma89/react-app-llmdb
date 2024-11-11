from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import psycopg2
from openai import OpenAI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()  # Load environment variables

# Retrieve database configuration from environment variables
db_name = "staging_sept_23"
db_user = "postgres"
db_host = "localhost"
db_port = 5432
db_password = ""  # No password

# Construct the database URL
db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


def get_db_connection():
    try:
        conn = psycopg2.connect(db_url)
        return conn
    except Exception as e:
        print("Failed to connect to PostgreSQL:", e)
        raise


client = OpenAI()

# Configure OpenAI API key
client.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic model for request payload
class QuestionRequest(BaseModel):
    question: str


@app.on_event("startup")
async def startup():
    # Ensure DB connection is available
    get_db_connection()


def get_gpt_response(question, prompt):
    messages = [
        {"role": "system", "content": prompt[0]},
        {"role": "user", "content": question},
    ]
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages
    )
    response = completion.choices[0].message.content
    return response


@app.post("/ask-question/")
async def ask_question(request: QuestionRequest):
    question = request.question
    print(question)
    # Define prompt with table names
    db_conn = get_db_connection()
    print("HeRE!!!")
    table_names_str = ", ".join(fetch_table_names(db_conn))
    # print(table_names_str)
    prompt = [
        f"""
        You are an expert in converting English questions to PostgreSQL SQL query.
        The PostgreSQL database contains the following tables: {table_names_str}.
        Based on these tables, generate a query.
        """
    ]

    try:
        # Generate SQL query using GPT
        sql_query = get_gpt_response(question, prompt)

        # THIS PART IS FAILING BECAUSE OF INCORRECT SQL QUERY GENERATION (FIX THIS)
        # Execute the SQL query
        # data = execute_sql_query(db_conn, sql_query)

        # answer = get_proper_answer(question, data)

        # return {"sql_query": sql_query, "query_result": data, "answer": answer}
        return {"response": sql_query}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


def execute_sql_query(db_conn, sql):
    cur = db_conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    return rows


def fetch_table_names(db_conn):
    cur = db_conn.cursor()
    cur.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema='public';
    """
    )
    tables = [table[0] for table in cur.fetchall()]
    cur.close()
    return tables


def get_proper_answer(question, data):
    data_str = "\n".join([str(row) for row in data])
    prompt = [
        f"""
        Based on the following data from the database: {data_str}, answer the question: {question}.
        """
    ]
    return get_gpt_response(question, prompt)
