# Week 4 Meeting Minutes `12/3/2022`

## Attendees

```
• James He
• Henry Wan
• Hanqi Bai
• Ella Huang
```

## **1. Agenda:**

- Discuss feedback fixes
- How to split `iteration 2` tasks
- Standup posts
- Any methods you add to class definitions PLEASE let others know so we don’t waste time repeating code

## **2. Discussion points:**

### Feedback fixes:

- Going to be completed in the next two days
- Code:
    - Split function tests into different files
    - Add more commenting + change test names to be more intuitive (channels_list + auth tests)
- Management:
    - Make standups official
    - Keep merge requests descriptive
- Splitting `iteration 2` workload:
    - Everyone carries over functinos from `iteration 1`
    - `iteration 2` functions to be split as:  
        - `Messages`
        > •	message/send/v1  
        > •	message/edit/v1  
        > •	message/remove/v1  
        > •	dm/messages/v1  
        > •	message/senddm/v1  

        - `Users`
        > •	users/all/v1  
        > •	user/profile/v1  
        > •	user/profile/setname/v1  
        > •	user/profile/setemail/v1  
        > •	user/profile/sethandle/v1  

        - `dm`
        > •	dm/create/v1  
        > •	dm/list/v1  
        > •	dm/remove/v1  
        > •	dm/details/v1  
        > •	dm/leave/v1  

        - `channel` & `admin`
        > •	channel/leave/v1  
        > •	channel/addowner/v1  
        > •	channel/removeowner/v1  
        > •	admin/user/remove/v1  
        > •	admin/userpermission/change/v1  

    - Ella to do message functions
        - May require a new message class?
    - Others to be decided later(Tuesday)
    - Auth/logout/v1 requires W5 lectures, also TBD
- Standup posts to b made on Saturday / Tuesday evening, everyone to give a short update on their progress in teams before the next standup post is made.
-	Henry may be unavailable first days of W6 due to international travel
- Finish wrapping v2 functions by Tuesday (15/3) and be prepared to start on new functions
- If you are implementing new methods under a certain class please let others know through a standup/discord post so we don’t end up writing double the code.

### Actions Items:

- Everyone: Complete v2 functions for iteration 2
- Everyone: Implement feedback fixes

----

**This meeting minute is authored by `Ella Huang` and translated to `.md` format by `Henry Wan`**
