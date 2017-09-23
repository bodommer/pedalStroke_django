from django.db import models
from django.utils import timezone
from datetime import date, timedelta
from plan.model.Season import Season

class Plan(models.Model):
    PLAN_CHOICES = (
        ('normal', 'Normal'),
        ('reversed', 'Reversed')
    )

    start = date.today()
    end = start + timedelta(weeks=52)

    name = models.CharField(max_length=80, default="")
    annualHours = models.PositiveIntegerField('Annual hours', default=200)
    typeOfPlan = models.CharField('Type of Plan', max_length=20,
                                  choices=PLAN_CHOICES, default='normal')
    planStart = models.DateField('Start of Plan', default=start)
    planEnd = models.DateField('End of Plan', default=end)
    parent_season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-hour plan for {}".format(self.annualHours, self.season_id)

    def count_load(self, weekset):
        load = 0
        print(weekset)
        for a in weekset: 
            load += a
        self.load = load
        
    def save_data(self, data, season_id):
        self.name = data['name']
        self.annualHours = int(data['annualHours'])
        self.typeOfPlan = data['typeOfPlan']
        self.planStart = data['planStart']
        self.planEnd = data['planEnd']
        self.parent_season = Season(season_id)
        
    def createPlan(self, annualHours, season, typeOfPlan, planStart, planEnd, activeUser, age, id=0):
        errordata = []
        if not self.setAnnualHours(annualHours):
            errordata.append('annual hours')
        if not self.setTypeOfPlan(typeOfPlan):
            errordata.append('type of plan')
        if not self.setPlanStart(planStart):
            errordata.append('start of plan - must be monday')
        if not self.setPlanEnd(planEnd):
            errordata.append('end of plan')
        if errordata != []:
            errordata = ', '.join(errordata)
            self.errordata = errordata
            return
        weeksCount = (self.planEnd - self.planStart).days // 7 + 1      #spocita ake dlhe je obdobie
        planWeeks = self.createPlanWeeks(weeksCount, season)     #vytvori treningove tyzdne - urci tyzden + pondelok, priradi tyzdnom zoznam pretekov
        peak = self.whenIsPeakRace(planWeeks, weeksCount)        #vrati cisla tyzdnov, kedy su Ackove preteky 
        peakPeriods = self.makePeakPeriods(peak, activeUser, age)        #spravi zavodne obdobia na zaklade Ackovych pretekov
        self.assignRaceWeeks(planWeeks, peakPeriods)
        if peakPeriods == []:
            self.setOtherWeeks(planWeeks, weeksCount-1, typeOfPlan, weeksCount-1, age)   
        else:         
            self.setOtherWeeks(planWeeks, weeksCount-1, typeOfPlan, peakPeriods[0], age)
        self.setSkillTraining(planWeeks, activeUser, annualHours)
        self.planWeeks = planWeeks
        self.setAllRaces(season)
        self.correct = True
        self.errordata = errordata
        # po dokonceni vytvarania planu zacne ukladat data do databazy (ak vsetko prebehlo v poriadku a spravne)
        if self.errordata == []:
            conn= pymysql.connect(host=self.server,user=self.username,password=self.password,db=self.database,charset=self.charset,cursorclass=pymysql.cursors.DictCursor)
            a=conn.cursor()
            add_plan = ("INSERT INTO tp_plan VALUES (%s, %s, %s, %s, %s, %s)")
            data_plan = (id, annualHours, typeOfPlan, planStart, planEnd, season)
            a.execute(add_plan, data_plan)
            conn.commit()
            get_id = ("SELECT id FROM tp_plan WHERE annualHours={} AND season_id={}".format(annualHours, season))
            a.execute(get_id)
            planID = a.fetchone()
            planID = planID['id']
            for p in self.planWeeks:
                add_planWeek = ("INSERT INTO tp_planweek VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
                data_planWeek = (id, p.getAEndurance(), p.getEForce(), p.getEndurance(), p.getForce(), p.getGym(), p.getMaxPower(), p.getMonday(), p.getPeriod(), p.getSpeedSkills(), p.getTest(), p.getWeek(), p.getWeeklyHours(), p.getRace(), planID)
                a.execute(add_planWeek, data_planWeek)
                conn.commit()
            a.close()
            conn.close()
            
    def createPlanWeeks(self, weeksCount, season):
        planWeeks = [0]*weeksCount
        for i in range(weeksCount):
            weekplan = PlanWeek()
            weekplan.setWeek(i+1)
            weekplan.setMonday(self.planStart + i*datetime.timedelta(days=7))
            weekplan.setPeriod('')
            weekplan.setGym(False)
            weekplan.setEndurance(False)
            weekplan.setForce(False)
            weekplan.setSpeedSkills(False)
            weekplan.setEForce(False)
            weekplan.setAEndurance(False)
            weekplan.setMaxPower(False)
            weekplan.setTest(False)
            planWeeks[i] = weekplan
        conn= pymysql.connect(host=self.server,user=self.username,password=self.password,db=self.database,charset=self.charset,cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_races = ("SELECT date FROM tp_seasonrace WHERE season_id={} AND priority=3".format(season))
        a.execute(get_races)
        races = a.fetchall()
        a.close()
        conn.close()
        for data in races:     #priradzovanie pretekov k tyzdnom
            for week in planWeeks:      #skusa pre kazdy tyzden:
                mon = week.getMonday()
                if mon <= data['date'] < mon + datetime.timedelta(days=7):  # ak je datum pretekov v danom tyzdni
                    week.setRace(data)
                    break
        return planWeeks
        
    def whenIsPeakRace(self, planWeeks, weeksCount):
        peaks = []
        for i in range(weeksCount-1, -1, -1):
            for r in planWeeks[i].races:
                if i not in peaks:
                    peaks.append(planWeeks[i].week)
        return peaks
    
    def makePeakPeriods(self, peak, activeUser, age):   
        if peak == []:
            return [] 
        if age > 40: #or gender = woman
            shorterPeriods = 1
        else:
            shorterPeriods = 0
        if len(peak) == 1:
            if peak[0] > 5 - shorterPeriods:
                return list([peak[0]])
                pass
            else:
                return []
        else:
            peakPeriods = []
            ref = 0
            while peak[ref] != peak[-1]:
                minimum = min(len(peak)-ref, 3)
                for i in range(1, minimum):
                    if peak[ref] - peak[ref+i] < 3:
                        if peak[ref+i] < 6 - shorterPeriods:
                            peak.pop(ref+i)
                        else:
                            peakPeriods.append([range(ref, ref+i+1)])
                            ref = peak[ref+i]
                    else:
                        peakPeriods.append(peak[ref])
                ref += i
            if peak[ref-1] - peak[ref] > 6 or peak[ref-1] - peak[ref] == 1:
                peakPeriods.append(peak[ref]) 
            return peakPeriods
            
    def assignRaceWeeks(self, planWeeks, racePeriods):
        for week in planWeeks:
            if week.getWeek() in racePeriods:
                week.setPeriod('Racing-1')
    
    def setOtherWeeks(self, planWeeks, weekNumber, typ, peak0, age):
        index = 0
        if age > 39: #or gender = woman
            if typ == 'normal':
                periods = ['Peak 2', 'Peak 1', 
                           'Build 2-4', 'Build 2-2', 'Build 2-1', 
                           'Build 1-4', 'Build 1-2', 'Build 1-1', 
                           'Base 3-4', 'Base 3-2', 'Base 3-1', 
                           'Base 2-4', 'Base 2-2', 'Base 2-1', 
                           'Base 1-4', 'Base 1-2', 'Base 1-1',
                           'Preparatory-1']
            elif typ == 'reversed':
                periods = ['Peak 2', 'Peak 1', 
                           'Base 3-4','Base 3-2', 'Base 3-1', 
                           'Base 2-4', 'Base 2-2', 'Base 2-1', 
                           'Base 1-4', 'Base 1-2', 'Base 1-1', 
                           'Build 2-4', 'Build 2-2', 'Build 2-1', 
                           'Build 1-4', 'Build 1-2', 'Build 1-1',
                           'Preparatory-1']
        else:
            if typ == 'normal':
                periods = ['Peak 2', 'Peak 1', 
                           'Build 2-4', 'Build 2-3', 'Build 2-2', 'Build 2-1', 
                           'Build 1-4', 'Build 1-3', 'Build 1-2', 'Build 1-1', 
                           'Base 3-4', 'Base 3-3', 'Base 3-2', 'Base 3-1', 
                           'Base 2-4', 'Base 2-3', 'Base 2-2', 'Base 2-1', 
                           'Base 1-4', 'Base 1-3', 'Base 1-2', 'Base 1-1',
                           'Preparatory-1']
            elif typ == 'reversed':
                periods = ['Peak 2', 'Peak 1', 
                           'Base 3-4', 'Base 3-3', 'Base 3-2', 'Base 3-1', 
                           'Base 2-4', 'Base 2-3', 'Base 2-2', 'Base 2-1', 
                           'Base 1-4', 'Base 1-3', 'Base 1-2', 'Base 1-1', 
                           'Build 2-4', 'Build 2-3', 'Build 2-2', 'Build 2-1', 
                           'Build 1-4', 'Build 1-3', 'Build 1-2', 'Build 1-1',
                           'Preparatory-1']
        if weekNumber > len(periods):
            for i in range(weekNumber-len(periods)+1):
                periods.append('Preparatory-1') 
        while weekNumber > -1:
            if weekNumber > 43 and weekNumber > peak0:
                planWeeks[weekNumber].setPeriod('Recovery-1')
            else:
                if planWeeks[weekNumber].getPeriod() == 'Racing-1':
                    index = 0
                else:
                    planWeeks[weekNumber].setPeriod(periods[index])
                    index += 1
            weekNumber -= 1
        for i in range(len(planWeeks)):
            if planWeeks[i].getPeriod() == 'Racing-1':
                if planWeeks[i-1].getPeriod == 'Racing-1':
                    planWeeks[i+2].setPeriod('Recovery-1')
                planWeeks[i+1].setPeriod('Recovery-1')
        
    def setSkillTraining(self, planWeeks, activeUser, annualHours):
        conn= pymysql.connect(host=self.server,user=self.username,password=self.password,db=self.database,charset=self.charset,cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_props = ("SELECT weak1, weak2, strong1, strong2 FROM tp_user WHERE id={}".format(activeUser))
        a.execute(get_props)
        data = a.fetchone()
        a.close()
        conn.close() 
        weak = data['weak1']
        weak2 = data['weak2']
        strong = data['strong1']
        #strong2 = data['strong2']
        if True:
        #if activeUser.getAge() < 40: #pre 4-tyzdnove cykly
            for week in planWeeks:
                periodName = week.getPeriod()[:4]
                try:
                    periodCount = int(week.getPeriod()[-3])
                    weekCount = int(week.getPeriod()[-1])
                except:
                    periodCount = 1
                    weekCount = 1
                if periodName == 'Prep':
                    week.setEndurance(True)
                    week.setSpeedSkills(True)
                    if 0 < weekCount < 3:
                        week.setGym('MT')
                    elif 2 < weekCount < 6:
                        week.setGym('AA') 
                        
                if weekCount != 4:
                    if periodName == 'Base':
                        week.setEndurance(True)
                        week.setSpeedSkills(True)    
                        if periodCount != 1:
                            week.setForce(True)
                            week.setEForce(True)
                        else:
                            week.setGym('MP')
                        
                    if periodName == 'Buil':
                        week.setEForce(True)
                        week.setEndurance(True)
                        if periodCount == 1:
                            if weak == '':
                                week.setForce(True)
                            else:
                                if weak == 'AEndurance':
                                    week.setAEndurance(True)
                                elif weak == 'Force':
                                    week.setForce(True)
                                elif weak == 'SpeedSkills':
                                    week.setSpeedSkills(True)
                                elif weak == 'MaxPower':
                                    week.setMaxPower(True)
                            if weak not in ('AEndurance', 'MaxPower'):
                                week.setSpeedSkills(True)  
                                
                        else:
                            if weak in ('', 'Force'):
                                week.setForce(True)
                            else:
                                if weak == 'AEndurance':
                                    week.setAEndurance(True)
                                elif weak == 'SpeedSkills':
                                    week.setSpeedSkills(True)
                                elif weak == 'MaxPower':
                                    week.setMaxPower(True)
                            a = False
                            if week.getRace() != []:
                                a = True
                            if a:
                                if weak2 == '':
                                    week.setAEndurance(True)
                                else:
                                    if weak2 == 'AEndurance':
                                        week.setAEndurance(True)
                                    elif weak2 == 'Force':
                                        week.setForce(True)
                                    elif weak2 == 'SpeedSkills':
                                        week.setSpeedSkills(True)
                                    elif weak2 == 'MaxPower':
                                        week.setMaxPower(True)         
            
                    if periodName == 'Peak':
                        week.setEForce(True)
                        if weak == '':
                            week.setAEndurance(True)
                        else:
                            if weak == 'AEndurance':
                                week.setAEndurance(True)
                            elif weak == 'Force':
                                week.setForce(True)
                            elif weak == 'SpeedSkills':
                                week.setSpeedSkills(True)
                            elif weak == 'MaxPower':
                                week.setMaxPower(True)  
                            elif weak == 'Endurance':
                                week.setSpeedSkills(True)
                            elif weak == 'EForce':
                                week.setEForce(True)                      
        
                    if periodName == 'Raci':
                        week.setAEndurance(True)
                        week.setSpeedSkills(True)
                        if strong in ('', 'Endurance', 'EForce'):
                            week.setEForce(True)
                        else:
                            if strong == 'MaxPower':
                                week.setMaxPower(True)  
                            if strong == 'Force':
                                week.setForce(True)
                        
                    if periodName == 'Reco':
                        week.setEndurance(True)
                else:
                    week.setEndurance(True)
                    week.setSpeedSkills(True)
                    week.setTest(True)
                    week.setGym('FM')
            for week in planWeeks:
                if not week.getForce():
                    if week.getPeriod()[:4] in ('Buil', 'Base'):
                        week.setGym('FM')
            conn= pymysql.connect(host=self.server,user=self.username,password=self.password,db=self.database,charset=self.charset,cursorclass=pymysql.cursors.DictCursor)
            a=conn.cursor()
            get_hrs = ("SELECT * FROM weeklyhours WHERE annualHours={}".format(annualHours))
            a.execute(get_hrs)
            data = a.fetchone()
            a.close()
            conn.close()
            for week in planWeeks:
                period = data['{}'.format(week.getPeriod())]
                week.setWeeklyHours(period)
 
    def setAllRaces(self, season): 
        conn= pymysql.connect(host=self.server,user=self.username,password=self.password,db=self.database,charset=self.charset,cursorclass=pymysql.cursors.DictCursor)
        a=conn.cursor()
        get_races = ("SELECT * FROM tp_seasonrace WHERE season_id={}".format(season))
        a.execute(get_races)
        races = a.fetchall()
        a.close()
        conn.close()
        for week in self.planWeeks:      #skusa pre kazdy tyzden:
            week.races = []
        if races:
            for data in races:     #priradzovanie pretekov k tyzdnom
                for week in self.planWeeks:      #skusa pre kazdy tyzden:
                    mon = week.getMonday()
                    if mon <= data['date'] < mon + datetime.timedelta(days=7):  # ak je datum pretekov v danom tyzdni
                        week.setRace(data['name'])
                        break
    

class PlanWeek(models.Model):
    aEndurance = models.PositiveSmallIntegerField(0)
    eForce = models.PositiveSmallIntegerField(0)
    endurance = models.PositiveSmallIntegerField(0)
    force = models.PositiveSmallIntegerField(0)
    gym = models.CharField(max_length=10)
    maxPower = models.PositiveSmallIntegerField(0)
    monday = models.DateField()
    period = models.CharField(max_length=25)
    speedSkills = models.PositiveSmallIntegerField(0)
    test = models.PositiveSmallIntegerField(0)
    week = models.PositiveSmallIntegerField(0)
    weeklyHours = models.DecimalField(max_digits=5, decimal_places=1)
    races = models.CharField(max_length=300)
    parent_plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    def __str__(self):
        return "Week {}".format(self.week)
    
class PlanWeekDay(models.Model):
    dailyHours = models.DecimalField(max_digits=4, decimal_places=2)
    day = models.PositiveIntegerField(0)
    intensity = models.PositiveIntegerField(0)
    workoutType = models.PositiveIntegerField(0)
    parent_week = models.ForeignKey(PlanWeek, on_delete=models.CASCADE)