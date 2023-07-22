from datetime import timedelta

PHONE_OTP = "phone_otp"
DEFAULT_USER_ROLE = "customer"
EMAIL_PASSWORD = "email_password"
NOTIF_SERVICE_HEADER = {'Content-Type': 'application/json'}
NOTIF_TYPE_INDICATORS = {"sms": 10, "email": 11, "push_notification": 12}
NOTIF_TEMPLATE_INDICATOR = {"sms": 1, "email": 2}
USER_STATUS = {"active": 1, "inactive": 0}
CREDENTIAL_TYPES = {PHONE_OTP: 0, EMAIL_PASSWORD: 1}
FORGOT_PASSWORD_REQUEST_TYPES = {"generate": 0, "validate": 1, "reset": 2}
EMAIL_PASSWORD_PATTERN = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-])(?!.* ).{8,20}$"
STATUS_ACTIVE = 1
STATUS_INACTIVE = 0 
CREATION_BY = "system"
DEFAULT_ROLE = "customer"