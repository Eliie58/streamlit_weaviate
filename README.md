# Streamlit Weaviate Demo App

Demo Streamlit Connection to Weaviate

### Usage

To use the WeaviateConnection

```
import streamlit as st

connection = st.experimental_connection('weaviate', type=WeaviateConnection)
```

Connection parameters are stored in the secrets.toml file of streamlit.
<br>
Example file for local deployment of weaviate without authentication:

```
[connections.weaviate]
url = "http://localhost:8080"
```

### Create Schema

```
json_schema = {
    "classes": [{
        "class": "Publication",
        "description": "A publication with an online source",
        "properties": [
            {
                "dataType": [
                "text"
                ],
                "description": "Name of the publication",
                "name": "name"
            },
            {
                "dataType": [
                "Article"
                ],
                "description": "The articles this publication has",
                "name": "hasArticles"
            }
        ]
    }]
}
connection.schema().create(json_schema)
```

### Query Schema

```
connection.schema().get()
```

### Create Object

```
data_obj = {
    "name" : "Nature"
}

uuid = connection.create(data_obj, "Publication")
```

### Get Objects

```
connection.data_object().get(class_name="Publication")
```

### Other functionality

For all other functionalities, you can use the client() method to get the underlying weaviate Client.
