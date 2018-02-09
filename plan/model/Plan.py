from django.db import models
from django.utils import timezone
from datetime import date, timedelta, datetime
import datetime
from plan.model.Season import Season
import json

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
    duration = models.PositiveIntegerField('Duration of plan', default=0)
    load = models.PositiveIntegerField('Load', default=0)
    parent_season = models.ForeignKey(Season, on_delete=models.CASCADE)

    def __str__(self):
        return "{}-hour plan for {}".format(self.annualHours, self.name)
        
    def save_data(self, data, season_id):
        self.name = data['name']
        self.annualHours = int(data['annualHours'])
        self.typeOfPlan = data['typeOfPlan']
        self.planStart = data['planStart']
        self.planEnd = data['planEnd']
        self.parent_season = Season(season_id)
        
    def createPlan(self, weeklyHours, userProfile, aRaces, allRaces):
        self.weeksCount = (self.planEnd - self.planStart).days // 7 + 1      #counts the duration of the plan in weeks
        peak = self.createPlanWeeks(aRaces)     #creates PlanWeeks - sets week #, monday, assigns races to races AND returns week #s that contain A-races 
        #peak = self.whenIsPeakRace(weeksCount)        #returns week #s that contain A-races 
        peakPeriods = self.makePeakPeriods(peak, userProfile.age)        #creates peak training periods according to A-races
        self.assignRaceWeeks(peakPeriods)        #assigns peak training periods to its weeks
        if peakPeriods == []: #if peak periods do not exist, classic model applies to all other weeks
            self.setOtherWeeks(self.typeOfPlan, self.weeksCount-1, userProfile.age)   
        else:         # if peak periods exist, other weeks are set their periods according to these peak periods
            self.setOtherWeeks(self.typeOfPlan, peakPeriods[0], userProfile.age)
        self.setSkillTraining(userProfile, weeklyHours) # sets skill training to weeks according to training period and profile settings
        self.setAllRaces(allRaces) # assign B- and C- races to their weeks
        self.count_load()
        self.duration = len(self.planWeeks)
        self.correct = True
        
        for week in self.planWeeks: # after planWeeks are complete, they are saved into the db
            week.save()
            
            
    # creates instances of PlanWeeks for the plan, assigns standard values to properties 
    def createPlanWeeks(self, aRaces):
        self.planWeeks = [0]*self.weeksCount
        for i in range(self.weeksCount):
            weekplan = PlanWeek(parent_plan = self)
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
            weekplan.races = []
            self.planWeeks[i] = weekplan

        peaks = []
        for data in aRaces:     #priradzovanie pretekov k tyzdnom
            for week in self.planWeeks:      #skusa pre kazdy tyzden:
                mon = week.getMonday()
                if mon <= data.date < mon + datetime.timedelta(days=7):  # ak je datum pretekov v danom tyzdni
                    week.setRace(data.name)
                    if data.priority == 3: # checks if the races assigned is High priority
                        peaks.append(week.getWeek()) # adds A-race into the list of peaks
                    break
        return peaks
      
    #deprecated. createPlanWeeks'  if data['priority'] == 3 does the job instead and returns the same list 
    def whenIsPeakRace(self, weeksCount):
        peaks = []
        for i in range(weeksCount-1, -1, -1):
            for r in self.planWeeks[i].races:
                if i not in peaks:
                    peaks.append(self.planWeeks[i].week)
        return peaks
    
    def makePeakPeriods(self, peak, age):   
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
                print(peak[ref], ref, peak[-1])
                minimum = min(len(peak)-ref, 3)
                for i in range(1, minimum):
                    if peak[ref+i] - peak[ref] < 3:
                        if peak[ref+i] < 6 - shorterPeriods:
                            print('i got here')
                            peak.pop(ref+i)
                        else:
                            print('i got here2')
                            peakPeriods.append([range(ref, ref+i+1)])
                            ref = peak[ref+i]
                    else:
                        print('i got here3')
                        peakPeriods.append(peak[ref])
                ref += i
                print('i got here4')
            if peak[ref-1] - peak[ref] > 6 or peak[ref-1] - peak[ref] == 1:
                peakPeriods.append(peak[ref]) 
            return peakPeriods
            
    def assignRaceWeeks(self, racePeriods):
        for week in self.planWeeks:
            if week.getWeek() in racePeriods:
                week.setPeriod('Racing-1')
    
    def setOtherWeeks(self, typ, peak0, age):
        index = 0
        weekNumber = self.weeksCount - 1
        
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
                self.planWeeks[weekNumber].setPeriod('Recovery-1')
            else:
                if self.planWeeks[weekNumber].getPeriod() == 'Racing-1':
                    index = 0
                else:
                    self.planWeeks[weekNumber].setPeriod(periods[index])
                    index += 1
            weekNumber -= 1
        for i in range(len(self.planWeeks)):
            if self.planWeeks[i].getPeriod() == 'Racing-1':
                if self.planWeeks[i-1].getPeriod == 'Racing-1':
                    self.planWeeks[i+2].setPeriod('Recovery-1')
                self.planWeeks[i+1].setPeriod('Recovery-1')
        
    def setSkillTraining(self, userProfile, weeklyHours):
        weak = userProfile.weak1
        weak2 = userProfile.weak2
        strong = userProfile.strong1
        #strong2 = data['strong2']
        if True:
        #if activeUser.getAge() < 40: #pre 4-tyzdnove cykly
            for week in self.planWeeks:
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
                    
            periods = ['annualHours', 'Preparatory-1', 'Base 1-1', 'Base 1-2', 'Base 1-3', 'Base 1-4', 
               'Base 2-1', 'Base 2-2', 'Base 2-3', 'Base 2-4', 'Base 3-1', 'Base 3-2', 'Base 3-3', 'Base 3-4', 
               'Build 1-1', 'Build 1-2', 'Build 1-3', 'Build 1-4', 'Build 2-1', 'Build 2-2', 'Build 2-3', 'Build 2-4', 
               'Peak 1', 'Peak 2', 'Racing-1', 'Recovery-1']            
        
            #assigns Force Maintenance to remamining weeks and sets weekly hours to all weeks
            for week in self.planWeeks:
                if not week.getForce():
                    if week.getPeriod()[:4] in ('Buil', 'Base'):
                        week.setGym('FM')
                period = weeklyHours[periods.index(week.getPeriod())]
                week.setWeeklyHours(period)
 
    def setAllRaces(self, races): 
        for week in self.planWeeks:      #skusa pre kazdy tyzden:
            week.races = []
        if races:
            for race in races:     #priradzovanie pretekov k tyzdnom
                for week in self.planWeeks:      #skusa pre kazdy tyzden:
                    mon = week.getMonday()
                    if mon <= race.date < mon + datetime.timedelta(days=7):  # ak je datum pretekov v danom tyzdni
                        week.setRace(race.name)
                        break
    
    def count_load(self):
        load = 0.0
        for week in self.planWeeks:
            print(week.weeklyHours) 
            load += float(week.weeklyHours)
            print(load)
        self.load = round(load)
        print(self.load)
        
    def get_graph_data(self, planWeeks):
        x = []
        y = []
        captions = []
        
        for wk in planWeeks:
            x.append(int(wk.week))
            y.append(int(wk.weeklyHours))
            text = "Week: {}\nPeriod: {}\nHours: {}\nMonday: {}\nTraining:".format(wk.week, wk.period, wk.weeklyHours, wk.monday)
            if wk.gym:
                text += ' Gym: {}'.format(wk.gym)                    
            if wk.endurance != '0':
                text += ' EN'
            if wk.force != '0':
                text += ' FO'
            if wk.speedSkills != '0':
                text += ' SpS'
            if wk.eForce != '0':
                text += ' EF'
            if wk.aEndurance != '0':
                text += ' AE'
            if wk.maxPower != '0':
                text += ' MP'
            if wk.test != '0':
                text += ' TEST'
                
            captions.append(text)
            
        if (len(x) == len(y)):
            return [x, y, captions]

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
    
    def setWeek(self, week):
        self.week = week

    def getWeek(self):
        try:
            return self.week
        except:
            return None

    def setMonday(self, monday):
        self.monday = monday

    def getMonday(self):
        try:
            return self.monday
        except:
            return None
        
    def setRace(self, race):
        a = self.races
        self.races.append(race)
        
    def getRace(self):
        r = '\n'.join(self.races)
        return r

    def setPeriod(self, period, periodWeek=1):
        self.period = period
        self.periodWeek = periodWeek    
    
    def getPeriod(self):
        try:
            return self.period #, self.periodWeek
        except:
            return None
    
    def setWeeklyHours(self, hours):
        self.weeklyHours = hours

    def getWeeklyHours(self):
        try:
            return self.weeklyHours
        except:
            return None

    def getWeeklyHoursFromDB(self, period, week):
        return 5

    def setGym(self, gym):
        self.gym = gym
        
    def getGym(self):
        try:
            return self.gym
        except:
            return None

    def setEndurance(self, endurance):
        self.endurance = endurance

    def getEndurance(self):
        try:
            return self.endurance
        except:
            return None

    def setForce(self, force):
        self.force = force

    def getForce(self):
        try:
            return self.force
        except:
            return None
        
    def setSpeedSkills(self, speedSkills):
        self.speedSkills = speedSkills

    def getSpeedSkills(self):
        try:
            return self.speedSkills
        except:
            return None
        
    def setEForce(self, eForce):
        self.eForce = eForce

    def getEForce(self):
        try:
            return self.eForce
        except:
            return None
        
    def setAEndurance(self, aEndurance):
        self.aEndurance = aEndurance

    def getAEndurance(self):
        try:
            return self.aEndurance
        except:
            return None
        
    def setMaxPower(self, maxPower):
        self.maxPower = maxPower

    def getMaxPower(self):
        try:
            return self.maxPower
        except:
            return None
        
    def setTest(self, test):
        self.test = test

    def getTest(self):
        try:
            return self.test
        except:
            return None

    def prepareData(self):
        if self.endurance:
            self.endurance = 'X'
        else:
            self.endurance = ''
        if self.force:
            self.force = 'X'
        else:
            self.force = ''
        if self.speedSkills:
            self.speedSkills = 'X'
        else:
            self.speedSkills = ''
        if self.aEndurance:
            self.aEndurance = 'X'
        else:
            self.aEndurance = ''
        if self.eForce:
            self.eForce = 'X'
        else:
            self.eForce = ''
        if self.maxPower:
            self.maxPower = 'X'
        else:
            self.maxPower = ''    
        if self.test:
            self.test = 'X'
        else:
            self.test = '' 
        if self.races != '[]':
            string = self.races[2:-2]
            races = string.split(',')
            self.races = ', '.join(races)
        else:
            self.races = '-'       
        self.monday = self.monday.strftime('%b, %d')
        if self.gym == 'False':
            self.gym = '-'
        
        
        
        
        
    
class PlanWeekDay(models.Model):
    dailyHours = models.DecimalField(max_digits=4, decimal_places=2)
    day = models.PositiveIntegerField(0)
    intensity = models.PositiveIntegerField(0)
    workoutType = models.PositiveIntegerField(0)
    parent_week = models.ForeignKey(PlanWeek, on_delete=models.CASCADE)