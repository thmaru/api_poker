from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="XREiYxq7OSKuOrd7gEAu"
)

result = CLIENT.infer("2.jpg", model_id="playing-cards-ow27d/4")
print(result)