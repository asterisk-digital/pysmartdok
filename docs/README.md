# docs/

The SmartDok OpenAPI JSON is published at <https://api.smartdok.no/docs/v1>.

It is **not** vendored into this repo — it's a third-party document that goes stale quickly and would bloat the repo (~500 KB). Save it locally into this folder when implementing a new endpoint or reviewing an existing model. The rest of `docs/` is gitignored; only this README is tracked.

```bash
curl https://api.smartdok.no/docs/v1 -o docs/swagger.json
```
