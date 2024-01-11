# hdx-pyutils

A python package containing utility functions.

## Install Library
```bash
pip install git+https://github.com/hashdex/hdx-pyutils.git
```

## Local development

```bash
pipenv shell
pipenv install '-e .'
```

Important: Whenever adding a new package add it to setup.py and run the command above, setup.py is the source of truth for the required packages. (If it's a devpackage it can be added directly to Pipfile)
## Features

### Built-in packages

This package comes with the following *must-have* packages:

- requests
- pandas
- numpy
- boto3
- pyathena
- s3fs
- openpyxl

You can use them normally as indicated below:

```python
import pandas as pd
```

### Utility Classes

- [SecretsManager](#secretsmanager)
  
- [DatalakeManager](#datalakemanager)

- [S3Manager](#s3manager)

- [DynamodbManager](#dynamodbmanager)

- [LambdaManager](#lambdamanager)
  
- [InoaApiManager](#inoaapimanager)

### SecretsManager

```python
import hdxpyutils

sm = hdxpyutils.SecretsManager()
secret = sm.get_secret('my-secret-name')

value = secret['value']
value2 = secret['value2']
```

### DatalakeManager

```python
import hdxpyutils

dm = hdxpyutils.DatalakeManager(
    key=secret['key'], 
    secret=secret['secret'], 
    s3_staging_dir='s3://bucket-name/data/staging-dir/'
)

data = dm.query('SELECT * FROM "database_name"."table_name" limit 10')
```

### S3Manager

```python
import hdxpyutils

s3m = hdxpyutils.S3Manager()

# Save data in s3.
s3m.save_to_s3('my-bucket', data='id,name\r\nmyid,hello', path='hello.csv') 

# Save pandas dataframe in s3 as CSV.
s3m.save_df_to_s3('my-bucket', df, path='data.csv')

# Check if a file exists.
s3m.file_exists('my-bucket', path='data.csv')

# List files
s3m.list_files('my-bucket', prefix='data/testing/')

# Read CSV file as pandas dataframe
df = s3m.read_csv('my-bucket', path='data.csv')

# Get Excel file
excel_file = s3m.read_excel('my-bucket', path='data/file.xlsx')

# Read excel sheet as pandas dataframe
df = s3m.read_excel_sheet('my-bucket', path='file.xlsx', sheet_name='Test', skip_header=5, usecols='A:F')

# Read JSON file.
data = s3m.read_json('my-bucket', path='data.json')

# Upload file
s3m.upload_file('my-bucket', filepath='./documents/file.xlsx', path='data/target/file.xlsx')
```

### DynamodbManager

```python
import hdxpyutils

ddbm = hdxpyutils.DynamodbManager()

# PartiQL generic query.
data = ddbm.pql_query(pql_string='SELECT * FROM "table_name";')

# Insert item in table
ddbm.put_item('table_name', item={'id': 'myitem', 'name': 'Test Item'})

# Get item in table
obj = ddbm.get_item('table_name', keys={'id': 'myitem'})

# Delete item in table
ddbm.delete_item('table_name', keys={'id': 'myitem'})
```

### LambdaManager
```python
import hdxpyutils

lm = hdxpyutils.LambdaManager()

result = lm.invoke('function-name', { 'my-param': 'my-value' })
```



### InoaApiManager

```python
import hdxpyutils

iam = hdxpyutils.InoaApiManager(
    api_url=secret['inoa_url'],
    username=secret['username'], 
    password=secret['password']
)

# Inoa query.
data = iam.call(module='funds', method='get_funds', params={})
```

