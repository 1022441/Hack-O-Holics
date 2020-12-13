from textwrap import wrap
import datetime



operators = [
             ['contains '],
             ['datestartswith ']]


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]
                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    # try:
                    #     value = float(value_part)
                    # except ValueError:
                    value = value_part
                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


def update_table(filter_q, dff, del_row=None):
    # print("filter_q, dff-----------", filter_q, dff)
    filtering_expressions = filter_q.split(' && ')
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
        elif operator == 'contains':
            dff = dff.loc[dff[col_name].str.contains(filter_value, case=False)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            dff = dff.loc[dff[col_name].str.startswith(filter_value)]

    if del_row:
        dff = dff["uee_id" != del_row]
    return dff.to_dict('records')

def wrap_str(text_val, width):
    return "<br>".join(wrap(text_val, width=width))


def assign_val(inp_dict, dkey, dval):
    if dval:
        inp_dict[dkey] = dval
    return inp_dict


def valid_date(input_date):
    if input_date == "NA" or input_date == "NaT":
        out_date = datetime.datetime.min
    elif input_date:
        out_date = input_date
    else:
        out_date = datetime.datetime.min

    return out_date

def switch_val(val):
    if val:
        return True
    else:
        return False


def get_group(total, strat, num=7):
    import math
    if total <=num:
        return list(range(total))
    else:
        val = math.ceil(total/num)
        if strat > val:
            strat = val
        start = (strat - 1) * num
        lst = list(range(0, total))
        return lst[start:start + num]



