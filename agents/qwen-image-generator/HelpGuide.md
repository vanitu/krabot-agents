# Qwen Image Generator — Help Guide

## Telegram Commands

| Command | Description |
|---------|-------------|
| `/generate <prompt>` | Start an image generation request (you will be asked to confirm before it runs) |
| `/templates` | List all your saved prompt templates |
| `/use_template <name>` | Load a saved template and start a generation request |
| `/save_template` | Save the last prompt you used as a named template |
| `/status` | Show the result of the last generation job |
| `/help` | Show this list of commands |

## Generating an Image

Send `/generate` followed by your description, or just type your description as a plain message:

```
/generate a samurai standing in heavy rain, neon city background, cinematic
```

The agent will reply with a summary of what it is about to generate, including the image size and model. Reply **yes** (or **ok**, **confirm**) to start the job. Reply anything else to cancel.

## Using Image Size Options

You can override the default image size inline:

```
/generate a wide mountain panorama --size 16:9
/generate a tall portrait of a knight --size 3:4
/generate a square logo concept --size 1:1
```

Accepted size shortcuts: `1:1` (1280×1280), `3:4` (1104×1472), `4:3` (1472×1104), `16:9` (1696×960), `9:16` (960×1696).

## Generating Multiple Images

Add `--n 2` (or up to 4) to get several variations at once:

```
/generate a futuristic city skyline --n 3
```

## Saving a Prompt as a Template

After a successful generation, send:

```
/save_template
```

The agent will show you a summary of the prompt and settings used and ask you to give the template a name. Confirm with **yes** to save.

You can also trigger this mid-conversation if you have just described a prompt you want to reuse.

## Using a Saved Template

```
/templates
```

Lists all saved templates with short previews. Then:

```
/use_template landscape portrait
```

Loads the template and goes through the normal confirmation flow before generating.

## Troubleshooting

**"Content moderation error"** — the prompt contains restricted content. Rephrase and try again.

**"API authentication failed"** — your DashScope API key may have expired or been revoked. Reconfigure in the settings panel.

**Generation takes longer than 3 minutes** — the API is under heavy load. The agent will keep polling and send the result when it arrives.
