.. highlight:: python

About Sphinx
============

Sphinx is a tool for making documentation. It was originally created for the
`Python documentation <https://docs.python.org/3/>`_, but is now used for many other software projects.

Sphinx uses :term:`reStructuredText` as its markup language.
It can produce HTML, LaTeX, ePub and PDF documents.

Source: https://www.sphinx-doc.org


Getting started
---------------

After installation, you can get started quickly with the tool 
:program:`sphinx-quickstart`. Just enter::

   sphinx-quickstart

Answer each customization question with yes or no. Be sure to say **yes** to the **autodoc** extension.
The :program:`sphinx-quickstart` creates a directory with several documents:

- :file:`conf.py` file, the *default configuration file*
- :file:`index.rst` file, the *master document*

The :file:`conf.py` file let's you configure all aspects of Sphinx.
The :file:`index.rst` is the entry page for your documentation.
It contains the ``toctree`` directive which determines the files to include. 
For this project it looks like this::

   .. toctree::
      :maxdepth: 2
      :caption: Contents:

      1_intro/intro
      2_draw/draw
      3_image/image
      ...

To build the HTML pages just run::

   make html

To make the PDF document run::

   make pdf

reStructuredText
----------------

reStructuredText (.rst) is the default markup language used with Sphinx.
It is important to know that:

- paragraphs are separated by one or more blank lines
- indentation is significant

Inline styles
^^^^^^^^^^^^^

Inside text you can use:

- one asterisk for *italics*
- two asterisks for **bold**
- backquotes for ``code``

Lists
^^^^^

This code:

.. code-block:: none
   :linenos:

   * This is a bulleted list.
   * It has two items, the second
     item uses two lines.

   #. This is a numbered list.
   #. It has two items too.

produces this result:

* This is a bulleted list.
* It has two items, the second
  item uses two lines.

#. This is a numbered list.
#. It has two items too.

Hyperlinks
^^^^^^^^^^

This code::

   `Source <https://www.sphinx-doc.org>`_

produces `Source <https://www.sphinx-doc.org>`_

Admonitions
^^^^^^^^^^^

.. danger::
   Be careful with this code!

.. tip::
   Be careful with this code!

.. warning::
   Be careful with this code!

Footnotes
^^^^^^^^^

This is a footnote [#f1]_ inside a text, this is another one [#f2]_.

.. rubric:: Footnotes

.. [#f1] Text of the first footnote
.. [#f2] Text of the second footnote

Horizontal list
^^^^^^^^^^^^^^^

To add a horizontal list add this code::

   .. hlist::
      :columns: 3

      * happy
      ...

.. hlist::
   :columns: 3

   * happy
   * short
   * intelligent
   * thankful
   * displayed
   * horizontal

.. this is a comment

Download
^^^^^^^^

To add a download link add this code::

   :download:`requirements.txt<requirements.txt>`.

:download:`requirements.txt<requirements.txt>`.

Include from a file
-------------------

It is possible to include a Python object (class, method) from a file. 
For example you can include a **class** definition with::

   .. literalinclude:: 5_app/app.py
      :pyobject: Rectangle
      :linenos:
      :emphasize-lines: 5-7

resulting in

.. literalinclude:: 5_app/app.py
   :pyobject: Rectangle
   :linenos:
   :emphasize-lines: 5-7

Or you can include just a **method** definition with:: 

   .. literalinclude:: 5_app/app.py
      :pyobject: Rectangle.render

resulting in

.. literalinclude:: 5_app/app.py
   :pyobject: Rectangle.render

Directives
----------

A directive consists of

- name
- arguments
- options
- content

The structure is this::

   .. name:: arguments
      :option: value

      content

Function
^^^^^^^^

This directive defines a function::

   .. function:: spam(eggs)
                  ham(eggs)

      Spam ham ham the are made with a certain number of eggs.

.. function:: spam(eggs)
                 ham(eggs)

   Spam and ham the are made with a certain number of eggs.


To cross-reference you can use:
 
- :meth:`method_name` with ``:meth:`method_name```
- :class:`class_name` with ``:class:`class_name```
- :func:`function_name` with ``:func:`function_name```

For example with ``:func:`spam``` one can refernce 
the above functions :func:`spam` or :func:`ham` inside a sentence..

.. :module:: pygamelib


Data
^^^^

To describe global data and constants in a module use this code::

   .. data:: number=1000

      Describe data.

produces

.. data:: number=1000

   Describe data.


Class
^^^^^

.. class:: App

   Describe class without parameters.

   .. method:: run()

   Describe the method.

.. class:: App(parameters)

   Describe class with parameters.

   .. attribute:: objects

   Global class attribute.


Functions with arguments
^^^^^^^^^^^^^^^^^^^^^^^^

.. function:: send_message(sender, recipient, message_body, [priority=1])

   Send a message to a recipient

   :param str sender: The person sending the message
   :param str recipient: The recipient of the message
   :param str message_body: The body of the message
   :param priority: The priority of the message, can be a number 1-5
   :type priority: integer or None
   :return: the message id
   :rtype: int
   :raises ValueError: if the message_body exceeds 160 characters
   :raises TypeError: if the message_body is not a basestring


Math formulas
-------------

Since Pythagoras, we know that :math:`a^2 + b^2 = c^2`.

.. math:: e^{i\pi} + 1 = 0
   :label: euler

Euler's identity, equation :math:numref:`euler`, was elected one of the
most beautiful mathematical formulas.


The app module
--------------

This code::

   .. automodule:: app
      :members:
      :member-order: bysource

Prints the whole app documentation and lists members by source order.

.. automodule:: app
   :members:
   :member-order: bysource

Glossary
--------

.. glossary::
   
   reStructuredText
      reStructedText is ligh-weight markup langage. 