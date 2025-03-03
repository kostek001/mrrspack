import hashlib
import requests
import os
import tomllib

mods_directory = "../../mods"
template_file = "./InertiaAntiCheat_template.toml"
target_file = "../../config/InertiaAntiCheat/InertiaAntiCheat.toml.server"


def getTargetHash(d):
  return hashlib.sha1(d).hexdigest()


hashes = []

# List files in directory
for file in os.listdir(mods_directory):
  path = os.path.join(mods_directory, file)

  # Parse toml file
  if file.endswith(".toml"):
    with open(path, "rb") as f:
      data = tomllib.load(f)

      # Skip when server
      if (data["side"] == "server"):
        print(f"Skipping {data["name"]}")
        continue

      print(f"Parsing {data["name"]}")

      # Download target file to memory
      r = requests.get(data["download"]["url"])

      # Check downloaded file hash
      h = hashlib.new(data["download"]["hash-format"])
      h.update(r.content)
      if (h.hexdigest() != data["download"]["hash"]):
        raise Exception("Hash is not matching!")

      hashes.append(getTargetHash(r.content))

  # Parse jar file
  elif file.endswith(".jar"):
    with open(path, "rb") as f:
      print(f"Parsing {file}")

      hashes.append(getTargetHash(f.read()))

hashes.sort()
groupHash = hashlib.md5("|".join(hashes).encode('utf-8')).hexdigest()
print(f"Group hash: {groupHash}")

# Replace template file
with open(template_file, "r") as f:
  data = f.read()
  with open(target_file, "w") as f:
    f.write(data.replace("{REPLACE_ME}", groupHash))
