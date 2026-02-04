# AnimStack-Lite
Animation tools for Gimp 3. It allows to add overlays or backgrounds to multiple existing layers (frames of an animation).

Based on [tshatrov's AnimStack](https://tshatrov.github.io/animstack) plugin, this version is written in Python and is compatible with Gimp 3.

## Currently implemented features
- `[fg]` and `[bg]` effects
- Layer Limits for those effects
- Flatten Layer Groups function (although Gimp 3 implements it natively)

## Examples and tutorial
- Put a layer named `my_background[bg]` at the botton of your layers and run script in order to make it the background for every other layer.
- Put a layer named `my_overlay[fg]` at the top of your layers and run script in order to overlay that layer on top of every other layer.
- Put a layer named `my_overlay[fg:5]` and run script in order to overlay that layer on top of 5 layers below it.
- Don't forget to combine all layer groups at the end.

You can hopefully run the first part of this video also with AnimStack-Lite:

https://www.youtube.com/watch?v=lHKx0g8xEl4
