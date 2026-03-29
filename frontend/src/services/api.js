import axios from "axios";

const API_BASE = "/api";

export async function fetchLanguages() {
  const res = await axios.get(`${API_BASE}/languages`);
  return res.data.languages;
}

export async function detectLanguage(text) {
  const form = new FormData();
  form.append("text", text);
  const res = await axios.post(`${API_BASE}/detect-language`, form);
  return res.data;
}

export async function extractText(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await axios.post(`${API_BASE}/extract-text`, form);
  return res.data;
}

export async function synthesize({ text, file, voice, language, speed, style }) {
  const form = new FormData();
  if (file) form.append("file", file);
  if (text) form.append("text", text);
  form.append("voice", voice);
  form.append("language", language);
  form.append("speed", speed);
  form.append("style", style);

  const res = await axios.post(`${API_BASE}/synthesize`, form);
  return res.data;
}
