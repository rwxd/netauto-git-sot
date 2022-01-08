PROJECT_NAME := "python-pip-setup-test"

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Setup required things
	@python3 -m pip install -r requirements.txt
	@python3 -m pip install -r requirements-dev.txt

convert-schemas: ## Convert JSON schemas to other files
	@datamodel-codegen --input schemas/topology.schema.json --input-file-type jsonschema --output eve/models/topology.py
	@datamodel-codegen --input schemas/system.schema.json --input-file-type jsonschema --output eve/models/system.py
	@generate-schema-doc schemas/ docs/schemas/

serve-web: convert-schemas ## Run the web server
	@docker run --rm -v "${PWD}":/usr/local/apache2/htdocs/ -p 8080:80 httpd