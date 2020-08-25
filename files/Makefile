.PHONY: test
all: extract transform load

publishers:
	echo "Extracting publishers...."
	python3 ./extract_publishers.py -o ./tmp/

extract:
	echo "Extracting dataservices...."
	python3 ./extract_dataservices.py -o ./tmp/

transform:
	echo "Transforming dataservices...."
	python3 -u ./transform_dataservices.py -o ./tmp/

load:
	echo "Loading dataservices...."
	python3 ./load_dataservices.py -o ./tmp/

remove_loaded:
	echo "Removing loaded dataservices...."
	python3 ./remove_loaded_dataservices.py -o ./tmp/

clean:
	rm ./tmp/*.json
