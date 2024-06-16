import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import json
import pandas as pd
from google.cloud.firestore_v1._helpers import DatetimeWithNanoseconds

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def datetime_to_str(o):
    if isinstance(o, DatetimeWithNanoseconds):
        return o.isoformat()
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

def get_all_docs(collection_name):
    print("Collection", collection_name)
    collection_ref = db.collection(collection_name)
    docs = collection_ref.stream()
    
    doc_list = []
    
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id 
        doc_list.append(doc_dict)

    return doc_list

def json_to_excel(data, collection_name):
    df = pd.DataFrame(data)
    df.to_excel(collection_name + ".xlsx", index=False)



if __name__ == "__main__":
    collection_name = "kv3" 
    docs_list = get_all_docs(collection_name)
    json_output = json.dumps(docs_list, default=datetime_to_str)
    json_data = json.loads(json_output)
    json_to_excel(json_data, collection_name)
