
# Foreword

The reason all of these commands start capitalized (against how bad it looks) is because of auto-caps in phones, so I figured rather than fighting the system, I would just use it

# Commands

## Get future
`Get future` will return **all** things that have been stored and are still to come

## Get past
`Get past` will return **all** things that have been stored and whose date has passed

## Get current
`Get current` will return all things within the `range` parameter

## Get all
`Get all` will return **all** things that have been stored

## Get range {x}
`Get range {x}` will return all things between now and {x}

## Delete all
`Delete all` will delete **all** items in the database (even if they are in the future)

## Delete past
`Delete past` will delete all items that have already happened.

## Reset {day}
`Reset {day}` will remove all items from a given day, using the same date parsing as that that was used for setting up reminders

# Parameters

Set with the following structure:
```
Set parameter value
i.e.
Set range 5
```

range: how far in advance to remind about things, in days
delete: delete items that are passed


# Sample Text Message

```
Module 4 HW
10/4/20
```
