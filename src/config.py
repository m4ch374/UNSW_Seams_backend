port = 40000

'''
<user_test> import <url> as BASE_URL
'''
url = f"http://localhost:{port}/"

# A random 64 byte secret 
TOKEN_SECRET = 'cdb53c23db72f44496625661d2bc417e5f47b0050b7869cd3c00976854ff12e8a6a77cfe3590326fd42a2ce0f2ee14e99f3654fd54c91333b4db51ebbfc8d3a3'

# A random 64 byte secret for encode user's password
PASSWORD_SECRET = 'kfyusre1df6g68serdsf32g185awe961a3621jh4561yt9u4635231sfxg32h1291w65ef6qw8efs3edbhn1sfjs23er8ag4awsz3c2v1aw65we6r48raweyae63rh13'

# Notification types
TAGGED      = "tagged"
MSG_REACTED = "reacted message"
ADDED       = "added to channel/DM"

# for send email
SERVER_EMAIL = "cs1531ant@gmail.com"
SERVER_PASSWORD = 'unsw1531ant'

# size of reset_code
N = 5   # example: AS23F

# expiration of reset_code
EXPIRATION = 60

# Default icon
ICON = url + 'static/icon.jpg'

# Valid react ids
REACT_IDS = [1]
