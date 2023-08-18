from configparser import ConfigParser
import pathlib

config = ConfigParser()
config["database"]  = {
    "db_user" : "<your db_user>",
    "db_name" : "<your db_name>",
    "db_password" : "<your db_password>",
    "db_host" : "<your db_host>",
}
config["wazirx"] = {
    "url" : "https://api.wazirx.com/api/v2/tickers"
}
current_path = pathlib.Path(__file__).parent.resolve()
print(current_path)
config_file_name = 'configuration.ini'
with open(f"{current_path}/{config_file_name}",'w') as f:
    config.write(f)