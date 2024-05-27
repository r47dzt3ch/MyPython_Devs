#!/usr/bin/python3
'''
Instructions: 
1. Create class ECar[Surname] 
2. Problem Scenario 
Electronic vehicles are becoming rampant nowadays because of its environment friendly benefits.  
One problem they seem to observe for the owners is the monitoring of how much exact percentage  
of battery charge will the owner be needing per destination. The consumption is based on  kilograms`
load and distance travelled. You seemed to be very optimistic on helping them, thus you  are very eager 
to develop a program that foresee and monitor battery consumptions of a car or  vehicle. 
Each km travel on a normal load (0) is thrice the distance to be consumed or should be reduced 
from your vehicle`s battery charge. While twice the mass (kg) of the load per km travelled diminishing 
value. How much amount of battery charge, allowable distance and kg needed for each  vehicle for each 
destination?  
3. Input 
Input consist 1 integer percentage for car battery charge and 3 values float values: distance  
travelled in km, load weight in kg, and vehicle`s capacity or Gross vehicle weight rating(GVWR) in  
pounds (lbs) where 1 kg= 2.20462262 
1kg = 0.001 km
4. Constraints 
0 ≤ battery charge(percentage) ≤100 
3,000.00 ≤ GVWR (lbs) ≤10,000.00 
0.1 ≤ Distance (km) ≤ ∞ 
0 ≤ load weight (kg) ≤ GVRW max limits 
5. Output 
Your program should output the battery charge before the travel, GVRW, distance, load weight, 
and battery charge after the travel.
IT121/L Martzel P. Baste|Page 1 
LEGACY COLLEGE OF COMPOSTELA Dagohoy Street, Poblacion Compostela Compostela Province 
6. Source Codes 
7. Sample Input/Output 
NOTE: Provide a screenshot and describe your observation for each action you performed
based on  the item below: 
✓ Input any value for battery charge, gvwr, distance and load between the constraints 
✓ Input any battery charge, gvwr, distance and load value NOT between the constraints 
✓ Input any value for load more than its gvwr 
✓ Input less battery charge with much more required distance and load 
8. Submit your file with filename convention: ECar[Surname] 
'''
import os
from colorama import init
init(autoreset=True)
from colorama import Fore
class Ecar_Jose():
    def Ecar():
        try:
            print("Welcome to E-Car Management System\n")
            batt_charge=int(input("Input battery charge: "))
            if batt_charge >= 0 and batt_charge <=  100:
                print("The battery Percentage charge of car is: {}%\n".format(batt_charge))
                min_gvwr=3000.00
                max_gvwr=10000.00
                GVWWR = float(input("Input vehicle`s capacity with minimum of 3000.00 upto the maximum of 10000.00: "))
                if (GVWWR >=  min_gvwr and GVWWR <= max_gvwr):
                    gvwr_inKG = GVWWR / 2.20462262
                    print("The gross vehicle weight(lbs) capacity is: {}\n".format(GVWWR))
                    distance = float( input("distance travelled in km: "))
                    if distance >= 0:
                        print("distance travelled in km is: {}\n".format(distance))
                        load_weight = float(input("Input the load weight in kg: "))
                        if (load_weight >= 0 and load_weight <= gvwr_inKG):
                            print("The car load weight is: {} kg\n\n".format(load_weight))
                            
                            batt_charge_consumed=int((distance*3)+(((load_weight*2)*0.001)*distance))
                            batt_charge_after=(batt_charge-batt_charge_consumed)
                            batt_addedCharge=batt_charge_after-1
                            print("The consumed battery charge percentage after travel is: {}%".format(batt_charge_consumed))
                            if (batt_charge_after >=0):
                                print("The remaining charge of the car is: {}%\n".format(batt_charge_after))
                                # comment: 
                            else:
                                 print("The Battery charged {}% of the car is not reached into their distination  of {} km\n\nTo make it reach you need to add {}% of battery charge\n".format(batt_charge, distance,abs(batt_addedCharge)))
                                # comment: 
                            # END IF
                           
                            # comment: 
                        else:
                            # comment: 
                            print("The load weight is exceeded to the vehicles capacity is {} kg".format(gvwr_inKG))
                        # END IF
                    else:
                        # comment: 
                        print("The required Distance is greater than equal to  0.1 km\n")
                    
                    #return 1
            else:
                print("Your car battery is not working\n")  


        except Exception as e:
            print ("Error:  ",e)
        pass
    
    cond = True
    while cond:
        Ecar()
        print("\n{}Are you want to continue?\n{}(enter)-Yes\t\t{}(1)-No".format(Fore.YELLOW,Fore.GREEN,Fore.RED))
        key = input("enter: ")
        os.system('cls')
        if str(key) =='1' or str(key)=='no':
            cond=False
pass

  

    