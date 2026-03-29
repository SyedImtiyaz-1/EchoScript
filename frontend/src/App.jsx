import { useState, useCallback } from "react";
import TextInput from "./components/TextInput";
import Settings from "./components/Settings";
import AudioOutput from "./components/AudioOutput";
import { synthesize, detectLanguage } from "./services/api";

export default function App() {
  const [text, setText] = useState("");
  const [settings, setSettings] = useState({
    voice: "male",
    language: "auto",
    speed: "normal",
    style: "neutral",
  });
  const [detectedLang, setDetectedLang] = useState({ code: "", name: "", confidence: 0 });
  const [status, setStatus] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const onLanguageDetected = useCallback((code, name, confidence) => {
    setDetectedLang({ code, name, confidence });
  }, []);

  const handleTextChange = useCallback(
    async (newText) => {
      setText(newText);
      // Auto-detect language when user stops typing (debounced in a real app)
      if (newText.trim().length > 30) {
        try {
          const data = await detectLanguage(newText);
          onLanguageDetected(data.language_code, data.language_name, data.confidence);
        } catch {
          // silent fail for auto-detect
        }
      }
    },
    [onLanguageDetected]
  );

  const handleGenerate = async () => {
    if (!text.trim()) {
      setStatus({ type: "error", message: "Please enter some text or upload a file" });
      return;
    }

    setLoading(true);
    setResult(null);
    setStatus({ type: "loading", message: "Generating speech... This may take a moment." });

    try {
      const data = await synthesize({
        text,
        file: null,
        voice: settings.voice,
        language: settings.language,
        speed: settings.speed,
        style: settings.style,
      });
      setResult(data);
      setStatus({ type: "success", message: `Audio generated successfully in ${data.language_name}` });
    } catch (err) {
      setStatus({
        type: "error",
        message: err.response?.data?.detail || "Generation failed. Check the backend.",
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>EchoScript</h1>
        <p>AI-powered multilingual text-to-speech</p>
      </header>

      <div className="main-grid">
        <div>
          <TextInput
            text={text}
            setText={handleTextChange}
            onLanguageDetected={onLanguageDetected}
            setStatus={setStatus}
          />

          {status && (
            <div className={`status ${status.type}`}>
              {status.type === "loading" && <span className="spinner" />}
              {status.message}
            </div>
          )}

          {result && <AudioOutput result={result} />}
        </div>

        <div>
          <Settings
            settings={settings}
            setSettings={setSettings}
            detectedLang={detectedLang}
          />

          <button
            className="generate-btn"
            onClick={handleGenerate}
            disabled={loading || !text.trim()}
            style={{ marginTop: 16 }}
          >
            {loading ? (
              <>
                <span className="spinner" />
                Generating...
              </>
            ) : (
              "Generate Speech"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
