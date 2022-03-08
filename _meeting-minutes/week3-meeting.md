# Week 3 Meeting Minutes `1/3/2022`

## Attendees

```
• James He
• Henry Wan
• Hanqi Bai
• Ella Huang
```

## **1. Agenda:**

- Assumptions
- Discusses merges and who's going to check/accept them
- Make sure using same variable names
    - Follow specs / Hanqi's
    - Start IDs with 0
    - Datastore method
- Classes or just giant lists (how to structure the list?)

## **2. Disscussion Points:**

### Merge Requests on `GitLab`: 

- Whoever is available can read over and approve/accept them.
- Make sure code is functioning before merging to master
- Push tests to a branch first --> implement code and make sure the branch passes pipeline --> merge to master.

### Assumptions: 

- Not sure if `assumptions.md` is marked
- Add in stuff as we go if there are any issues

### Variable names:

- Whoever first creates a variable let everyone know what they're naming it
- Following Hanqi for the current ones since he's got his ~~shit~~ stuff together the most.
- IDs to start at one
    - Probably going to get messed up anyways when users join/leave
    - Standardised to 1
- Add an extra global permissions ID to the user class
    - Not sure about the purpose/implementation for now but will likely be used more in future iterations
- Using Classes/Lists
    - Keep lists for Users since the functions are already written?
    - Changing to classes wonn't affect the code that is currently implemented much `[Henry]`
    - Having classes and methods will make it a lot easier to reuse snippets of code
    - Final verdict is to switch to classes.
- Testing
    - Not allowed to use `data_store`?
        - ask if our current tests are valid
- Make sure to use issues board
- Standups
    - Asynchronous updates on teams at the end of each week
    - Normal meetings on Tue/Fri should already cover most communications

## **Actions Items:**
- Continue with assigned tasks from Friday 25/2

----

**This meeting minute is authored by `Ella Huang` and translated to `.md` format by `Henry Wan`**