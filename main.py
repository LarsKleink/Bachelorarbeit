# main file
import toml

with open('config.toml', 'r') as f:
    config = toml.load(f)

for x in range(config["algorithms"]["count_a"]):
    print(config["algorithms"][str(x)])