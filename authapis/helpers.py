

class CustomExceptionHandler(Exception):
    def __init__(self, detail='', status_code=400):
        # Call the base class constructor with the parameters it needs
        super(CustomExceptionHandler, self).__init__(detail)
        self.status_code = status_code
        self.detail = detail


def get_response(status_attribute, data=None):
    if data is None:
        return {'status': status_attribute['status_code'], 'message': status_attribute['message']}
    else:
        return {'status': status_attribute['status_code'], 'message': status_attribute['message'], 'data': data}


def help_text_for_dict(dict_value):
    """_summary_

    Args:
        dict_value (_type_): Dict type

    Returns:
        _type_: String Format help text
    """
    return f'Enter value from this list - {list(dict_value.keys())}'


def common_checking_and_passing_value_from_list_dict(value, list_dict, error_label):
    """
    merged two functions common_dict_checking_and_passing_value, common_list_checking
    """
    if value == "":
        return None
    
    if value:
        if type(list_dict) == list:
            if value not in list_dict:
                raise CustomExceptionHandler(error_label)
            return value
        else:
            if value not in list_dict.keys():
                raise CustomExceptionHandler(error_label)
            return list_dict[value]
    return value
