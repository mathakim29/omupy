<div align="center">
  <h3> 
    Retrieval Voice Cloning API 
  </h3>
</div>

----
- the idea of cloning and mimicking voices are cool.
- but so far i didnt find a stable working one that's api based
- There's w-okada, but the setup is complicated and i want something simple
- so i spent hours making one.
- the engine is pretty barebones, but would be useful for future project purposes




## Requirements

<table>
  <tr>
    <td>uv</td>
    <td>python 3.10+</td>
    <td>a very good nvidia rtx card (optional, but recommended)</td>
  </tr>
</table>

## How to use it

1. Clone this repo 
2. Run this 
```bash
uv run rvc-api
```

> **NOTE:** All configs are in the .env file, they are included intentionally for demo purposes.

- `API_PORT` controls the API port. `RVC_MODELS_DIR` controls where uploaded
models are stored.

- By default, the API is available at <http://127.0.0.1:8000>.

- Set `API_PORT` to change the port used by the app. Set `RVC_MODELS_DIR` to
change where models are stored. The default model directory is
`~/.local/rvc_app`.

## API

### Upload a model

```bash
curl -X POST http://127.0.0.1:8000/models \
  -F "file=@my-model.zip"
```

- The zip must contain a `.pth` file. An optional `.index` file is used during
conversion.

### List models

```bash
curl http://127.0.0.1:8000/models
```

### Convert audio

```bash
curl -X POST http://127.0.0.1:8000/convert \
  -F "audio=@input.wav" \
  -F "model=my-model" \
  -F "pitch=0" \
  -F "f0method=rmvpe" \
  --output output.wav
```

The `/convert` endpoint accepts these form fields:

| Field | Required | Default | Description |
| --- | --- | --- | --- |
| `audio` | Yes | — | Input audio file. |
| `model` | Yes | — | Name of a model uploaded through `/models`. |
| `pitch` | No | `0` | Pitch shift in semitones. Use `12` for one octave up or `-12` for one octave down. |
| `f0method` | No | `rmvpe` | Pitch extraction method. `rmvpe` is the recommended default. |
| `index_rate` | No | `0.7` | How strongly the model index influences the result. Higher values can sound more like the trained voice. |
| `protect` | No | `0.33` | Protects consonants and unvoiced sounds. Increase it if speech becomes unclear. |
| `hop_length` | No | `128` | Pitch-tracking window step. Leave at the default unless you know you need to tune it. |
| `rms_mix_rate` | No | `0.25` | Mixes the input volume envelope into the output. Higher values preserve more of the original volume changes. |

For a basic conversion, only `audio` and `model` are required. The other
fields can be adjusted when experimenting with quality, pitch, or clarity.

- The API is built on FastAPI, so internal docs are auto-generated.
- Interactive API docs (based on Swagger) are available at <http://127.0.0.1:8000/docs>.

## Demo audio
<audio controls src="./demo.wav">
  Your browser does not support audio playback. [Download demo.wav](./demo.wav)
</audio>

## Live audio

`src/live.py` also contains an experimental microphone-to-speaker conversion
loop. 
However please note to self, it's barely tested and only there as proof of concept. 
