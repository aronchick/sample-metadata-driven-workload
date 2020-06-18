# Example Machine Learning Experiment

This example machine learning experiment has three steps.

* A processing data step
* A training step
* A packaging step (where a model might be put into a container for rolling out to production)

It requires having a secret in your repo that is base64 encoded credentials to a Gremlin-backed Database. You can create this string by executing the following command:

```
import base64
credentials_unpacked = """
url: "wss://ACCOUNT_NAME.gremlin.cosmos.azure.com:443/"
key: "KEY"
database_name: "DATABASE_NAME"
container_name: "COLLECTION_NAME"
"""
base64_encoded = base64.urlsafe_b64encode(credentials_unpacked.encode("utf-8"))
final_encode_to_utf8 = str(base64_encoded, "utf-8")
```







