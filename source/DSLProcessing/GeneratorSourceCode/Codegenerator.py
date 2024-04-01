from textx import metamodel_from_file, textx_isinstance
import LineCreator
import SemanticValidator

def main():
    DSL_meta = metamodel_from_file("../camera_grammar.tx")
    DSLPath = "../DSLsourcePrograms/simpleCamProgram.cam"
    DSLProgramm = DSL_meta.model_from_file(DSLPath)
    PythonPath = "../../GeneratedPythonCode/generatedCode.py"


    lineCreator = LineCreator.LineCreator(DSL_meta)
    semanticValidator = SemanticValidator.SemanticValidator(DSL_meta)


    with open(PythonPath, 'w') as savefile:
        savefile.write(f"#The following code was generated out of DSL-code from the file: {DSLPath}")
        savefile.write(lineCreator.lines_import())
        savefile.write("\nlogger.info('Program wurde gestartet')")

        # Definition aller Eventfunktionen zuerst
        for command in DSLProgramm.commands:
            print("Main:", type(command))
            customEventList = []
            if textx_isinstance(command, DSL_meta["CustomEvent"]):
                customEventList.append(command)
                savefile.write(lineCreator.lines_customEvent(command))

        # allgemeine Strukturen
        savefile.write(lineCreator.lines_setup())

        # sämtliche Prgramm spezifischen lines
        for command in DSLProgramm.commands:
            semanticValidator.add_command(command)
            if textx_isinstance(command, DSL_meta["CustomEvent"]):
                continue
            savefile.write(lineCreator.lines_programCommand(command))

        # Kompelierungsstatus
        if semanticValidator.returnMessage:
            print(f"\nlogger.info('Program wurde mit Fehlern generiert:{semanticValidator.returnMessage}')")
        else:
            print(f"\nlogger.info('Program wurde erfolgreich generiert')")
        # log Programmende
        savefile.write("\nlogger.info('Program wurde beendet')")


if __name__ == "__main__":
    main()
