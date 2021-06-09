.PHONY: test
all: extract transform load

extract:
	echo "Extracting datasets & dataservices...."
	python3 ./extract_datasets.py -o ./tmp/
	python3 ./extract_dataservices.py -o ./tmp/

transform:
	echo "Transforming datasets & dataservices...."
	python3 ./transform_datasets.py -o ./tmp/
	python3 ./transform_dataservices.py -o ./tmp/

load:
	echo "Loading dataservices...."
	python3 ./load_dataservices.py -o ./tmp/

clean:
	rm ./tmp/*.json
