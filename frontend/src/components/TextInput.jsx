import { useState } from "react";
import { extractText } from "../services/api";

export default function TextInput({ text, setText, onLanguageDetected, setStatus }) {
  const [fileName, setFileName] = useState("");

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setFileName(file.name);
    setStatus({ type: "loading", message: "Extracting text from file..." });

    try {
      const data = await extractText(file);
      setText(data.text);
      onLanguageDetected(data.language_code, data.language_name, data.confidence);
      setStatus({ type: "success", message: `Extracted ${data.text.split(/\s+/).length} words from ${file.name}` });
    } catch (err) {
      setStatus({ type: "error", message: err.response?.data?.detail || "Failed to extract text" });
    }
  };

  return (
    <div className="card">
      <div className="card-title">Input</div>

      <textarea
        className="text-input"
        placeholder="Type or paste your text here..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <div className="divider">or upload a file</div>

      <div className="file-upload">
        <input
          type="file"
          accept=".pdf,.docx,.doc,.png,.jpg,.jpeg,.bmp,.tiff,.tif,.webp,.txt"
          onChange={handleFileChange}
        />
        <div className="file-upload-label">
          <strong>Click to upload</strong> or drag and drop
          <br />
          PDF, DOCX, Image, or Text file
        </div>
        {fileName && <div className="file-name">{fileName}</div>}
      </div>
    </div>
  );
}
