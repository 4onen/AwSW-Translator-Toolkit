from modloader.modclass import Mod, loadable_mod

import jz_magmalink as ml

import renpy.game

@loadable_mod
class MyAwSWMod(Mod):
    name = "Translator Toolkit"
    version = "v0.8"
    author = "4onen"
    dependencies = ["MagmaLink"]

    @staticmethod
    def mod_load():
        ( ml.Overlay()
            .add(['textbutton "Mod Translation":'\
                 ,'    xalign 0.5'\
                 ,'    yalign 0.7'\
                 ,'    action [Show("four_tltk_bg", transition=dissolve), Show("four_tltk_screen"), Play("audio", "se/sounds/open.ogg")]'\
                 ,'    hovered Play("audio", "se/sounds/select.ogg")'\
                ])
            .compile_to("main_menu")
        )

    @staticmethod
    def mod_complete():
        pass
        # print(list(renpy.game.script.translator.file_translates.keys()))
