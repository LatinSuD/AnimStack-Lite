# AnimStack-Lite
A simplified version of AnimStack for Gimp 3

Based on [tshatrov's AnimStack](https://tshatrov.github.io/animstack) plugin, this version is written in Python and is compatible with Gimp 3.

Currently implemented features:
- [fg] and [bg] effects
- Layer Limits for those effects

Examples:
- Put a layer named `my_background[bg]` at the botton of your layers and run script in order to make it the background for every other layer.
- Put a layer named `my_overlay[fg]` at the top of your layers and run script in order to overlay that layer on top of every other layer.
- Put a layer named `my_overlay[fg:5]` and run script in order to overlay that layer on top of 5 layers below it.
- Don't forget to combine all layer groups at the end (Gimp 3 can do this natively).

You can hopefully run the first tutorial of this video also with AnimStack-Lite:
https://www.youtube.com/watch?v=lHKx0g8xEl4
