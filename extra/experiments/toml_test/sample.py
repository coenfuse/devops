# requires python3.11 and further
import tomllib
import json

file_path = "../../../config/lamina.toml"
data = tomllib.load(open(file_path, "rb"))
data = json.dumps(data, indent = 4)

out_path = "../../../config/lamina.config.json"
out_file = open(out_path, mode = 'w')
out_file.write(data)
out_file.close()