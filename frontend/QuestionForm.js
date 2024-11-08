import React, { useState } from 'react';
import axios from 'axios';

function QuestionForm() {
    const [question, setQuestion] = useState("");
    const [response, setResponse] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);

        try {
            const result = await axios.post('http://localhost:8000/ask-question/', { question });
            setResponse(result.data);
        } catch (error) {
            console.error("Error fetching data:", error);
        }
        setLoading(false);
    };

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <label>Enter your question:</label>
                <input
                    type="text"
                    value={question}
                    onChange={(e) => setQuestion(e.target.value)}
                    required
                />
                <button type="submit">Submit</button>
            </form>

            {loading && <p>Loading...</p>}

            {response && (
                <div>
                    <h3>Generated SQL Query:</h3>
                    <p>{response.sql_query}</p>

                    <h3>Query Results:</h3>
                    <ul>
                        {response.query_result.map((row, index) => (
                            <li key={index}>{JSON.stringify(row)}</li>
                        ))}
                    </ul>

                    <h3>Generated Answer:</h3>
                    <p>{response.answer}</p>
                </div>
            )}
        </div>
    );
}

export default QuestionForm;
