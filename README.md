#Stack ID integration - Internal

#This is one of our internal projects at work to integrate our stackID into zabbix
#StackID is a way to group all the similar application servers with common purpose under one name
#There was a need to organize such common servers with a similar stackID into zabbix
#Advantages of this would be to assign particular templates in zabbix to different stackIDs
#In this project I have integrated stackID's as host groups into zabbix
#If you want to assign, say, IIS template to one particular stackID, then you can do it by assigning the IIS template with hostgroup which has the same name as its stackID
#This uses the Pyzabbix api which is available for zabbix

