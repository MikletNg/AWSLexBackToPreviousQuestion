import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

INTENT_NAME = 'testIntent'


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit,
                message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def elicit_slot_with_response_card(session_attributes, intent_name, slots,
                                   slot_to_elicit, message, response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message,
            'responseCard': response_card
        }
    }


def message(content):
    return {'contentType': 'PlainText', 'content': content}


def confirm_intent(session_attributes, intent_name, slots, message,
                   response_card):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message,
            'responseCard': response_card
        }
    }


def build_response_card(title, subtitle, buttons):
    return {
        'contentType':
        'application/vnd.amazonaws.card.generic',
        'version':
        1,
        'genericAttachments': [{
            'title': title,
            'subTitle': subtitle,
            'buttons': buttons
        }]
    }


def build_buttons(options):
    buttons = []
    for i in options:
        if i is None:
            button = {'text': 'No option', 'value': 'No option'}
        else:
            button = {'text': i, 'value': i}
        buttons.append(button)
    return buttons


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': fulfillment_state,
            'message': message
        }
    }
    return response


def dispatch(intent_request):
    intent_name = intent_request['currentIntent']['name']
    # Match the intent name right or not
    if intent_name == INTENT_NAME:
        return wecarebill(intent_request)
    raise Exception('Intent with name ' + intent_name + ' not supported')


def wecarebill(intent_request):
    firstname = intent_request['currentIntent']['slots']['firstname']
    lastname = intent_request['currentIntent']['slots']['lastname']
    phone = intent_request['currentIntent']['slots']['phone']
    invocation_source = intent_request['invocationSource']
    intent_name = intent_request['currentIntent']['name']
    slots = intent_request['currentIntent']['slots']
    session_attributes = {} if intent_request['sessionAttributes'] is None else intent_request[
        'sessionAttributes']

    if invocation_source == 'DialogCodeHook':
        if not firstname:
            return delegate(session_attributes, slots)
        ######################################################################
        if firstname and not lastname:
            return delegate(session_attributes, slots)
        ######################################################################
        if firstname and lastname and not phone:
            if lastname == 'back':
                intent_request['currentIntent']['slots']['firstname'] = None
                intent_request['currentIntent']['slots']['lastname'] = None
                x = wecarebill(intent_request)
            else:
                x = delegate(session_attributes, slots)
            return x
        ######################################################################
        return delegate(session_attributes, slots)

    elif invocation_source == 'FulfillmentCodeHook':
        if phone == 'back':
            intent_request['currentIntent']['slots']['lastname'] = None
            intent_request['currentIntent']['slots']['phone'] = None
            intent_request['invocationSource'] = 'DialogCodeHook'
            x = wecarebill(intent_request)
        else:
            x = close(
                session_attributes, 'Fulfilled', {
                    'contentType':
                    'PlainText',
                    'content':
                    f'[First Name: {firstname}] - [Last Name: {lastname}] - [Phone Number: {phone}]'
                })
        return x


def lambda_handler(event, context):
    logger.debug("event.bot.name={event['bot']['name']}")
    return dispatch(event)
