#!/usr/bin/env python3

def format_number(num):
    if isinstance(num, (int, float)):
        return f'{num:,.2f}'
    return str(num)

def format_pct(pct):
    if isinstance(pct, (int, float)):
        return f'{pct:+.2f}%'
    return str(pct)
