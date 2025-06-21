# opgg-llm

pip freeze | xargs pip uninstall -y
pip install -r requirements.txt

"../llama-server.exe" -m "model/Qwen3.gguf" -c 5000 -ngl 99