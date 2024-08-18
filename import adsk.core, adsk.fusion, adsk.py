import adsk.core, adsk.fusion, adsk.cam, traceback

def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui  = app.userInterface
        design = app.activeProduct

        # Obtenha o componente raiz do design ativo.
        rootComp = design.rootComponent

        # Crie um novo esboço no plano XY.
        sketches = rootComp.sketches
        xyPlane = rootComp.xYConstructionPlane
        sketch = sketches.add(xyPlane)

        # Defina os parâmetros para as dimensões da caixa.
        comprimentoParam = design.userParameters.add("comprimento", adsk.core.ValueInput.createByReal(10), "cm", "Comprimento da caixa")
        larguraParam = design.userParameters.add("largura", adsk.core.ValueInput.createByReal(5), "cm", "Largura da caixa")
        alturaParam = design.userParameters.add("altura", adsk.core.ValueInput.createByReal(2), "cm", "Altura da caixa")

        # Desenhe um retângulo usando os parâmetros.
        lines = sketch.sketchCurves.sketchLines
        rectLines = lines.addCenterPointRectangle(adsk.core.Point3D.create(0, 0, 0), adsk.core.Point3D.create(comprimentoParam.value/2, larguraParam.value/2, 0))

        # Obtenha o perfil definido pelo retângulo.
        prof = sketch.profiles.item(0)

        # Crie uma extrusão.
        extrudes = rootComp.features.extrudeFeatures
        extInput = extrudes.createInput(prof, adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
        distance = adsk.core.ValueInput.createByReal(alturaParam.value)
        extInput.setDistanceExtent(False, distance)
        ext = extrudes.add(extInput)

        # Notifique o usuário que a caixa foi criada.
        ui.messageBox('Caixa paramétrica criada com sucesso!')

    except:
        if ui:
            ui.messageBox('Falha:\n{}'.format(traceback.format_exc()))
