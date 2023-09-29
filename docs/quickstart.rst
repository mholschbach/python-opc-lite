Quick Start
===========

Python Support
--------------

This library supports these Python versions::
    3.11

This library may be compatible with earlier versions of python as well.


Installation
------------

Use pip to install this libary::

    pip install python-opc-lite
    
Introduction
------------

OPC stands for Open Package Convention. It is used to package the Office Open XML 
documents like powerpoint pptx, word docx, excel xlsx etc. 


For simple understanding, we can say that opc package is a zip file containing
many files. For example below tree shows the contents of some pptx file.

::
    
    .
    |-- [Content_Types].xml
    |-- _rels
    |   `-- .rels
    |-- docProps
    |   |-- app.xml
    |   |-- core.xml
    |   `-- thumbnail.jpeg
    `-- ppt
        |-- _rels
        |   `-- presentation.xml.rels
        |-- presProps.xml
        |-- presentation.xml
        |-- slideLayouts
        |   |-- _rels
        |   |   `-- slideLayout1.xml.rels
        |   `-- slideLayout1.xml
        |-- slideMasters
        |   |-- _rels
        |   |   `-- slideMaster1.xml.rels
        |   `-- slideMaster1.xml
        |-- slides
        |   |-- _rels
        |   |   `-- slide1.xml.rels
        |   `-- slide1.xml
        |-- tableStyles.xml
        |-- theme
        |   `-- theme1.xml
        `-- viewProps.xml


For simplicity, package contents are called as items. Items are are of
two categories. One is ContentType and the other is Part

There is only one ContentType item in a package. It is \"/[Content_Types].xml\"
at the top level of package structure.

All items except ContentType item are called Part item or just Part. Parts
that have \".rels\" extension are called RelsPart (special Part). 

Each RelsPart is associated with one Part such that if path of Part is 
\"/ppt/presentation.xml\" then its RelsPart would be \"/ppt/_rels/presentation.xml.rels\"

RelsPart \"/_rels/.rels\" is considered as RelsPart of package itself.

Every Part need not have a corresponding RelsPart. But every RelsPart has a
corresponding Part except the package's RelsPart.

RelsPart contains the relationship information among different Parts in a package.


Examples
--------

Below are many examples to show how this libary can be used to read, write and navigate through
the powerpoint file (\*.pptx file)


Example to show how to read and write an opc package::

    from opc import Package

    # create an object of package with path of the file and read contents
    package = Package("/some/path/to/presentation.pptx").read()

    # do some changes to the content of the package

    # write the package to a file
    package.write("/some/other/path/to/saved.pptx")

|

Example to show how to get a part of an opc package::

    presentation_part = package.get_part('/ppt/presentation.xml')

|

Example to get the rels part of a part::

    presentation_rels_part = presentation_part.get_rels_part()

|

Example to get the related part (slide) of a part(presentation)::

    slide_part = presentation_part.get_related_part('rId2')

|

Example to add a part to the package::

    part = package.add_part('/uri/str/of/part.xml', "type/of/part")

|

Example to register a hook to the given part type. 
This callback will be called when part of registered type is 
encountered while reading the package

::

    package = Package("/some/path/to/presentation.pptx")
    package.register_part_hook('/some/type', some_callback)
    package.register_part_hook('/some/other/type', some_other_callback)
    package.read()

    # callbacks are called with the part object as the argument
    # one can use this feature to construct objects of certain classes depending on types
    # return of callback will be assigned to typeobj property of part object

    part = package.get_parts('/some/type')[0]
    part.typeobj # will refer the return value of callback of the hook 

    # typeobj that are returned by the callback must implement read and write methods.
    # these methods would be called when reading/writing the content of a part 



