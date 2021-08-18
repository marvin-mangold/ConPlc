- tested with S7-300, S7-1200 and S7-1500
- example TIA-Portal project included

PLC:
The PLC-Block "ConPLC" sends an UDT (User Defined Datatype) via TCP to the PC.
- in the PLC-Software call the FB "ConPLC"
- connect it with the datablock where the UDT-data is saved
- setup the IP-address and portnumber
- save the UDT source on your local machine

Software:
The PC-Programm recieves data from the PLC and show the live data or saves it as CSV-File.
- setup the IP-address and portnumber for the TCP-Server
- open the UDT source to sync the datastructure
- define the CSV - name, path, seperator and rows
- select the data for each row
- select the triggermode (time based or rising edge of a boolean datapoint)


https://user-images.githubusercontent.com/10088323/119235272-ed106b80-bb31-11eb-926f-328e9d561289.mp4

<p align="center">
  <iframe width="560" height="315" src="https://user-images.githubusercontent.com/10088323/119235272-ed106b80-bb31-11eb-926f-328e9d561289.mp4" title="ConPlc-Video" frameborder="0" allow="accelerometer"; "autoplay"; "clipboard-write"; "encrypted-media"; "gyroscope"; "picture-in-picture" allowfullscreen></iframe>
</p>

<iframe width="955" height="537" src="https://www.youtube.com/embed/2P87NS63K94" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
