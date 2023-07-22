from rest_framework import serializers
from rest_framework.fields import empty
from authapis.helpers import CustomExceptionHandler

class CustomCharField(serializers.CharField,):
    def __init__(self, **kwargs):
        self.store_lower = kwargs.pop('store_lower', True)
        super().__init__(**kwargs)

        self.allow_blank = kwargs.pop('allow_blank', True)
        self.allow_null = kwargs.pop('allow_null', True)

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.

        if not self.required and data in [empty, "", None]:
            return None

        if not getattr(self.root, "partial", False):
            if self.required and data in [empty, "", None]:
                # Handle field if required is True but field is not pass
                # Self.required is pass because field can be required in model file
                raise CustomExceptionHandler({"status_code":122, "message":"Field is required"})

            if data == "" and not self.allow_blank:
                # Handle field if required is True but field is not passed
                raise CustomExceptionHandler({"status_code":123, "message":"Field can not be blank"})

            if not isinstance(data, str):
                raise CustomExceptionHandler(
                    {"status_code":124, "message":"Field should be string type"})
            else:
                data = data.strip().lower() if self.store_lower else data.strip()

        if data != empty and isinstance(data, str):
            data = data.strip().lower() if self.store_lower else data.strip()
        return super().run_validation(data)



class CustomIntegerField(serializers.IntegerField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.allow_null = kwargs.pop('allow_null', True)

    def run_validation(self, data=empty):
        # Test for the empty string here so that it does not get validated,
        # and so that subclasses do not need to handle it explicitly
        # inside the `to_internal_value()` method.

        if not self.required and data in [empty, "", None]:
            return None

        if not getattr(self.root, "partial", False):
            if self.required and data in [empty, "", None]:
                # Handle field if required is True but field is not pass
                # Self.required is pass because field can be required in model file
                raise CustomExceptionHandler({"status_code":122, "message":"Field is required"})

        return super().run_validation(data)

    def to_internal_value(self, value):
        return value