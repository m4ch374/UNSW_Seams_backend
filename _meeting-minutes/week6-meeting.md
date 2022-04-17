# Week 6 Meeting Minutes `25/3/2022`

## Attendees

```
• James He
• Henry Wan
• Hanqi Bai
• Ella Huang
```

## **1. Agenda:**
- Any coverage issues
- When/how to run group testing
- Issue with removing items from datastore and generating new ids

## **2. Discussion points:**

### Coverage
- No big issues, everyone covers their own functions
- Can remove valid user checks that were in iteration 1 since it’s now covered by tokens implementation
- Make sure debug mode is false

### Group testing of frontend
- Sunday 6:30pm

### Issue with removing items from datastore and generating new ids
- Remove user functionality is specified in the spec
- Remove message just moves the message into an inaccessible channel so its place in the backend is kept but it is removed from the frontend
- Remove dms will delete the entire dm from datastore
    - Changing how ids are generated to accommodate this (no longer based on length of datastore)

### Auth.py functions
- Should comment out old iteration1 code or move code to a different file
- Commenting out may affect style
- Will change function names back to v1 for consistency with other domains

### Global/local owner permissions
- All functions which require permissions will have their own checks for both global/local ownership

## **3. Actions items:**
`Null`

----

This meeting minute is translated to `.md` file by `Henry Wan` and authored by `Ella Huang`
