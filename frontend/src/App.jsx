import { useState } from "react";
import axios from "axios";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const fetchQuery = async () => {
    const url = "http://localhost:8001/ask-question";

    try {
      const res = await axios.post(url, {
        question: query,
      });

      setResponse(res.data.response);
      console.log(res.data);
    } catch (err) {
      console.log(err.response?.data?.detail || err.message);
    }
  };

  const handleClick = async (ev) => {
    ev.preventDefault(); // To avoid the page from reloading

    console.log("The Query Submitted is:", query);

    await fetchQuery();
  };

  const handleInputChange = (ev) => {
    setQuery(ev.target.value); // Update the state when the input changes
  };

  const renderResponse = (response) => {
    if (!response) return null;

    // This assumes the response may have markdown formatting, so render it appropriately
    return (
      <div>
        <h3>Response:</h3>
        {/* Render as HTML, safely, in case it contains markdown like code blocks */}
        <div
          dangerouslySetInnerHTML={{
            __html: response.replace(
              /```sql([\s\S]*?)```/g,
              '<pre><code class="sql">$1</code></pre>'
            ),
          }}
        />
      </div>
    );
  };

  return (
    <>
      <h2>Simple React App to Generate SQL Queries</h2>
      <form>
        <label htmlFor="query">Query</label>
        <br />
        <input
          type="text"
          name="query"
          id="query"
          onChange={handleInputChange}
        />

        <br />
        <button onClick={handleClick}>Submit</button>
      </form>

      {/* Display the response after the API call */}
      {renderResponse(response)}
    </>
  );
}

export default App;
