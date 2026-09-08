# BUILD

```bash
python -m build .

twine upload dist/*0.1.18*   
```
uv run --with build python -m build .
uv tool install twine