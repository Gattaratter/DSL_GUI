Projektstruktur\
source/sourceCodeGUI: Pythonskripte, für den graphischen DSL-Designer \
  /MainWindow.py: Startet das Programm
  
source/savefiles: \
  /DSL:                    Enthält generierte DSL-Modelle\
  /DSLEvents/BasicCamera:  Enthält eine Zuordnung der BasisEvents für Kameras\
  /DSLEvents/CustomCamera: Enthält eine Zuordnung der CustomEvents für Kameras\
  /plans:                  Enthält gespeicherte Pläne vom physischen Aufbau

source/resources: \
  /configurations:   Enthält config Dateien, z.B. für das Logging vom graphischen Deisigner\
  /icons:            Enthält Bilder für den graphischen Designer

source/GeneratedPythonCode: nutzbarer generierter Code\
  /DSLPythonPackage:  Bibliothek für den generierten Code\
  /PypylonMockup:     Bibliohek zum Testen ohne Kameras

source/DSLProcessing: Grammatik und Bestandteile, um Python-Code zu generieren\
  /DSLsourceGraphs:     visuelle darstellung der DSL-Modelle\
  /DSLsourcePrograms:   DSL-Modelle, die verarbeitet werden sollen\
  /GeneratorSourceCode: Codegenerator inklusive verwendeter Module
  
  
  
  
