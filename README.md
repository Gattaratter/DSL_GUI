Projektstruktur\
source/sourceCodeGUI: Pythonskripte, für den graphischen DSL-Designer \
&emsp;/MainWindow.py: Startet das Programm
  
source/savefiles: \
&emsp;/DSL:                    Enthält generierte DSL-Modelle\
&emsp;/DSLEvents/BasicCamera:  Enthält eine Zuordnung der BasisEvents für Kameras\
&emsp;/DSLEvents/CustomCamera: Enthält eine Zuordnung der CustomEvents für Kameras\
&emsp;/plans:                  Enthält gespeicherte Pläne vom physischen Aufbau

source/resources: \
&emsp;/configurations:   Enthält config Dateien, z.B. für das Logging vom graphischen Deisigner\
&emsp;/icons:            Enthält Bilder für den graphischen Designer

source/GeneratedPythonCode: nutzbarer generierter Code\
&emsp;/DSLPythonPackage:  Bibliothek für den generierten Code\
&emsp;/PypylonMockup:     Bibliohek zum Testen ohne Kameras\
&emsp;/Tests:     DSL-Testmodelle, aus denen Python-Code generiert wurde

source/DSLProcessing: Grammatik und Bestandteile, um Python-Code zu generieren\
  &emsp;/DSLsourceGraphs:     visuelle darstellung der DSL-Modelle\
  &emsp;/DSLsourcePrograms:   DSL-Modelle, die verarbeitet werden sollen\
  &emsp;/GeneratorSourceCode:\
  &emsp;&emsp;/Codegenerator.py: Script, um aus einem DSL-Modell eine Python-Datei zu generieren\
  &emsp;&emsp;/LineCreator.py: Klasse, um für die einzelnen Konzepte der DSL Strings zu erzeugen\
  &emsp;&emsp;/SemanticValidator.py Klasse, um die Semantik der einzelnen Konzepte und dem DSL-Modell im ganzen zu prüfen:
  
  
  
  
