# Bootstrap Instructions

You are starting for the first time. Execute these steps in order before doing anything else.

---

## Step 1: Verify configuration

Check that the following environment variables are present and non-empty:
- `DASHSCOPE_API_KEY`
- `DASHSCOPE_REGION`

If either is missing, send a Telegram message:
> "⚠️ Qwen Image Generator could not start. Missing configuration: [list missing vars]. Please reconfigure in the settings panel."

Then stop.

---

## Step 2: Resolve the base URL

Map `DASHSCOPE_REGION` to the correct endpoint:
- `singapore` → `https://dashscope-intl.aliyuncs.com`
- `virginia` → `https://dashscope-us.aliyuncs.com`
- any other value → treat as `singapore` and log a warning

---

## Step 3: Test API credentials

Send a minimal API request to verify the key is valid:

```
GET <base_url>/api/v1/tasks/bootstrap-check
Authorization: Bearer $DASHSCOPE_API_KEY
```

(A 404 response is acceptable — it means the endpoint is reachable and the key was accepted. A 401 means the key is invalid.)

If you receive a 401 or network error, send a Telegram message:
> "⚠️ Qwen Image Generator could not authenticate with DashScope. Please check your API Key in the settings panel."

Then stop.

---

## Step 4: Initialise template storage

Check if `templates.json` exists in the workspace. If it does not exist, create it with an empty object:

```json
{}
```

---

## Step 5: Announce readiness

Send a Telegram message:
> "✅ Qwen Image Generator is ready.
>
> Send me a description of the image you want to create, or use /generate <prompt>.
> Send /help to see all available commands."

---

## Step 6: Enter normal operation

Begin listening for Telegram messages. Apply the behaviour described in Agent.md.
