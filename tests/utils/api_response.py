import allure
from requests import Response
from jsonschema import ValidationError, validate


class APIResponse:
    def __init__(self, response: Response):
        self.response = response

    def status_code_should_be_eq(self, expected_status):
        assert (
            self.response.status_code == expected_status
        ), f"Ожидали {expected_status}, но получили {self.response.status_code}"
        return self

    def len_of_json_should_be_eq(self, expected_len):
        assert (
            len(self.response.json()) == expected_len
        ), f"Ожидали {expected_len}, но получили {len(self.response.json())}"
        return self

    def json_should_be_eq(self, expected_json):
        try:
            response_json = self.response.json()
        except ValueError:
            raise AssertionError("Это не Json формат")

        assert (
            response_json == expected_json
        ), f"Ожидали Json {expected_json}, Но получили {response_json}"
        return self

    def response_without_fields(self, *fields):
        return {k: v for k, v in self.response.json().items() if k not in fields}

    @allure.step("Валидируем схему")
    def schema_should_be_eq(self, expected_schema):
        try:
            response_json = self.response.json()
        except ValueError:
            raise AssertionError("Это не Json формат")

        try:
            validate(instance=response_json, schema=expected_schema)
        except ValidationError as e:
            raise AssertionError(f"Ошибка валидации схемы: {e}")

        return self

    def len_of_values_with_key(self, key_name):
        self._current_value = len(self.response.json()[key_name])
        return self

    def type_of_value_with_key(self, key_name):
        self._current_value = type(self.response.json()[key_name])
        return self

    def value_with_key(self, key_name):
        self._current_value = self.response.json()[key_name]
        return self

    def get_value_with_key(self, key_name):
        return self.response.json()[key_name]

    def should_be_eq(self, expected_value):
        assert (
            self._current_value == expected_value
        ), f"Ожидали {expected_value}, но получили {self._current_value}"
        return self