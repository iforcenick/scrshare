import yaml

masks = {}
with open('mask.yaml', "r") as stream:
    masks = yaml.safe_load(stream) or {}

def set_mask(key: str, mask):
    global masks
    masks[key] = list(mask)
    print(masks)
    with open('mask.yaml', "w") as stream:
        yaml.dump(masks, stream=stream)

def get_mask(key: str) -> list:
    global masks
    if key in masks:
        return masks[key]
    return None