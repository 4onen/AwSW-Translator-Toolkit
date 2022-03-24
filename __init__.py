from modloader.modclass import Mod, loadable_mod

import jz_magmalink as ml


def link_test_langauge():
    cn = ( ml.find_label("splashscreen")
            .search_if("persistent.lang == \"Jp\"")
    )
    ( cn.branch()
        .search_menu().add_choice(text="Test Language", jump="four_tltk_activate_test_language")
    )
    ( cn.branch_else()
        .search_menu().add_choice(text="Test Language", jump="four_tltk_activate_test_language")
    )
    cn.link_behind_from("four_tltk_activate_test_language_end")

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

        # link_test_language()

    @staticmethod
    def mod_complete():
        pass
        # print(list(renpy.game.script.translator.file_translates.keys()))
