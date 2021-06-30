# Auto update all pip packages
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip install -U

# upd requirements
pip install -r requirements.txt

# pyenv
pyenv virtualenv <py version> <virtualenv name>