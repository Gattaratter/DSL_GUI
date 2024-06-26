from textx import metamodel_from_file, textx_isinstance
import LineCreator
import SemanticValidator

import logging
logger = logging.getLogger(__name__)
logging.basicConfig(filename='logfile.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)8s: %(message)s')

'''The generator interprets the AST of the DSL model, checks the semantics with the SemanticValidator and simultaneously generates Python codelines'''
def main():
    # Laden der Grammatik inklusive dem zu nutzenden DSL-Modell
    DSL_meta = metamodel_from_file("../camera_grammar.tx")
    #DSLPath = "../../savefiles/DSL/TestNestedCustomEvent.cam"
    DSLPath = "../DSLsourcePrograms/modell.cam"
    DSLProgramm = DSL_meta.model_from_file(DSLPath)
    #PythonPath = "../../GeneratedPythonCode/Tests/TestVerwendungsbeispiel.py"
    PythonPath = "../../GeneratedPythonCode/generatedCode.py"

    # Objekte, um Strings zu erzeugen und die Semantik zu prüfen
    lineCreator = LineCreator.LineCreator(DSL_meta)
    semanticValidator = SemanticValidator.SemanticValidator(DSL_meta)


    with open(PythonPath, 'w') as savefile:
        savefile.write(f"#The following code was generated out of DSL-code from the file: {DSLPath}")
       # savefile.write(f"\nimport sys")
       # savefile.write(f"\nsys.path.append('../../GeneratedPythonCode')")
        savefile.write(lineCreator.lines_import())
        savefile.write("\nlogger.info('Program wurde gestartet')")

        # Definition aller Eventfunktionen zuerst
        for command in DSLProgramm.commands:
            #print("Main:", type(command))
            if textx_isinstance(command, DSL_meta["CustomEvent"]):
                extraSemanticValidator = SemanticValidator.SemanticValidator(DSL_meta)
                extraSemanticValidator.add_command(command)
                semanticValidator.rule_unique_eventNames(command)
                if extraSemanticValidator.returnMessage:
                    semanticValidator.returnMessage += extraSemanticValidator.returnMessage
                savefile.write(lineCreator.lines_customEvent(command))

        # allgemeine Strukturen
        savefile.write(lineCreator.lines_setup())

        # sämtliche Prgramm spezifischen lines inklusive semantischer Kontrolle
        for command in DSLProgramm.commands:
            if textx_isinstance(command, DSL_meta["CustomEvent"]):
                continue
            semanticValidator.add_command(command)
            savefile.write(lineCreator.lines_programCommand(command))

        # Kompelierungsstatus
        if semanticValidator.returnMessage:
            logger.info(f"Program wurde mit Fehlern generiert:{semanticValidator.returnMessage}")
        else:
            logger.info(f"Program wurde erfolgreich generiert")
        # log Programmende
        savefile.write("\nlogger.info('Program wurde beendet')")


if __name__ == "__main__":
    main()
