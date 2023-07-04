from fulcrum.models.chatbot import Chatbot
import os
import subprocess
import yaml
import tempfile
import re

def deployChatbot(chatbot: Chatbot) -> str:
    '''
        Utility to deploy a given chatbot
        returns a URL string of the deployed resource.
    '''
    with open("services.yaml", "r") as stream:
        try:
            d = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            return e
    d["spec"]["template"]["spec"]["containers"][0]["image"] = os.environ["IMAGE_URL"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][0]["value"] = chatbot["vertex_bucket"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][1]["value"] = chatbot["vertex_url"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][2]["value"] = chatbot["gcs_bucket"]
    d["spec"]["template"]["spec"]["containers"][0]["env"][3]["value"] = chatbot["chatbot_id"]

    file = open("services_temp.yaml", "w")
    yaml.dump(d, file)
    file.close()
    subprocess.run(["gcloud", "run", "services", 
                                 "replace", f"{os.environ['PWD']}/services_temp.yaml"])
    
    service = str(d["metadata"]["name"])
    output = subprocess.run(["gcloud", "run", "services", "describe", f"{service}"], capture_output=True).stdout
    output = re.findall("https.*app", str(output))
    return output[0]

