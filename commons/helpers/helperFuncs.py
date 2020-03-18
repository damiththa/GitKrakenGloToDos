import json
import boto3
import os

from datetime import timedelta

import commons.helpers.helperVals as helpVals

DYNAMODB_TABLE_NAME = os.environ['DYNAMODB_TABLE_NAME']

# initializing dynamodb table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def is_recurring_task(lable_dict_lst):
    """
    Checking is this task is a recurring task. 
    A task to be a recurring task, it should contain a pre-defined recurring task labels. 
    
    Arguments:
        lable_dict_lst {list} -- list of dict of labels assigned to this task
    
    Returns:
        bool -- T/F whether this task is a recurring task or not
    """

    isRecurringTask = False # defailt value
    for label_dict in lable_dict_lst:
        # print (label_dict)
        # Ex. --> {'name': 'recuring task - MONTHLY', 'id': '5e1b3155553d4500116e11da'}
        if label_dict['name'] in helpVals.recurring_tasks_dict :
            isRecurringTask = True
            break # If there is at least one recurring task label found, break out of the loop (because we found a recurring task label)

    return isRecurringTask

def getRecurringTask(lable_dict_lst):
    """
    Returns the defined recurring amount value (in days) for the passed in recurring task.
    NOTEME: this also checks if thers are multiple recurring task labels assigned.
    If so, it then checks all assigned recurring task labels and then returns what the label name along with the recurring task amount as a tuple
    
    Arguments:
        lable_dict_lst {list} -- list of dict of labels assigned to this task
    
    Returns:
        [tuple] -- [a tuple of recurring task name and the recurring task amount]
    """
    # Checking (and getting) all assigned recurring task labels assigned to this task
    thisTask_recurringTasksLabels_lst =[] # list to hold tuple of recurring task and the recurring task amount

    for label_dict in lable_dict_lst:
        if label_dict['name'] in helpVals.recurring_tasks_dict :
            rt_amount = helpVals.recurring_tasks_dict.get(label_dict['name']) # value of this recurring task
            rt_tup = (rt_amount, label_dict['name'])

            thisTask_recurringTasksLabels_lst.append(rt_tup) # into to the list
    
    # sorting (ascending) list of tuples by the first value of each tuple
    thisTask_recurringTasksLabels_lst.sort()

    return thisTask_recurringTasksLabels_lst[0] # from the list of tuples sorted in ascending order, returning the first tuple

def task_new_dueDate(original_task_dueDate, recurring_task_val):
    """Returns the due date for the task.
    This function sets the due date according to the passed in recurring task value. 

    Arguments:
        original_task_dueDate {datetime} -- Original task due date. NOTEME: If not defined TODAY is passed in as original due date        
        recurring_task_val {int} -- Number of days to add to original due date 
    
    Returns:
        [datetime] -- [new due date date/time]
    """

    new_dueDate = original_task_dueDate + timedelta(days=recurring_task_val)

    return new_dueDate

def db_entry_formatter(item1, item2):
    """Takes in items and returns concatination of those items in the format that is defined in dynamodb
    
    Arguments:
        item1 {string} -- Item 1
        item2 {string} -- Item 2 
    
    Returns:
        [string] -- [Concatinated new item]
    """

    return item1+'#'+item2


def cardinfo_intoDB(cardID, boardID, columnID):
    """Adds new card into database
    
    Arguments:
        cardID {string} -- Id of the card
        boardID {string} -- Id of the board
        columnID {string} -- Id of the column
    
    Returns:
        [integer] -- [Returns the status response gets back from dynamodb for the operation]
    """

    board_card_Id = db_entry_formatter(boardID, cardID)
    card_column_Id = db_entry_formatter(cardID, columnID)

    # into dynamodb table
    res = table.put_item(
        Item = {
            'Board#Card': board_card_Id,
            'Card#Column': card_column_Id
        }
    )

    return res['ResponseMetadata']['HTTPStatusCode']

def cardInfo_deleteFromDB(cardID, boardID):
    """Deletes the card from the database
    
    Arguments:
        cardID {string} -- Id of the card
        boardID {string} -- Id of the board
    
    Returns:
        [integer] -- [Returns the status response gets back from dynamodb for the operation]
    """

    board_card_Id = db_entry_formatter(boardID, cardID)

    # delete from dynamodb table
    res = table.delete_item(
        Key = {
            'Board#Card': board_card_Id
        }
    )

    return res['ResponseMetadata']['HTTPStatusCode']

def cardInfo_updateDB(cardID, boardID, columnID, card_position):
    """Updates the entry in the database
    
    Arguments:
        cardID {string} -- Id of the card
        boardID {string} -- Id of the board
        columnID {string} -- Id of the column
        card_position {integer} -- Card position in the column
    """

    board_card_Id = db_entry_formatter(boardID, cardID) 
    card_column_Id = db_entry_formatter(cardID, columnID)

    # updating an entry into dynamodb
    table.update_item(
        Key = {
            'Board#Card': board_card_Id
        },
        UpdateExpression = 'SET #colName = :colValue, #colName2 = :colValue2',
        ExpressionAttributeNames = {
            '#colName': 'Card#Column',
            '#colName2': 'card_position'
        },
        ExpressionAttributeValues = {
            ':colValue' : card_column_Id,
            ':colValue2' : card_position
        },
        ReturnValues="UPDATED_NEW"
    )

def cardInfo_getFromDB(cardID, boardID):
    """Retrives the card info from table
    
    Arguments:
        cardID {string} -- Id of the card
        boardID {string} -- Id of the board
    
    Returns:
        integer -- [Returns the status response gets back from dynamodb for the operation]
    """

    board_card_Id = db_entry_formatter(boardID, cardID)

    # getting that updated item
    res = table.get_item(
        Key = {
            'Board#Card': board_card_Id
        }
    )

    return res['Item']

    # return res['ResponseMetadata']['HTTPStatusCode']
