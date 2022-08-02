

# --- Abstract method ---
def abstract_literal(lit):
    if lit['type'] == 'NumericLiteral':
        return lit['value']
    elif lit['type'] == 'NullLiteral':
        return None
    elif lit['type'] == 'StringLiteral':
        return lit['value']
    elif lit['type'] == 'BooleanLiteral':
        return lit['value']