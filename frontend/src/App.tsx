import { useState, useRef, useEffect } from "react";
import type { FormEvent } from "react";
import ReactMarkdown from "react-markdown";
import axios from "axios";
import "./App.css";

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
  const [submitted, setSubmitted] = useState(false);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto expand textarea height
  useEffect(() => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = textarea.scrollHeight + "px";
    }
  }, [question]);

  const handleSubmit = async (e: FormEvent | React.KeyboardEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setAnswer("");
    setSources([]);
    setSubmitted(true); // trigger layout change

    try {
      const res = await axios.post<ResponseData>(
        "/query",
        { query: question },
        { headers: { "Content-Type": "application/json" } }
      );

      setAnswer(res.data.answer);
      setSources(res.data.sources);
    } catch (err) {
      console.error("❌ Error fetching answer:", err);
      setAnswer("Error fetching answer.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen w-screen bg-gray-900 text-white transition-all duration-700 px-4">
      <div
        className={`w-full max-w-2xl mx-auto transition-all duration-700 ease-in-out ${
          submitted ? "mt-16" : "flex items-center h-screen"
        }`}
      >
        <div className="w-full">
          <form
            onSubmit={handleSubmit}
            className="bg-gray-800 p-6 rounded-xl shadow-lg"
          >
            <h1 className="text-2xl font-bold mb-4 text-center">
              ML Paper Interpreter
            </h1>

            <textarea
              ref={textareaRef}
              className="w-full bg-gray-700 text-white p-3 rounded-md resize-none overflow-hidden focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault(); // prevent newline
                  handleSubmit(e); // trigger form submission
                }
              }}
              placeholder="Ask a question about ML interpretability..."
              style={{ minHeight: "3rem" }}
            />

            <button
              type="submit"
              disabled={loading}
              className="mt-4 w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 px-4 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? "Loading..." : "Search"}
            </button>
          </form>

          {answer && (
            <div className="mt-8 bg-gray-800 p-6 rounded-xl shadow-lg">
              <h2 className="text-xl font-semibold mb-2">Answer</h2>
              <div className="prose prose-invert text-gray-300 mb-4">
                <ReactMarkdown>
                  {answer}
                </ReactMarkdown>
              </div>

              {sources.length > 0 && (
                <div>
                  <h3 className="text-lg font-medium mb-2">Sources</h3>
                  <ul className="space-y-2 text-sm">
                    {sources.map((src, idx) => (
                      <li key={idx}>
                        <strong className="text-white">{src.title}</strong>
                        <br />
                        <em className="text-gray-400">
                          by {src.authors.join(", ")}
                        </em>
                        <br />
                        <a
                          href={src.source}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-400 hover:underline break-words"
                        >
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
      </div>
    </div>
  );
}

export default App;
