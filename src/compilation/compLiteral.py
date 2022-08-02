from utils.delimiters import *
from utils.assemblyFunctions import convertASMExpression

# --- Abstract method ---
def abstract_literal(lit):
    if lit['type'] == 'NumericLiteral':
        return convertASMExpression("iconst", str(lit['value']))
    elif lit['type'] == 'NullLiteral':
        return convertASMExpression("aconst", "NULL")
    