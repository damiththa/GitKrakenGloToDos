
# TODO: break this into its own dict in a helperVal for easy edits
# dict holding value (in days) for each recurring task lable
recurring_tasks_dict = {
    'recuring task - 6 MONTHS': 240,
    'recuring task - MONTHLY': 30,
    'recuring task - BI-WEEKLY': 14,
    'recuring task - WEEKLY': 7 ,
    'recuring task - DAILY': 1
}


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
        if label_dict['name'] in recurring_tasks_dict :
            isRecurringTask = True
            break # If there is at least one recurring task label found, break out of the loop also that means this is a recurring task

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
        if label_dict['name'] in recurring_tasks_dict :
            rt_amount = recurring_tasks_dict.get(label_dict['name']) # value of this recurring task
            rt_tup = (rt_amount, label_dict['name'])

            thisTask_recurringTasksLabels_lst.append(rt_tup) # into to the list
    
    # sorting (ascending) list of tuples by the first value of each tuple
    thisTask_recurringTasksLabels_lst.sort()

    return thisTask_recurringTasksLabels_lst[0] # from the list of tuples sorted in ascending order, returning the first tuple