
success = {"status_code": 1000, "message": "Success"}
generic_error_1 = {"status_code": 10001, "message": "Invalid request details"}
generic_error_2 = {"status_code": 10002, "message": "Please try again after sometime"}

class Statuses:
    
    credential_type_invalid = {'status_code': 2200301, 'message': "Please select valid credential type"}
    secret_required = {'status_code': 2200302, 'message': "Please enter secret"}
    too_many_login_attempts = {'status_code': 2200303, 'message': "Too many login attempts. Please try again later"}
    password_invalid = {'status_code':2200304, 'message':'Password should contains 8 characters length, uppercase, special character, numeric, lowercase'}
    credential_already_exists = {'status_code': 2200305, 'message': "Credential already exits"}
    multiple_roles_returned = {'status_code': 2200306, 'message': "Multiple Role  present in db"}
    role_not_present_in_db = {'status_code': 2200307, 'message': "Role not present in db"}
    invalid_credential = {'status_code': 2200308, 'message': "Invalid Credential"}
    role_matching_failed = {'status_code': 2200309, 'message': "Role Matching Failed"}
    user_role_not_exsit = {'status_code': 2200310, 'message': "User Role not present"}
    invalid_role_name = {'status_code': 2200311, 'message': "please provide valid role name"}
    invalid_otp = {'status_code': 2200312, 'message': "Invalid OTP"}
    password_not_matching = {'status_code': 2200313, 'message': "Password does not match"}
    parameter_error = {'status_code': 2200313, 'message': "Some parameters might be missing or are in wrong format"}