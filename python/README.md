

# Prepare Python Sample Code


## Environment Variables
```sh
cp ../env.template.rc env.rc
```
edit env.rc and add your ClientId and ClientSecret.


## Create Virtual Environment
```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
source env.rc
```

## Run sample code
```sh
python <file.py>
```


## Deactivate Virtual Environment
```sh
deactivate
```