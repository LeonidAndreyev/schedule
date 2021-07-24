import pandas as pd
import streamlit as st

def update_location(a_, b_,row_, col_):
    if len(a_.columns)-1 > col_:
        col_ += 1
    elif len(a_.columns)-1 <= col_:
        col_ = 0
        row_ += 1
        try:
            if pd.isnull(b_.iloc[row_, :]).all(axis=0) == True:
                b_.loc[row_, :] = float("nan")
        except IndexError:
             b_.loc[row_, :] = float("nan")
    return(row_, col_)

def option1 (a_, b_, c_, con_, row_, col_):
    while (pd.isnull(b_.iloc[row_, con_ * col_]) == False):
                    row_, col_ = update_location(a_, b_, row_, col_)
    return(row_, col_)

def option2 (f_, a_, b_, c_, c, con_, row_, col_, attempt, possibility):
    while (pd.isnull(b_.iloc[row_, con_ * col_]) == False) or (c_.Duration[c] > a_.iloc[0, col_]):
        attempt += 1
        row_, col_ = update_location(a_, b_, row_, col_)
        if attempt > f_.shape[0] + 2 * len(a_.columns):
            possibility = False
            break
    return(row_, col_, attempt, possibility)

def option3 (a_, b_, c_, c, v_, con_, row_, col_):
    while (pd.isnull(b_.iloc[row_, con_ * col_]) == False) or ((b_.loc[:, b_.columns[(con_ * col_) + 2]] == c_[v_[2]][c]).any() and c_[v_[2]][c] != "E"):
        row_, col_ = update_location(a_, b_, row_, col_)
    return(row_, col_)

def option4 (f_, a_, b_, c_, c, v_, con_, row_, col_, attempt, possibility):
    while (pd.isnull(b_.iloc[row_, con_ * col_]) == False) or ((b_.loc[:, b_.columns[(con_ * col_) + 2]] == c_[v_[2]][c]).any() and c_[v_[2]][c] != "E") or (c_.Duration[c] > a_.iloc[0, col_]):
        attempt += 1
        row_, col_ = update_location(a_, b_, row_, col_)
        if attempt > f_.shape[0] + 2 * len(a_.columns):
            possibility = False
            break  
    return(row_, col_, attempt, possibility)

def distribution(f_, a_, b_, c_, v_, con_, condition_1, condition_2, condition_3, non_distributed):
    for c in c_.index:
        possibility = True
        attempt = 0
        row_ = 0
        col_ = len(a_.columns)-1
        row_, col_ = update_location(a_, b_, row_, col_)
        while possibility == True:
            if (condition_2 == True and condition_3 == True):
                row_, col_, attempt, possibility = option4 (f_, a_, b_, c_, c, v_, con_, row_, col_, attempt, possibility)
            elif (condition_2 == True and condition_3 == False):
                row_, col_ = option3 (a_, b_, c_, c, v_, con_, row_, col_)
            elif (condition_2 == False and condition_3 == True):
                row_, col_, attempt, possibility = option2(f_, a_, b_, c_, c, con_, row_, col_, attempt, possibility)
            elif (condition_2 == False and condition_3 == False):
                row_, col_ = option1 (a_, b_, c_, con_, row_, col_)    
            break
        if possibility == True:
            for v in range (0, len(v_)):
                b_.loc[row_, b_.columns[(con_ * col_) + v]] = c_[v_[v]][c]
            a_.iloc[0, col_] -= c_.Duration[c]
        elif possibility == False:
            non_distributed.append(c_.Courses[c])