export default function AudioOutput({ result }) {
  if (!result) return null;

  return (
    <div className="card output-section">
      <div className="card-title">
        Output — {result.language_name} ({result.language})
      </div>

      <audio className="audio-player" controls src={result.wav_url} />

      <div className="download-row">
        <a className="download-btn" href={result.wav_url} download>
          Download WAV
        </a>
        <a className="download-btn" href={result.mp3_url} download>
          Download MP3
        </a>
      </div>
    </div>
  );
}
