import { useState } from "react";
import type { FormEvent } from "react";
import axios from "axios";
import "./App.css";

// Removed hardcoded API_URL — use relative path instead

interface ResponseData {
  answer: string;
  sources: Source[];
}

interface Source {
  title: string;
  authors: string[];
  source: string;
}

function App() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setAnswer("");
    setSources([]);

    try {
      const res = await axios.post<ResponseData>(
        "/query",  // relative path works when frontend + backend served together
        { query: question },
        { headers: { "Content-Type": "application/json" } }
      );

      setAnswer(res.data.answer);
      setSources(res.data.sources);
    } catch (err) {
      console.error(err);
      setAnswer("Error fetching answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App" style={{ maxWidth: "600px", margin: "auto", padding: "2rem" }}>
      <h1>ML Paper Interpreter</h1>
      <form onSubmit={handleSubmit}>
        <textarea
          rows={4}
          style={{ width: "100%", marginBottom: "1rem" }}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about ML interpretability..."
        />
        <button type="submit" disabled={loading}>
          {loading ? "Loading..." : "Submit"}
        </button>
      </form>

      {answer && (
        <div style={{ marginTop: "2rem" }}>
          <h3>Answer:</h3>
          <p>{answer}</p>
          {sources.length > 0 && (
            <div>
              <h4>Sources:</h4>
              <ul>
                {sources.map((src, idx) => (
                  <li key={idx}>
                    <strong>{src.title}</strong><br />
                    <em>by {src.authors.join(", ")}</em><br />
                    <a href={src.source} target="_blank" rel="noopener noreferrer">
                      {src.source}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
