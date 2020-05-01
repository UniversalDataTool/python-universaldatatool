# e.g. image_url -> imageUrl
def camelify(s):
    s = list(s)
    indices_with_underscore = [i for i, ltr in enumerate(s) if ltr == "_"]
    for i in indices_with_underscore:
        if i + 1 < len(s):
            s[i+1] = s[i+1].upper()
    return "".join([c for c in s if c != "_"])

def camelify_dict(d):
    new_dict = {}
    for (k,v) in d.items():
        new_dict[camelify(k)] = v
    return new_dict

if __name__ == "__main__":
    print("image_url", camelify("image_url"))
    print("some_long_word", camelify("some_long_word"))
    print("""{ "interface_type": "image_segmentation" }""", camelify_dict({ "interface_type": "image_segmentation" }))
