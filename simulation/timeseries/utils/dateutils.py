from datetime import datetime
from datetime import timedelta
import pandas as pd

def days_between(d1, d2):
    return abs((d2 - d1).days) > 0

def numDaysBetween(d1, d2):
    return abs((d2 - d1).days)

def numMinutesBetween(d1, d2):
    return abs((d2 - d1).minutes)

def dataAtual():
    return datetime.utcnow() #Usar UTC

def convertDateToStr(d):
    return datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ').strftime('%Y-%m-%d')

def convertDateToStr2(d):
    return datetime.strptime(d, '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')

def convertStrToDate(d):
    return datetime.strptime(d, '%Y-%m-%dT%H:%M:%SZ')

def convertStrToDateFull(d):
    return datetime.strptime(d, '%Y-%m-%dT%H:%M:%S.000Z')

def rangeDates(dt ,numDays):
    return [x.strftime("%Y-%m-%d") for x in pd.date_range(dt, periods=numDays).to_pydatetime().tolist()]

def rangeMinutes(dt_ini ,dt_fin):
    return [x for x in pd.date_range(dt_ini, dt_fin, freq="1min").to_pydatetime().tolist()]

def addDays(dt, numDays):
    return (datetime.strptime(dt, '%Y-%m-%d') + timedelta(days=numDays)).strftime("%Y-%m-%d")

def addDaysDateFull(dt, numDays):
    return (datetime.strptime(dt, '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(days=numDays)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def addMinutesDateStr(dt, numMinutes):
    return (datetime.strptime(dt+'T00:00:00.000Z', '%Y-%m-%dT%H:%M:%S.000Z') + timedelta(minutes=numMinutes)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

def addMinutesDate(dt, numMinutes):
    return (dt + timedelta(minutes=numMinutes)).strftime("%Y-%m-%dT%H:%M:%S.000Z")