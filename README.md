# ConPLC
Send Data from Siemens S7 PLC to PC and save Data as CSV-File
-tested with S7-300, S7-1200 and S7-1500
-example TIA-Portal Project included
-The PLC-Block FB "ConPLC" sends an UDT (User Defined Datatype) via TCP to the PC
-The PC-Programm reads the recieved Data and saves them as CSV-File if the Trigger is active
-The Trigger could be an Bool from the recieved Data or an Timer
