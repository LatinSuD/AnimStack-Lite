#!/usr/bin/env python3

# A plugin similar to AnimStack, but simpler and compatible with Gimp 3
# By LatinSuD (but based on tshatrov's original plugin)

import gi
gi.require_version('Gimp', '3.0')
gi.require_version('GimpUi', '3.0')
gi.require_version('Gegl', '0.4')
from gi.repository import Gimp, GimpUi, GObject, GLib, Gio, Gegl

import sys


class OutlineSimple(Gimp.PlugIn):
    ## --- Standard GIMP 3 plugin boilerplate ---
    __gtype_name__ = "python_fu_outline_simple"

    
    ## GimpPlugIn virtual methods ##
    def do_query_procedures(self):
        return ['animstack-lite', 'flatten-layer-groups']

    # Register the procedures at load time
    def do_create_procedure(self, name):
        if name == 'animstack-lite':
            procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run_animstack, None)
            
            procedure.set_image_types("*")
            procedure.set_menu_label("AnimStack Lite")
            procedure.add_menu_path('<Image>/Filters/Animation')
            
            procedure.set_documentation("Processes AnimStack Lite tags",
                                    ".",
                                    name)
            procedure.set_attribution("LatinSuD",
                                    "MIT License",
                                    "2026")
            
            return procedure
        elif name == 'flatten-layer-groups':
            procedure = Gimp.ImageProcedure.new(self, name,
                                            Gimp.PDBProcType.PLUGIN,
                                            self.run_flatten, None)
            
            procedure.set_image_types("*")
            procedure.set_menu_label("Flatten Layer Groups")
            procedure.add_menu_path('<Image>/Filters/Animation')
            
            procedure.set_documentation("Flatten Layer Groups",
                                    ".",
                                    name)
            procedure.set_attribution("LatinSuD",
                                    "MIT License",
                                    "2026")
            
            return procedure
        

    # Actually run the plugin
    def run_animstack(self, procedure, run_mode, image, drawables, config, run_data):
        import re
                
        # Start undo group
        image.undo_group_start()
      
        try:

            # FG Layers
            active = []
            layers = image.get_layers()
            for layer in layers:
                    # Obtener el nombre de la capa
                    layer_name = layer.get_name()

                    # Identify FG layers
                    tag = re.search(r"\[(fg|bg)(:([0-9]+))?\]", layer_name)
                    if tag:
                        tipo = tag.group(1)
                        if tag.group(3):
                            active.append({"layer":layer, "type":tipo, "count": int(tag.group(3))})
                        else:
                            active.append({"layer":layer, "type":tipo, "count": -1})

                    else:
                        if layer.is_group():
                            group = layer
                        else:
                            group = None

                        # Apply to each layer
                        for fg in active:
                                if fg["type"]=="fg" and ( fg["count"]>0 or fg["count"]==-1 ):
                                    if fg["count"]>0:
                                        fg["count"]-=1

                                    # Convert current layer to a group if we are not already
                                    if not group:
                                        # Obtener la posición de la capa en la pila
                                        parent = layer.get_parent()
                                        position = image.get_item_position(layer)

                                        # Crear un nuevo grupo de capas
                                        group = Gimp.GroupLayer.new(image)
                                        group.set_name(f"{layer_name}")

                                        # Insertar el grupo en la misma posición que tenía la capa
                                        image.insert_layer(group, parent, position)

                                        # Mover la capa dentro del grupo
                                        image.reorder_item(layer, group, 0)

                                    l2 = fg["layer"].copy()
                                    l2.set_name(l2.get_name().replace("[fg]",""))
                                    image.insert_layer(l2, group, -1)

            for l in active:
                if l["type"]=="fg":
                    image.remove_layer(l["layer"])


            # BG layers
            active = []
            layers = image.get_layers()
            layers.reverse()
            for layer in layers:
                    # Obtener el nombre de la capa
                    layer_name = layer.get_name()

                    # Identify BG layers
                    tag = re.search(r"\[(fg|bg)(:([0-9]+))?\]", layer_name)
                    if tag:
                        tipo = tag.group(1)
                        if tag.group(3):
                            active.append({"layer":layer, "type":tipo, "count": int(tag.group(3))})
                        else:
                            active.append({"layer":layer, "type":tipo, "count": -1})

                    else:
                        if layer.is_group():
                            group = layer
                        else:
                            group = None

                        # Apply to each layer
                        for bg in active:
                                if bg["type"]=="bg" and ( bg["count"]>0 or bg["count"]==-1 ):
                                    if bg["count"]>0:
                                        bg["count"]-=1

                                    # Convert current layer to a group if we are not already
                                    if not group:
                                        # Obtener la posición de la capa en la pila
                                        parent = layer.get_parent()
                                        position = image.get_item_position(layer)

                                        # Crear un nuevo grupo de capas
                                        group = Gimp.GroupLayer.new(image)
                                        group.set_name(f"{layer_name}")

                                        # Insertar el grupo en la misma posición que tenía la capa
                                        image.insert_layer(group, parent, position)

                                        # Mover la capa dentro del grupo
                                        image.reorder_item(layer, group, 0)

                                    l2 = bg["layer"].copy()
                                    l2.set_name(l2.get_name().replace("[bg]",""))
                                    num_children = len(group.get_children())
                                    image.insert_layer(l2, group, num_children)

            for l in active:
                image.remove_layer(l["layer"])
            
        except Exception as e:
            image.undo_group_end()
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), 
                                          f"Error: {str(e)}", 0)
            return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR, error)
        
        image.undo_group_end()
        Gimp.displays_flush()
        
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


    # Run Flatten Layer Groups
    def run_flatten(self, procedure, run_mode, image, drawables, config, run_data):
                
        # Start undo group
        image.undo_group_start()
      
        try:
            procedure = Gimp.get_pdb().lookup_procedure('gimp-group-layer-merge')
            layers = image.get_layers()
            for layer in layers:
                if layer.is_group():
                    config = procedure.create_config()
                    config.set_property('group-layer', layer)
                    result = procedure.run(config)
        except Exception as e:
            image.undo_group_end()
            error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), 
                                          f"Error: {str(e)}", 0)
            return procedure.new_return_values(Gimp.PDBStatusType.EXECUTION_ERROR, error)
        
        image.undo_group_end()
        Gimp.displays_flush()
        
        return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(OutlineSimple.__gtype_name__, sys.argv)

