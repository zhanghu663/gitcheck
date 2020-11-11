;FLAVOR:Marlin
;TIME:2790
;Filament used: 2.08451m
;Layer height: 0.2
;MINX:18.931
;MINY:40.2
;MINZ:0.2
;MAXX:55.211
;MAXY:76.48
;MAXZ:20
;Generated with Cura_SteamEngine 4.2.1
M140 S60
M105
M190 S60
M104 S200
M105
M109 S200
M82 ;absolute extrusion mode
M201 X500.00 Y500.00 Z100.00 E5000.00 ;Setup machine max acceleration
M203 X500.00 Y500.00 Z10.00 E50.00 ;Setup machine max feedrate
M204 P500.00 R1000.00 T500.00 ;Setup Print/Retract/Travel acceleration
M205 X8.00 Y8.00 Z0.40 E5.00 ;Setup Jerk
M220 S100 ;Reset Feedrate
M221 S100 ;Reset Flowrate

G28 ;Home

G92 E0 ;Reset Extruder
G1 Z2.0 F3000 ;Move Z Axis up
G1 X10.1 Y20 Z0.28 F5000.0 ;Move to start position
G1 X10.1 Y200.0 Z0.28 F1500.0 E15 ;Draw the first line
G1 X10.4 Y200.0 Z0.28 F5000.0 ;Move to side a little
G1 X10.4 Y20 Z0.28 F1500.0 E30 ;Draw the second line
G92 E0 ;Reset Extruder
G1 Z2.0 F3000 ;Move Z Axis up

G92 E0
G92 E0
G1 F2700 E-5
;LAYER_COUNT:100
;LAYER:0
M107
G0 F6000 X23.311 Y41.121 Z0.2
;TYPE:SKIRT
G1 F2700 E0
G1 F1200 X24.044 Y40.784 E0.02952
G1 X24.807 Y40.521 E0.05904
G1 X25.592 Y40.336 E0.08855
G1 X26.391 Y40.228 E0.11805
G1 X27.071 Y40.2 E0.14295
G1 X47.034 Y40.2 E0.87332
G1 X47.84 Y40.24 E0.90284
G0 F9000 X44.484 Y63.787
G1 F1500 X43.583 Y64.688 E2084.21933
G0 F9000 X43.583 Y65.31
G1 F1500 X44.484 Y64.409 E2084.26595
G0 F9000 X44.484 Y65.031
G1 F1500 X43.763 Y65.753 E2084.30328
G0 F9000 X44.385 Y65.753
G1 F1500 X44.484 Y65.654 E2084.3084
G0 F9000 X42.801 Y66.403
G0 X42.698 Y66.505
;TYPE:SKIN
G1 F1500 X42.395 Y66.498 E2084.31415
G1 X32.128 Y66.498 E2084.50902
G0 F9000 X31.927 Y66.388
G1 F1500 X31.707 Y66.608 E2084.51471
;TIME_ELAPSED:2790.004464
G1 F2700 E2079.51471
M140 S0
M107
G91 ;Relative positionning
G1 E-2 F2700 ;Retract a bit
G1 E-2 Z0.2 F2400 ;Retract and raise Z
G1 X5 Y5 F3000 ;Wipe out
G1 Z10 ;Raise Z more
G90 ;Absolute positionning
M84
G1 X0 Y220 ;Present print

;End of Gcode
;SETTING_3 {"extruder_quality": ["[general]\\nversion = 4\\nname = Standard Qual
;SETTING_3 ity #2\\ndefinition = creality_base\\n\\n[metadata]\\nsetting_version
;SETTING_3  = 8\\nposition = 0\\ntype = quality_changes\\nquality_type = standar
;SETTING_3 d\\n\\n[values]\\nwall_thickness = 2\\n\\n"], "global_quality": "[gen
;SETTING_3 eral]\\nversion = 4\\nname = Standard Quality #2\\ndefinition = creal
;SETTING_3 ity_base\\n\\n[metadata]\\nsetting_version = 8\\ntype = quality_chang
;SETTING_3 es\\nquality_type = standard\\n\\n[values]\\nadhesion_type = brim\\nd
;SETTING_3 efault_material_bed_temperature = 60\\n\\n"}
