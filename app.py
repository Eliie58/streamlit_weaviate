# pylint: disable=broad-except
'''
Streamlit Web App
'''
import json
from connection import WeaviateConnection
import streamlit as st

CONNECTION = st.experimental_connection(
    'weaviate', type=WeaviateConnection)


def validate_json(content: str) -> bool:
    """
    Validate json string.

        Parameters
    ----------
    content : str

    Returns
    -------
    bool
        True if json is valid,
        False otherwise.
    """
    try:
        json.loads(content)
        return True
    except json.decoder.JSONDecodeError:
        return False


def layout() -> None:
    """
    Layout streamlit web app
    """
    st.title("Weaviate Streamlit Integration")
    if CONNECTION.is_ready():
        st.write("Connected to Weaviate")
    else:
        st.write("Not Connected to Weavite")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["View Schema 🔭", "Create Schema 🏗️", "Create Data Object ✍", "Query Schema Objects 🧐"])

    with tab1:
        st.header("View Schema")
        schema = CONNECTION.schema().get()
        st.json(schema)

    with tab2:
        st.header("Create a new schema")
        text = st.text_area("Schema Definition", height=200)
        if st.button('Create schema'):
            try:
                CONNECTION.schema().create(json.loads(text))
                st.toast("Schema created succesfully", icon="👏")
            except json.decoder.JSONDecodeError:
                st.toast("Invalid JSON in the schema", icon="🤦")
            except Exception as ex:
                st.toast("Failed creating schema", icon="🤦")

    with tab3:
        st.header("Add new Data Object")
        classes = (cls["class"]
                   for cls in CONNECTION.schema().get()["classes"])
        class_name = st.selectbox(
            "To Which class do you want to add this object?",
            classes
        )
        text = st.text_area("Object Definition", height=200)
        if st.button('Add Object'):
            try:
                if not class_name:
                    st.toast("Please select Object class", icon="🤦")
                if not text:
                    st.toast("Please add Object Definition", icon="🤦")
                uuid = CONNECTION.create(json.loads(text), class_name)
                st.toast(f"Object added with UUID {uuid}", icon="👏")
            except json.decoder.JSONDecodeError:
                st.toast("Invalid JSON in the Object Definition", icon="🤦")
            except Exception as ex:
                print(ex)
                st.toast("Failed adding Object", icon="🤦")

    with tab4:
        st.header("Query Data Objects")
        classes = (cls["class"]
                   for cls in CONNECTION.schema().get()["classes"])
        class_name = st.selectbox(
            "Which class do you want query?",
            classes
        )
        if class_name:
            all_objects = CONNECTION.get_all(class_name=class_name)
            st.json(all_objects)


if __name__ == "__main__":
    layout()
