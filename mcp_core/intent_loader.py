import yaml
import os

def load_intents(registry_path="registry"):
    """
    Load all intent YAML files into a single registry dict
    """
    intents = {}

    for file in os.listdir(registry_path):
        if file.endswith(".yaml"):
            with open(os.path.join(registry_path, file), "r") as f:
                data = yaml.safe_load(f)
                intents.update(data.get("intents", {}))

    return intents
