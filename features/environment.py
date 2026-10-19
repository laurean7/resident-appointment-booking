def before_scenario(context, scenario):
    context.slots = {}
    context.prebooked = []
    context.result = None
