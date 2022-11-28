# CAMP

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 13.3.2.

## Frontend (angular):
install the prerequisites packages
```python
...\CAMP-PROJECT\frontend> npm install
```
start UI
```python
...\CAMP-PROJECT\frontend> npm start
http://localhost:4200/model
```
## Backend 

```python
...\CAMP-PROJECT\backend>python app-kcamp.py start
```

### Model:
backend > input
 * Country and Global folders contain CEDS database

backend > models
`model-file-camp-sankey.xlsx`
 * this excel was created to be used by the user to enter inputs (manual run)
 * now, app sheet is added to be used by the UI

backend
`SankeyScript.py`
 * user inputs send to this python to generate output files

backend > output
 * after run `python SankeyScript.py`, the system will generate results in this folder
 
