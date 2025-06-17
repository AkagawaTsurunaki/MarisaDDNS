# Marisa DDNS

A very simple Python script for the free DDNS provider [dynv6](https://ipv4.dynv6.com).

Run the following commands if you are using Anaconda environment manager.
```
conda create --name marisa-ddns python=3.10 --yes
conda activate marisa-ddns
pip install -r requirements.txt
python ddns.py
```

Please edit `config.yaml` after you first run the `ddns.py`.