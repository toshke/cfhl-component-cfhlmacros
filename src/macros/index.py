import json

import methods
i = 0
def traverse(obj, parameters, function):
    global i
    print(f"traverse {i}")
    print('value=' + json.dumps(obj))
    i = i +1
    is_dict = isinstance(obj, dict)
    is_list = isinstance(obj, list)
    print(f"list={is_list} dict={is_dict}")
    if not (is_dict or is_list):
        return function(obj, parameters)
    itix = -1
    for it in obj:
        if is_dict:
            value = obj[it]
        else:
            itix = itix + 1
            value = it
        print(value)
        if isinstance(value, dict):
            print(f"traverse for {it}")
            traverse(value, parameters, function)

        elif isinstance(value, list):
            print(f"traverse for {it} as list")
            traverse(value, parameters, function)

        elif isinstance(value, (float, int, str)):
            if is_dict:
                obj[it] = function(value, parameters)
            else:
                print(f"Process list el {value}")

                obj[itix] = function(value, parameters)


def lambda_handler(event, context):
    print(json.dumps(event))
    template = event['fragment']
    parameters = event['templateParameterValues']

    traverse(template, parameters, methods.replace_network)

    return {
        'requestId': event['requestId'],
        'fragment': template,
        'status':'SUCCESS'
    }
