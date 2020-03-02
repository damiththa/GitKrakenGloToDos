from datetime import timedelta

import commons.helpers.helperVals as helpVals

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
        print (label_dict)
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

def taks_new_dueDate(original_task_dueDate, recurring_task_val):
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
