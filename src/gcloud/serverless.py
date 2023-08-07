import os
import subprocess
import yaml
import tempfile
import re

def deployChatbot(chatbot: dict, username: str) -> str:
    '''
        Utility to deploy a given chatbot
        returns a URL string of the deployed resource.
    '''
    with open(f"{os.environ['YAML_DIR']}/services.yaml", "r") as stream:
        try:
            d = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            return e
    name = "a" + username.lower()+chatbot["chatbot_id"]
    d["spec"]["template"]["spec"]["containers"][0]["image"] = os.environ["IMAGE_URL"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][0]["value"] = name
    d["spec"]["template"]["spec"]["containers"][0]["env"][1]["value"] = chatbot["gcs_bucket"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][2]["value"] = chatbot["chatbot_id"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][3]["value"] = os.environ["TEMPERATURE"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][4]["value"] = os.environ["GPT_MODEL"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][5]["value"] = os.environ["TOP_P"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][6]["value"] = os.environ["CHROMA_URL"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][7]["value"] = os.environ["CHROMA_PORT"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][8]["value"] = os.environ["OPENAI_API_KEY"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][9]["value"] = os.environ["FIREBASE_CREDENTIALS"]
    d["metadata"]["name"] = name
    file = open(f"{os.environ['YAML_DIR']}/services_temp.yaml", "w")
    yaml.dump(d, file)
    file.close()
    #print("bp1")
    subprocess.run(["gcloud", "run", "services",
                                 "replace", f"{os.environ['YAML_DIR']}/services_temp.yaml"])
    #print("bp2")
    service = str(d["metadata"]["name"])
    #print("service:", service)
    #print("len svc:", len(service))
    output = subprocess.run(["gcloud", "run", "services", "describe", f"{service}"], capture_output=True).stdout
    #print("bp3")
    output = re.findall("https.*app", str(output))
    subprocess.run(["rm", f"{os.environ['YAML_DIR']}/services_temp.yaml"])
    #print("output:", output)
    output[0] = str(output[0])
    url = output[0].split("\\n")[0]
    return url


def deleteChatbot(service_name: str):
    subprocess.run(["gcloud", "run", "services", "delete", f"a{service_name}", "--quiet"])

