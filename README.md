## Blender automation (Bauto) with python

Setting up development environment:

- maintain code within site-packages folder of Blender (similar to any other regularly installed package)
- set symbolic links to add-on python files from within scripts/addons directory
- to dynamically re-import and develop add-ons:
    - import add-on python file (with register() call in main block)
    - use importlib to re-import

```
# install add-on during development
import bauto.bauto.text_addon
bauto.bauto.text_addon.register()

# re-import
import importlib
importlib.reload(bauto.bauto.text_addon)
bauto.bauto.text_addon.register()
```
