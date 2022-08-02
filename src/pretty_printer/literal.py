from utils.delimiters import *

# --- Abstract method ---
def abstract_literal(lit):
    if lit['type'] == 'NumericLiteral':
        return str(lit['value']) 
    elif lit['type'] == 'NullLiteral':
        return "null"
    elif lit['type'] == 'StringLiteral':
        return quoteDelimiter + lit['value'] + quoteDelimiter
    elif lit['type'] == 'BooleanLiteral':
        return str(lit['value']).lower()