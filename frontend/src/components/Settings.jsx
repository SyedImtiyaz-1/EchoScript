import { useEffect, useState } from "react";
import { fetchLanguages } from "../services/api";

function RadioGroup({ options, value, onChange }) {
  return (
    <div className="radio-group">
      {options.map((opt) => (
        <button
          key={opt.value}
          className={`radio-btn ${value === opt.value ? "active" : ""}`}
          onClick={() => onChange(opt.value)}
          type="button"
        >
          {opt.label}
        </button>
      ))}
    </div>
  );
}

export default function Settings({ settings, setSettings, detectedLang }) {
  const [languages, setLanguages] = useState({});

  useEffect(() => {
    fetchLanguages().then(setLanguages).catch(() => {});
  }, []);

  const update = (key, val) => setSettings((prev) => ({ ...prev, [key]: val }));

  return (
    <div className="card">
      <div className="card-title">Settings</div>

      <div className="settings-group">
        <div className="settings-label">Voice</div>
        <RadioGroup
          options={[
            { value: "male", label: "Male" },
            { value: "female", label: "Female" },
          ]}
          value={settings.voice}
          onChange={(v) => update("voice", v)}
        />
      </div>

      <div className="settings-group">
        <div className="settings-label">
          Language
          {detectedLang.code && (
            <span style={{ fontWeight: 400, color: "#7c3aed", marginLeft: 8 }}>
              Detected: {detectedLang.name} ({Math.round(detectedLang.confidence * 100)}%)
            </span>
          )}
        </div>
        <select
          className="settings-select"
          value={settings.language}
          onChange={(e) => update("language", e.target.value)}
        >
          <option value="auto">Auto-detect</option>
          {Object.entries(languages).map(([code, name]) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>
      </div>

      <div className="settings-group">
        <div className="settings-label">Speed</div>
        <RadioGroup
          options={[
            { value: "slow", label: "Slow" },
            { value: "normal", label: "Normal" },
            { value: "fast", label: "Fast" },
          ]}
          value={settings.speed}
          onChange={(v) => update("speed", v)}
        />
      </div>

      <div className="settings-group">
        <div className="settings-label">Style</div>
        <RadioGroup
          options={[
            { value: "neutral", label: "Neutral" },
            { value: "expressive", label: "Expressive" },
            { value: "calm", label: "Calm" },
          ]}
          value={settings.style}
          onChange={(v) => update("style", v)}
        />
      </div>
    </div>
  );
}
