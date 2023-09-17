
def get_valid_columns(model):
    """Retrieve valid column names for a given SQLAlchemy model."""
    return [col.name for col in model.__table__.columns]

def are_keys_valid(filters, model):
    """Check if all keys in filters are valid columns of the given model."""
    valid_columns = get_valid_columns(model)
    return all(key in valid_columns for key in filters.keys())

# def find_records(model, **filters):
#     """
#     Retrieve records from the specified model based on provided filters.
#     """
#     # Check if all filter keys are valid
#     if not are_keys_valid(filters, model):
#         raise ValueError("Invalid column name provided in filters.")
    
#     session = Session()
#     query = session.query(model)
    
#     # Apply filters to the query
#     for key, value in filters.items():
#         query = query.filter(getattr(model, key) == value)

#     # Execute and fetch the results
#     results = query.all()
#     session.close()

#     return results
