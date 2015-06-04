import random
import string
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "dependencies/rstr"))

from .schemasstore import SchemasStore
import rstr


class DataGenerator(object):
    number_range = [-50, 50]
    string_range = [7, 15]
    array_range = [5, 10]
    not_required_probability = 0.3

    string_charset = string.ascii_letters + string.digits + ' '

    basic_types = ["string", "boolean", "number", "integer"]

    def __init__(self, schemas_store=None):
        self.schemas_store = schemas_store

    def random_value(self, schema):
        if isinstance(schema, str):
            schema = self.get_schema(schema)
        method = getattr(self, "random_%s" % schema["type"])
        return method(schema)

    def get_schema(self, type_name):
        if type_name in self.basic_types:
            return {"type": type_name}
        if self.schemas_store:
            return self.schemas_store.schema(type_name, True)
        return None

    def random_number(self, schema=dict()):
        minimum = schema.get("minimum", self.number_range[0])
        maximum = schema.get("maximum", self.number_range[1])

        if minimum > maximum:
            maximum = minimum
        return random.uniform(minimum, maximum)

    def random_schema(self):
        schema = {"properties": {}, "type": "object"}
        schema["name"] = self.random_string({"pattern": "^[a-zA-Z]{15}$"})

        nb_properties = self.random_integer({"minimum": 1, "maximum": 5})
        for i in range(nb_properties):
            prop_type = random.choice(["number", "boolean", "integer", "string"])

            prop_required = self.random_boolean()
            prop_def = {"type": prop_type, "required": prop_required}

            while True:
                prop_name = self.random_string({"pattern": "[a-zA-Z][a-zA-Z]{1,7}"})
                if prop_name not in schema["properties"]:
                    schema["properties"][prop_name] = prop_def
                    break

        return schema

    def random_integer(self, schema=dict()):
        minimum = schema.get("minimum", self.number_range[0])
        maximum = schema.get("maximum", self.number_range[1])
        divisible_by = schema.get("divisibleBy", 1)

        if schema.get("exclusiveMinimum", False):
            minimum += 1

        if schema.get("exclusiveMaximum", False):
            maximum -= 1

        if divisible_by == 0:
            raise Exception("Can't generate a number divisible by 0")

        if minimum > maximum:
            maximum = minimum
        return random.randint(minimum / abs(divisible_by), maximum /
                              abs(divisible_by)) * divisible_by

    def random_boolean(self, schema=dict()):
        return bool(random.getrandbits(1))

    def random_string(self, schema=dict()):
        # pattern = schema.get("pattern", None)
        if "pattern" in schema:
            return rstr.xeger(schema["pattern"])

        min_length = schema.get("minLength", self.string_range[0])
        max_length = schema.get("maxLength", self.string_range[1])

        if min_length > max_length:
            max_length = min_length
        length = random.randint(min_length, max_length)
        return ''.join(random.choice(self.string_charset) for x in range(length))

    def random_array(self, schema):
        items_type = schema["items"]["type"]
        items_schema = self.get_schema(items_type)
        if not items_schema:
            raise Exception("Don't know how to generate '%s'" % items_type)

        min_items = schema.get("minItems", self.array_range[0])
        max_items = schema.get("maxItems", self.array_range[1])
        if min_items > max_items:
            max_items = min_items

        unique_items = schema.get("uniqueItems", False)

        count = random.randint(min_items, max_items)
        if unique_items:
            max_tries = 100
            res = []
            for x in range(count):
                tries = 0
                while True:
                    obj = self.random_value(items_schema)
                    if obj not in res:
                        break
                    tries += 1
                    if tries > max_tries:
                        raise Exception("Failed to generate the required number of unique items")
                res.append(obj)
            return res
        return [self.random_value(items_schema) for x in range(count)]

    def random_object(self, schema):
        obj = {}

        for prop_name, prop_schema in list(schema.get("properties", []).items()):
            if prop_schema.get("required", False) or random.random() <= self.not_required_probability:
                obj[prop_name] = self.random_value(prop_schema)
        return obj


if __name__ == "__main__":
    pass
