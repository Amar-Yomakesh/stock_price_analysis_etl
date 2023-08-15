export AIRFLOW_HOME
SOURCE_DIR=$(pwd)

if [ -z "$AIRFLOW_HOME" ]; then
    echo "Error: airflow home not setEnvironment variable not set."
    exit 1
fi

# Define the source directory (current working directory)
SOURCE_DIR=$(pwd)

# Define the destination directory using the environment variable
DEST_DIR="$AIRFLOW_HOME"

# Check if the destination directory exists
if [ ! -d "$DEST_DIR" ]; then
    echo "Error: Destination directory does not exist."
    exit 1
fi

# Copy files from the source directory to the destination directory
cp -r "$SOURCE_DIR"/dags/* "$DEST_DIR"/dags/

echo "Dag files copied successfully from '$SOURCE_DIR' to '$DEST_DIR'."

cp ../data/crypto_price_etl.py "$DEST_DIR"/dags/scripts/
