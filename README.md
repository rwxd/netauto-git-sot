# Git as Source of Truth for network automation

![structure](out/docs/structure/name%20Git%20as%20Source%20of%20Truth.png)

## JSON Schema

### Convert Schema to Python Model

```bash
datamodel-codegen --input schemas/device.schema.json --input-file-type jsonschema --output generator/models/device_configuration.py
```
