# Week 7 Meeting Minutes `1/4//2022`

## Attendees

```
• James He
• Henry Wan
• Hanqi Bai
• Ella Huang
```

## **1. Agenda:**
- Discuss `Iteration 3`

## **2. Discussion points:**

### Current Progress
- New json persistence method
    - Done by Henry
    - Converts datastore b/w json and objects
    - Had to use local import in datastore to avoid circular import error
    - All black box, shouldn’t affect current functions (thank you Henry)
- Notifications class
    - Done by Hanqi/Henry
    - Work in progress but the class has been set up 
- Emails
    - Done by Hanqi
    - Is setup, server uses its own email to send password reset emails to users

### Issues/Questions
- Notifications
    - Needs to be completed last after message/ functions (i.e. message pin)
    - May be difficult to test, will require in depth planning to test exhaustively.
    - User/stats/v1
    - Not sure why channel_joined returned a list of dictionaries with num_user_channels as a key
    - Will ask on Ed for clarification
- User password reset
    - Requires all current user tokens to be removed from datastore
- Auth/ domain tests from iter 2
    - Some issues with tests for changing the permission of a user who already has the same permission/is the last channel owner not raising inputerror.
    - May be because of using wrong channel permission codes (1 and 2, not 0 and 1)

### Iteration 3 workload
- Funtion splits as follows:

James & Henry:
```
notifications/get/v1
message/share/v1
message/react/v1
message/unreact/v1
message/pin/v1
message/unpin/v1
```

Hanqi:
```
search/v1
auth/passwordreset/request/v1 
auth/passwordreset/reset/v1 
user/profile/uploadphoto/v1 
user/stats/v1 
users/stats/v1
```

Ella:
```
message/sendlater/v1
message/sendlaterdm/v1
standup/start/v1
standup/active/v1
standup/send/v1
```

- James/Henry sharing notifications/message routes
- Hanqi may help Ella (ty king) as he’s done most of his new routes already (absolute god)

## **3. Actions Items**
- Finish fixing Iter2 bugs (by next meeting)
- Work on finding interviewees to collect data for ‘iteration 4’ (by next meeting)
- Code up tests + implement new routes (flexible, keep on track to finish by Iter3 due date)
- Set up git issues board for iter 3

----

This meeting minute is translated to `.md` file by `Henry Wan` and authored by `Ella Huang`
